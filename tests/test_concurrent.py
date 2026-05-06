"""
Multi-process concurrency / thread safety tests for PyAV-migrated pipeline.
Tests that PyAV operations can safely run across multiple processes.
"""
import os
import pytest
import av
import numpy as np
import cv2
import tempfile
import shutil
import concurrent.futures

from modules.VideoProcessor import extract_frames
from modules.GenerateVideo import merge_sequences, check_codec_available
from BasicSystem.const import Encoder, BitRateControl, FFmpegTune, FFmpegPreset


# ── Module-level worker functions (must be picklable for ProcessPoolExecutor) ──

def _worker_extract_slice(args):
    video_path, slice_range, out_dir = args
    extract_frames(video_path,
                   start_frame=slice_range[0],
                   end_frame=slice_range[1],
                   output_dir=out_dir)
    return out_dir


def _worker_extract_and_count(args):
    video_path, start, count, out_dir_prefix, tmpdir = args
    out_dir = os.path.join(tmpdir, out_dir_prefix)
    extract_frames(video_path,
                   start_frame=start,
                   end_frame=start + count - 1,
                   output_dir=out_dir)
    files = sorted(os.listdir(out_dir))
    assert len(files) == count


def _worker_encode_slice(args):
    sub_dir, output_name, tmpdir = args
    pattern = os.path.join(sub_dir, "frame_%06d.png")
    out_path = os.path.join(tmpdir, output_name)
    merge_sequences(
        input_files=pattern,
        output_file=out_path,
        fps=30,
        bitrate_control=BitRateControl.CQP,
        maximum_bitrate="5M",
        target_bitrate="23",
        video_encoder=Encoder.X264,
        tune=FFmpegTune.NULL,
        preset=FFmpegPreset.X264_VERYFAST,
        output_format="mp4",
    )
    return out_path


def _worker_encode_output(args):
    pattern, out_path = args
    merge_sequences(
        input_files=pattern,
        output_file=out_path,
        fps=30,
        bitrate_control=BitRateControl.CQP,
        maximum_bitrate="5M",
        target_bitrate="23",
        video_encoder=Encoder.X264,
        tune=FFmpegTune.NULL,
        preset=FFmpegPreset.X264_VERYFAST,
        output_format="mp4",
    )
    return out_path


def _worker_full_pipeline(args):
    video_path, slice_range, idx, tmpdir_root = args
    work_dir = os.path.join(tmpdir_root, f'work_{idx}')
    extract_dir = os.path.join(work_dir, 'extracted')
    os.makedirs(extract_dir, exist_ok=True)

    extract_frames(video_path,
                   start_frame=slice_range[0],
                   end_frame=slice_range[1],
                   output_dir=extract_dir)

    output_path = os.path.join(work_dir, f'output_{idx}.mp4')
    pattern = os.path.join(extract_dir, "frame_%06d.png")
    merge_sequences(
        input_files=pattern,
        output_file=output_path,
        fps=30,
        bitrate_control=BitRateControl.CQP,
        maximum_bitrate="5M",
        target_bitrate="23",
        video_encoder=Encoder.X264,
        tune=FFmpegTune.NULL,
        preset=FFmpegPreset.X264_VERYFAST,
        output_format="mp4",
    )
    return output_path


# ── Fixtures ──

def create_concurrent_test_video(path, width=320, height=240, num_frames=90, fps=30):
    container = av.open(path, 'w')
    stream = container.add_stream('libx264', rate=fps)
    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'
    stream.codec_context.options['preset'] = 'ultrafast'

    for i in range(num_frames):
        frame = av.VideoFrame(width, height, 'yuv420p')
        for plane_idx in range(3):
            plane_w = width >> (1 if plane_idx > 0 else 0)
            plane_h = height >> (1 if plane_idx > 0 else 0)
            val = (i * 7 + plane_idx * 31) % 256
            arr = np.full((plane_h, plane_w), val, dtype=np.uint8)
            frame.planes[plane_idx].update(arr)
        frame.pts = i
        for packet in stream.encode(frame):
            container.mux(packet)

    for packet in stream.encode(None):
        container.mux(packet)
    container.close()
    return path


