"""
Conftest for video processing tests — generates test media files using PyAV.
"""
import os
import pytest
import av
import numpy as np
import tempfile
import shutil


def create_test_video(path, width=320, height=240, num_frames=30, fps=30, codec='libx264'):
    """Create a simple test video file."""
    container = av.open(path, 'w')
    stream = container.add_stream(codec, rate=fps)
    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'
    stream.codec_context.options['preset'] = 'ultrafast'

    for i in range(num_frames):
        frame = av.VideoFrame(width, height, 'yuv420p')
        for plane_idx in range(3):
            plane_w = width >> (1 if plane_idx > 0 else 0)
            plane_h = height >> (1 if plane_idx > 0 else 0)
            val = (i * 20 + plane_idx * 50) % 256
            arr = np.full((plane_h, plane_w), val, dtype=np.uint8)
            frame.planes[plane_idx].update(arr)
        frame.pts = i

        for packet in stream.encode(frame):
            container.mux(packet)

    for packet in stream.encode(None):
        container.mux(packet)

    container.close()
    return path


def create_test_audio(path, duration=1.0, sample_rate=44100):
    """Create a simple test audio file (AAC in MP4)."""
    container = av.open(path, 'w')
    stream = container.add_stream('aac')
    stream.codec_context.sample_rate = sample_rate
    stream.codec_context.options['channels'] = '1'
    stream.codec_context.options['layout'] = 'mono'

    total_samples = int(duration * sample_rate)
    chunk_size = 1024
    pts = 0

    for offset in range(0, total_samples, chunk_size):
        nsamples = min(chunk_size, total_samples - offset)
        if nsamples < 1:
            break
        frame = av.AudioFrame(format='fltp', layout='mono', samples=nsamples)
        frame.sample_rate = sample_rate
        arr = (np.sin(2 * np.pi * 440 * np.arange(nsamples) / sample_rate) * 32767).astype(np.float32)
        frame.planes[0].update(arr)
        frame.pts = pts
        pts += nsamples
        for packet in stream.encode(frame):
            container.mux(packet)

    for packet in stream.encode(None):
        container.mux(packet)

    container.close()
    return path


def create_test_video_with_audio(path, width=320, height=240, num_frames=30, fps=30, codec='libx264'):
    """Create a test video with embedded audio track."""
    container = av.open(path, 'w')

    vstream = container.add_stream(codec, rate=fps)
    vstream.width = width
    vstream.height = height
    vstream.pix_fmt = 'yuv420p'
    vstream.codec_context.options['preset'] = 'ultrafast'

    astream = container.add_stream('aac')
    astream.codec_context.sample_rate = 44100
    astream.codec_context.options['channels'] = '1'
    astream.codec_context.options['layout'] = 'mono'

    samples_per_frame = 1024
    audio_pts = 0
    total_samples = int(num_frames / fps * 44100)

    for i in range(num_frames):
        frame = av.VideoFrame(width, height, 'yuv420p')
        for plane_idx in range(3):
            plane_w = width >> (1 if plane_idx > 0 else 0)
            plane_h = height >> (1 if plane_idx > 0 else 0)
            val = (i * 20 + plane_idx * 50) % 256
            arr = np.full((plane_h, plane_w), val, dtype=np.uint8)
            frame.planes[plane_idx].update(arr)
        frame.pts = i
        for packet in vstream.encode(frame):
            container.mux(packet)

        if audio_pts < total_samples:
            chunk = min(samples_per_frame, total_samples - audio_pts)
            aframe = av.AudioFrame(format='fltp', layout='mono', samples=chunk)
            aframe.sample_rate = 44100
            arr = (np.sin(2 * np.pi * 440 * np.arange(chunk) / 44100) * 32767).astype(np.float32)
            aframe.planes[0].update(arr)
            aframe.pts = audio_pts
            audio_pts += chunk
            for packet in astream.encode(aframe):
                container.mux(packet)

    for packet in vstream.encode(None):
        container.mux(packet)
    for packet in astream.encode(None):
        container.mux(packet)

    container.close()
    return path


def create_test_images(dir_path, count=30, width=320, height=240):
    """Create sequential test PNG images."""
    import cv2
    os.makedirs(dir_path, exist_ok=True)
    for i in range(count):
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :, 0] = (i * 20) % 256
        img[:, :, 1] = (i * 30) % 256
        img[:, :, 2] = (i * 10) % 256
        path = os.path.join(dir_path, f"frame_{i:06d}.png")
        cv2.imwrite(path, img)
    return dir_path


@pytest.fixture(scope='function')
def test_video_path():
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, 'test_video.mp4')
    create_test_video(path)
    yield path
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='function')
def test_video_with_audio_path():
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, 'test_video_audio.mp4')
    create_test_video_with_audio(path)
    yield path
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='function')
def test_audio_path():
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, 'test_audio.mp4')
    create_test_audio(path)
    yield path
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='function')
def test_images_dir():
    tmpdir = tempfile.mkdtemp()
    img_dir = os.path.join(tmpdir, 'images')
    create_test_images(img_dir, count=30, width=320, height=240)
    yield img_dir
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='function')
def temp_output_dir():
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope='function')
def temp_dir():
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)
