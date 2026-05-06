"""
Unit tests for PyAV-migrated video processing functions.
Tests all migrated functions from GenerateVideo, VideoProcessor, ProcessUnit, and Slice.
"""
import os
import pytest
import av
import numpy as np
import cv2
import tempfile
import shutil

from modules.GenerateVideo import (
    merge_sequences,
    merge_video_sequnece,
    get_video_parameters_simple,
    get_audio_parameters_simple,
    setup_sequence,
)
from modules.VideoProcessor import (
    extract_frames,
    add_audio_to_video,
    spitter,
    slice_list,
    get_frame_count,
    video_sampler,
    extract_frame_by_index,
)
from modules.AudioProcessor import (
    extract_audio_to_flac,
    get_audio_tracks_info,
)
from BasicSystem.const import (
    Encoder,
    BitRateControl,
    FFmpegTune,
    FFmpegPreset,
    SamplerType,
)


class TestGenerateVideo:

    def test_get_video_parameters_simple(self, test_video_path):
        result = get_video_parameters_simple(test_video_path)
        assert "320×240" in result or "320x240" in result
        assert "30" in result
        assert os.path.basename(test_video_path) in result

    def test_get_video_parameters_simple_invalid_path(self):
        result = get_video_parameters_simple("/nonexistent/video.mp4")
        assert "不存在" in result or "出错" in result

    def test_get_audio_parameters_simple_no_audio(self, test_video_path):
        result = get_audio_parameters_simple(test_video_path)
        assert result == "" or "音频" not in result

    def test_get_audio_parameters_simple_with_audio(self, test_video_with_audio_path):
        result = get_audio_parameters_simple(test_video_with_audio_path)
        assert "音频" in result or "aac" in result.lower()

    def test_merge_sequences_basic(self, test_images_dir, temp_dir):
        output_path = os.path.join(temp_dir, "output.mp4")
        input_pattern = os.path.join(test_images_dir, "frame_%06d.png")
        code = merge_sequences(
            input_files=input_pattern,
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
        assert code == 0
        assert os.path.exists(output_path)
        container = av.open(output_path)
        vstream = container.streams.video[0]
        assert vstream.average_rate == 30
        assert vstream.frames == 30
        container.close()

    def test_merge_sequences_cbr(self, test_images_dir, temp_dir):
        output_path = os.path.join(temp_dir, "output_cbr.mp4")
        input_pattern = os.path.join(test_images_dir, "frame_%06d.png")
        code = merge_sequences(
            input_files=input_pattern,
            output_file=output_path,
            fps=30,
            bitrate_control=BitRateControl.CBR,
            maximum_bitrate="5M",
            target_bitrate="3M",
            video_encoder=Encoder.X264,
            tune=FFmpegTune.NULL,
            preset=FFmpegPreset.X264_VERYFAST,
            output_format="mp4",
        )
        assert code == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 100

    def test_merge_sequences_vbr(self, test_images_dir, temp_dir):
        output_path = os.path.join(temp_dir, "output_vbr.mp4")
        input_pattern = os.path.join(test_images_dir, "frame_%06d.png")
        code = merge_sequences(
            input_files=input_pattern,
            output_file=output_path,
            fps=30,
            bitrate_control=BitRateControl.VBR,
            maximum_bitrate="5M",
            target_bitrate="3M",
            video_encoder=Encoder.X264,
            tune=FFmpegTune.NULL,
            preset=FFmpegPreset.X264_VERYFAST,
            output_format="mp4",
        )
        assert code == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 100

    def test_merge_sequences_debug_mode(self, test_images_dir, temp_dir):
        output_path = os.path.join(temp_dir, "output_debug.mp4")
        input_pattern = os.path.join(test_images_dir, "frame_%06d.png")
        code = merge_sequences(
            input_files=input_pattern,
            output_file=output_path,
            fps=30,
            bitrate_control=BitRateControl.CQP,
            maximum_bitrate="5M",
            target_bitrate="23",
            video_encoder=Encoder.X264,
            tune=FFmpegTune.NULL,
            preset=FFmpegPreset.X264_VERYFAST,
            output_format="mp4",
            debug=True,
        )
        assert code == 0
        assert not os.path.exists(output_path)

    def test_merge_sequences_invalid_encoder(self, test_images_dir, temp_dir):
        class FakeEncoder:
            pass
        fake = FakeEncoder()
        output_path = os.path.join(temp_dir, "output_fail.mp4")
        input_pattern = os.path.join(test_images_dir, "frame_%06d.png")
        with pytest.raises(ValueError, match="Unsupported video encoder"):
            merge_sequences(
                input_files=input_pattern,
                output_file=output_path,
                fps=30,
                bitrate_control=BitRateControl.CQP,
                maximum_bitrate="5M",
                target_bitrate="23",
                video_encoder=fake,
                tune=FFmpegTune.NULL,
                preset=FFmpegPreset.X264_VERYFAST,
                output_format="mp4",
            )

    def test_merge_video_sequnece_multiple_videos(self, test_images_dir, temp_dir):
        import sys
        from loguru import logger
        sys.modules.setdefault('modules.GenerateVideo', type(sys)('modules.GenerateVideo'))
        tmp_logger = logger.bind(tags="test")

        video1_path = os.path.join(temp_dir, "slice1.mp4")
        video2_path = os.path.join(temp_dir, "slice2.mp4")
        merged_path = os.path.join(temp_dir, "merged.mp4")

        input_pattern = os.path.join(test_images_dir, "frame_%06d.png")
        merge_sequences(
            input_files=input_pattern, output_file=video1_path, fps=30,
            bitrate_control=BitRateControl.CQP, maximum_bitrate="5M", target_bitrate="23",
            video_encoder=Encoder.X264, tune=FFmpegTune.NULL,
            preset=FFmpegPreset.X264_VERYFAST, output_format="mp4",
        )
        merge_sequences(
            input_files=input_pattern, output_file=video2_path, fps=30,
            bitrate_control=BitRateControl.CQP, maximum_bitrate="5M", target_bitrate="23",
            video_encoder=Encoder.X264, tune=FFmpegTune.NULL,
            preset=FFmpegPreset.X264_VERYFAST, output_format="mp4",
        )

        code = merge_video_sequnece(
            [video1_path, video2_path], merged_path,
            logger_inst=tmp_logger, audio_file=None, output_format="mp4",
        )
        assert code == 0
        assert os.path.exists(merged_path)
        container = av.open(merged_path)
        vstream = container.streams.video[0]
        assert vstream.frames == 60
        container.close()

    def test_setup_sequence(self, test_images_dir):
        import os
        for f in os.listdir(test_images_dir):
            os.remove(os.path.join(test_images_dir, f))
        for i in range(5):
            img = np.zeros((240, 320, 3), dtype=np.uint8)
            cv2.imwrite(os.path.join(test_images_dir, f"frame_{i:06d}.png"), img)

        pattern = setup_sequence(test_images_dir)
        assert pattern == "frame_%06d.png"


class TestVideoProcessor:

    def test_spitter(self):
        result = spitter(100, 30)
        assert len(result) == 4
        assert result[0] == (0, 29)
        assert result[1] == (30, 59)
        assert result[2] == (60, 89)
        assert result[3] == (90, 99)

    def test_spitter_exact(self):
        result = spitter(60, 30)
        assert len(result) == 2
        assert result[0] == (0, 29)
        assert result[1] == (30, 59)

    def test_slice_list(self):
        result = slice_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
        assert len(result) == 4
        assert result[0] == [1, 2, 3]
        assert result[3] == [10]

    def test_get_frame_count(self, test_video_path):
        count = get_frame_count(test_video_path)
        assert count == 30

    def test_extract_frames(self, test_video_path, temp_output_dir):
        extract_frames(test_video_path, start_frame=0, end_frame=9, output_dir=temp_output_dir)
        files = sorted(os.listdir(temp_output_dir))
        assert len(files) == 10
        assert files[0].startswith("frame_")
        assert files[0].endswith(".png")

    def test_extract_frames_callback(self, test_video_path, temp_output_dir):
        progress_values = []
        def callback(prog):
            progress_values.append(prog)

        extract_frames(test_video_path, start_frame=0, end_frame=4, output_dir=temp_output_dir, callback=callback)
        assert len(progress_values) > 0

    def test_extract_frames_mid_range(self, test_video_path, temp_output_dir):
        extract_frames(test_video_path, start_frame=10, end_frame=19, output_dir=temp_output_dir)
        files = sorted(os.listdir(temp_output_dir))
        assert len(files) == 10

    def test_extract_frames_invalid_range(self, test_video_path, temp_output_dir):
        extract_frames(test_video_path, start_frame=0, end_frame=999, output_dir=temp_output_dir)
        files = os.listdir(temp_output_dir)
        assert len(files) == 0

    def test_extract_frames_invalid_video(self, temp_output_dir):
        with pytest.raises(FileNotFoundError):
            extract_frames("/nonexistent/video.mp4", start_frame=0, end_frame=9, output_dir=temp_output_dir)

    def test_extract_frame_by_index(self, test_video_path, temp_output_dir):
        out_path = os.path.join(temp_output_dir, "single_frame.png")
        extract_frame_by_index(test_video_path, 5, out_path)
        assert os.path.exists(out_path)

    def test_video_sampler_random(self, test_video_path):
        result = video_sampler(test_video_path, sampler_times=3, sampler_extension=2,
                               sampler_type=SamplerType.RANDOM)
        assert len(result) > 0
        assert max(result) <= 30

    def test_video_sampler_full(self, test_video_path):
        result = video_sampler(test_video_path, sampler_times=3, sampler_extension=2,
                               sampler_type=SamplerType.FULL)
        assert result == list(range(30))

    def test_video_sampler_average(self, test_video_path):
        result = video_sampler(test_video_path, sampler_times=3, sampler_extension=2,
                               sampler_type=SamplerType.AVERAGE)
        assert 0 in result

    def test_video_sampler_manual(self, test_video_path):
        result = video_sampler(test_video_path, sampler_times=1, sampler_extension=1,
                               sampler_type=SamplerType.MANUAL, manual="5,10,15")
        assert result == [5, 10, 15]

    def test_add_audio_to_video(self, test_video_path, test_video_with_audio_path, temp_dir):
        output_path = os.path.join(temp_dir, "with_audio.mp4")
        add_audio_to_video(test_video_path, test_video_with_audio_path, output_path)
        assert os.path.exists(output_path)
        container = av.open(output_path)
        audio_streams = [s for s in container.streams if s.type == 'audio']
        assert len(audio_streams) == 1
        container.close()


class TestProcessUnit:

    def test_extract_audio_to_flac(self, test_video_with_audio_path, temp_dir):
        output_path = os.path.join(temp_dir, "audio.flac")
        result = extract_audio_to_flac(test_video_with_audio_path, output_path, audio_track=0)
        assert result is True
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_extract_audio_to_flac_no_audio(self, test_video_path, temp_dir):
        output_path = os.path.join(temp_dir, "audio_no.flac")
        result = extract_audio_to_flac(test_video_path, output_path, audio_track=0)
        assert result is False

    def test_get_audio_tracks_info_with_audio(self, test_video_with_audio_path):
        count = get_audio_tracks_info(test_video_with_audio_path)
        assert count == 1

    def test_get_audio_tracks_info_no_audio(self, test_video_path):
        count = get_audio_tracks_info(test_video_path)
        assert count == 0


class TestEncoderMapping:

    def test_supported_encoders_map(self):
        from modules.GenerateVideo import _ENCODER_MAP
        assert _ENCODER_MAP[Encoder.X264] == 'libx264'
        assert _ENCODER_MAP[Encoder.NVIDIA_H264] == 'h264_nvenc'
        assert _ENCODER_MAP[Encoder.NVIDIA_HEVC] == 'hevc_nvenc'
        assert _ENCODER_MAP[Encoder.NVIDIA_AV1] == 'av1_nvenc'
        assert _ENCODER_MAP[Encoder.AMD_H264] == 'h264_amf'
        assert _ENCODER_MAP[Encoder.AMD_HEVC] == 'hevc_amf'
        assert _ENCODER_MAP[Encoder.Resolume_DXV] == 'dxv'


class TestIntegration:

    def test_full_pipeline_extract_encode_merge(self, test_video_path, temp_output_dir):
        extract_dir = os.path.join(temp_output_dir, "extracted")
        extract_frames(test_video_path, start_frame=0, end_frame=9, output_dir=extract_dir)

        files = sorted(os.listdir(extract_dir))
        assert len(files) == 10

        encode_path = os.path.join(temp_output_dir, "re_encoded.mp4")
        input_pattern = os.path.join(extract_dir, "frame_%06d.png")
        code = merge_sequences(
            input_files=input_pattern,
            output_file=encode_path,
            fps=30,
            bitrate_control=BitRateControl.CQP,
            maximum_bitrate="5M",
            target_bitrate="23",
            video_encoder=Encoder.X264,
            tune=FFmpegTune.NULL,
            preset=FFmpegPreset.X264_VERYFAST,
            output_format="mp4",
        )
        assert code == 0
        assert os.path.exists(encode_path)

        container = av.open(encode_path)
        vstream = container.streams.video[0]
        assert vstream.frames == 10
        assert vstream.average_rate == 30
        container.close()