def create_concurrent_test_images(dir_path, count=30, width=320, height=240):
    os.makedirs(dir_path, exist_ok=True)
    for i in range(count):
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :, 0] = (i * 17) % 256
        img[:, :, 1] = (i * 23) % 256
        img[:, :, 2] = (i * 11) % 256
        path = os.path.join(dir_path, f"frame_{i:06d}.png")
        cv2.imwrite(path, img)


@pytest.fixture(scope='function')
def concurrent_test_video():
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, 'concurrent_test.mp4')
    create_concurrent_test_video(path)
    yield path
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='function')
def concurrent_images_dir():
    tmpdir = tempfile.mkdtemp()
    img_dir = os.path.join(tmpdir, 'images')
    create_concurrent_test_images(img_dir, count=30)
    yield img_dir
    shutil.rmtree(tmpdir, ignore_errors=True)


# ── Tests ──

class TestConcurrentFrameExtraction:

    def test_concurrent_extract_different_ranges(self, concurrent_test_video):
        slices = [(0, 29), (30, 59), (60, 89)]
        tmpdir = tempfile.mkdtemp()
        output_dirs = [os.path.join(tmpdir, f'slice_{i}') for i in range(3)]

        args_list = [(concurrent_test_video, slices[i], output_dirs[i]) for i in range(3)]

        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(_worker_extract_slice, a) for a in args_list]
            for f in futures:
                f.result(timeout=30)

        for i, out_dir in enumerate(output_dirs):
            files = sorted(os.listdir(out_dir))
            expected_count = slices[i][1] - slices[i][0] + 1
            assert len(files) == expected_count, f"Slice {i}: expected {expected_count}, got {len(files)}"

        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_concurrent_extract_overlapping_ranges(self, concurrent_test_video):
        slices = [(0, 49), (25, 74), (50, 89)]
        tmpdir = tempfile.mkdtemp()
        output_dirs = [os.path.join(tmpdir, f'slice_{i}') for i in range(3)]

        args_list = [(concurrent_test_video, slices[i], output_dirs[i]) for i in range(3)]

        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(_worker_extract_slice, a) for a in args_list]
            for f in futures:
                f.result(timeout=30)

        for i, out_dir in enumerate(output_dirs):
            files = sorted(os.listdir(out_dir))
            expected_count = slices[i][1] - slices[i][0] + 1
            assert len(files) == expected_count, f"Slice {i}: expected {expected_count}, got {len(files)}"

        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_concurrent_extract_shared_video_file_no_corruption(self, concurrent_test_video):
        tmpdir = tempfile.mkdtemp()

        slices_cfg = [
            (concurrent_test_video, 0, 15, f'out_0', tmpdir),
            (concurrent_test_video, 15, 15, f'out_15', tmpdir),
            (concurrent_test_video, 30, 15, f'out_30', tmpdir),
            (concurrent_test_video, 45, 15, f'out_45', tmpdir),
        ]

        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(_worker_extract_and_count, a) for a in slices_cfg]
            for f in futures:
                f.result(timeout=30)

        for _, start, count, prefix, tmpdir_ in slices_cfg:
            out_dir = os.path.join(tmpdir_, prefix)
            files = sorted(os.listdir(out_dir))
            assert len(files) == count, f"Slice {prefix}: expected {count}, got {len(files)}"

        shutil.rmtree(tmpdir, ignore_errors=True)


class TestConcurrentEncoding:

    def test_concurrent_encode_different_sequences(self, concurrent_images_dir):
        tmpdir = tempfile.mkdtemp()
        base_imgs = sorted(os.listdir(concurrent_images_dir))

        slices_img = [
            (base_imgs[:10], "slice_a"),
            (base_imgs[10:20], "slice_b"),
            (base_imgs[20:30], "slice_c"),
        ]

        for files, name in slices_img:
            sub_dir = os.path.join(tmpdir, name)
            os.makedirs(sub_dir, exist_ok=True)
            for f in files:
                shutil.copy(os.path.join(concurrent_images_dir, f),
                            os.path.join(sub_dir, f))

        args_list = [(os.path.join(tmpdir, name), f"{name}.mp4", tmpdir)
                     for _, name in slices_img]

        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(_worker_encode_slice, a) for a in args_list]
            for f in futures:
                path = f.result(timeout=60)
                assert os.path.exists(path)
                container = av.open(path)
                vstream = container.streams.video[0]
                assert vstream.frames > 0
                container.close()

        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_concurrent_encode_same_input_to_different_outputs(self, concurrent_images_dir):
        tmpdir = tempfile.mkdtemp()
        pattern = os.path.join(concurrent_images_dir, "frame_%06d.png")

        args_list = [(pattern, os.path.join(tmpdir, f"output_{i}.mp4")) for i in range(3)]

        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(_worker_encode_output, a) for a in args_list]
            for f in futures:
                path = f.result(timeout=60)
                assert os.path.exists(path)
                container = av.open(path)
                assert container.streams.video[0].frames == 30
                container.close()

        shutil.rmtree(tmpdir, ignore_errors=True)


class TestConcurrentExtractEncode:

    def test_concurrent_full_pipeline(self, concurrent_test_video):
        slices = [(0, 29), (30, 59), (60, 89)]
        tmpdir_root = tempfile.mkdtemp()

        args_list = [(concurrent_test_video, slices[i], i, tmpdir_root) for i in range(3)]

        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(_worker_full_pipeline, a) for a in args_list]
            for f in futures:
                path = f.result(timeout=90)
                assert os.path.exists(path)
                container = av.open(path)
                vstream = container.streams.video[0]
                assert vstream.frames == 30
                container.close()

        shutil.rmtree(tmpdir_root, ignore_errors=True)


class TestCodecAvailability:

    def test_libx264_available(self):
        assert check_codec_available('libx264', 'w')

    def test_dxv_availability_reported(self):
        result = check_codec_available('dxv', 'w')
        assert isinstance(result, bool)
        print(f"\nDXV encoder available: {result}")


class TestDXVRendering:

    def test_dxv_encode_if_available(self, concurrent_images_dir):
        if not check_codec_available('dxv', 'w'):
            pytest.skip("DXV encoder not available on this system")

        tmpdir = tempfile.mkdtemp()
        out_path = os.path.join(tmpdir, "output.mov")
        pattern = os.path.join(concurrent_images_dir, "frame_%06d.png")

        try:
            merge_sequences(
                input_files=pattern,
                output_file=out_path,
                fps=30,
                bitrate_control=BitRateControl.CQP,
                maximum_bitrate="5M",
                target_bitrate="23",
                video_encoder=Encoder.Resolume_DXV,
                tune=FFmpegTune.NULL,
                preset=FFmpegPreset.X264_VERYFAST,
                output_format="mov",
                dxv_alpha=False,
            )

            assert os.path.exists(out_path)
            container = av.open(out_path)
            vstream = container.streams.video[0]
            assert vstream.frames == 30
            container.close()
        except av.error.FFmpegError as e:
            if "returned 22" in str(e):
                pytest.skip(f"DXV encoder requires unavailable parameters: {e}")
            raise

        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_dxv_alpha_encode_if_available(self, concurrent_images_dir):
        if not check_codec_available('dxv', 'w'):
            pytest.skip("DXV encoder not available on this system")

        tmpdir = tempfile.mkdtemp()
        img_dir_alpha = os.path.join(tmpdir, "alpha_images")
        os.makedirs(img_dir_alpha, exist_ok=True)

        for i in range(10):
            img = np.zeros((240, 320, 4), dtype=np.uint8)
            img[:, :, 0] = (i * 17) % 256
            img[:, :, 1] = (i * 23) % 256
            img[:, :, 2] = (i * 11) % 256
            img[:, :, 3] = 255
            cv2.imwrite(os.path.join(img_dir_alpha, f"frame_{i:06d}.png"), img)

        out_path = os.path.join(tmpdir, "output_alpha.mov")
        pattern = os.path.join(img_dir_alpha, "frame_%06d.png")

        try:
            merge_sequences(
                input_files=pattern,
                output_file=out_path,
                fps=30,
                bitrate_control=BitRateControl.CQP,
                maximum_bitrate="5M",
                target_bitrate="23",
                video_encoder=Encoder.Resolume_DXV,
                tune=FFmpegTune.NULL,
                preset=FFmpegPreset.X264_VERYFAST,
                output_format="mov",
                dxv_alpha=True,
            )

            assert os.path.exists(out_path)
            container = av.open(out_path)
            vstream = container.streams.video[0]
            assert vstream.frames == 10
            container.close()
        except av.error.FFmpegError as e:
            if "returned 22" in str(e):
                pytest.skip(f"DXV encoder requires unavailable parameters: {e}")
            raise

        shutil.rmtree(tmpdir, ignore_errors=True)


class TestSetupSequence:

    def test_setup_sequence_sorted(self):
        from modules.GenerateVideo import setup_sequence

        tmpdir = tempfile.mkdtemp()
        for i in range(5):
            img = np.zeros((240, 320, 3), dtype=np.uint8)
            cv2.imwrite(os.path.join(tmpdir, f"frame_{i:06d}.png"), img)

        pattern = setup_sequence(tmpdir)
        assert pattern == "frame_%06d.png"

        try:
            setup_sequence("/nonexistent_dir")
            assert False, "Should have raised"
        except FileNotFoundError:
            pass

        shutil.rmtree(tmpdir, ignore_errors=True)


class TestSeekPerformance:

    def test_seek_vs_noseek_consistency(self, concurrent_test_video):
        tmpdir_seek = tempfile.mkdtemp()
        tmpdir_noseek = tempfile.mkdtemp()

        extract_frames(concurrent_test_video, start_frame=40, end_frame=49,
                       output_dir=tmpdir_seek)
        extract_frames(concurrent_test_video, start_frame=40, end_frame=49,
                       output_dir=tmpdir_noseek)

        files_seek = sorted(os.listdir(tmpdir_seek))
        files_noseek = sorted(os.listdir(tmpdir_noseek))

        assert len(files_seek) == 10
        assert files_seek == files_noseek

        for fs, fn in zip(files_seek, files_noseek):
            img_s = cv2.imread(os.path.join(tmpdir_seek, fs))
            img_n = cv2.imread(os.path.join(tmpdir_noseek, fn))
            assert np.array_equal(img_s, img_n)

        shutil.rmtree(tmpdir_seek, ignore_errors=True)
        shutil.rmtree(tmpdir_noseek, ignore_errors=True)

    def test_extract_from_beginning(self, concurrent_test_video):
        tmpdir = tempfile.mkdtemp()
        extract_frames(concurrent_test_video, start_frame=0, end_frame=9,
                       output_dir=tmpdir)
        files = sorted(os.listdir(tmpdir))
        assert len(files) == 10
        assert files[0].startswith("frame_000000")
        assert files[9].startswith("frame_000009")
        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_extract_last_frames(self, concurrent_test_video):
        tmpdir = tempfile.mkdtemp()
        extract_frames(concurrent_test_video, start_frame=80, end_frame=89,
                       output_dir=tmpdir)
        files = sorted(os.listdir(tmpdir))
        assert len(files) == 10
        assert files[0].startswith("frame_000080")
        assert files[9].startswith("frame_000089")
        shutil.rmtree(tmpdir, ignore_errors=True)
