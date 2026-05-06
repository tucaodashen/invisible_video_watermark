import json
import re
import time
import cv2
import random
import os
import av
import numpy as np

from BasicSystem import const
from BasicSystem.log_client import setup_logger, get_logger

setup_logger(default_tags="VideoProcessor", enable_udp=True, enable_console=True)
logger = get_logger()


def add_audio_to_video(video_path, audio_path, output_path):
    output = None
    try:
        video_in = av.open(video_path)
        audio_in = av.open(audio_path)

        output = av.open(output_path, 'w')

        video_in_stream = video_in.streams.video[0]
        ref_w = video_in_stream.codec_context.width
        ref_h = video_in_stream.codec_context.height
        ref_fps = video_in_stream.average_rate
        ref_codec = video_in_stream.codec_context.name
        video_out = output.add_stream(ref_codec, rate=ref_fps)
        video_out.width = ref_w
        video_out.height = ref_h
        video_out.pix_fmt = 'yuv420p'
        video_out.codec_context.options['preset'] = 'ultrafast'

        audio_in_stream = audio_in.streams.audio[0]
        audio_codec_name = audio_in_stream.codec_context.name
        audio_out = output.add_stream(audio_codec_name, rate=audio_in_stream.codec_context.sample_rate or 44100)
        audio_out.codec_context.sample_rate = audio_in_stream.codec_context.sample_rate or 44100

        for frame in video_in.decode(video_in_stream):
            img = frame.to_ndarray(format='bgr24')
            vf = av.VideoFrame.from_ndarray(img, format='bgr24')
            for packet in video_out.encode(vf):
                output.mux(packet)
        for packet in video_out.encode(None):
            output.mux(packet)

        for frame in audio_in.decode(audio_in_stream):
            for packet in audio_out.encode(frame):
                output.mux(packet)
        for packet in audio_out.encode(None):
            output.mux(packet)

        output.close()
        video_in.close()
        audio_in.close()

        logger.success(f"Add audio to video success: {output_path}", tags="VideoProcessor:add_audio_to_video")

    except Exception as e:
        if output is not None:
            try:
                output.close()
            except Exception:
                pass
        logger.error(f"Add audio to video error: {str(e)}", tags="VideoProcessor:add_audio_to_video")
        raise


def slice_list(target_list, per_len):
    sl_inde = []
    liust_len = len(target_list)
    full_times = liust_len // per_len
    remain_len = liust_len % per_len
    if remain_len == 0:
        for i in range(full_times):
            sl_inde.append(target_list[i * per_len:(i + 1) * per_len])
        return sl_inde
    else:
        for i in range(full_times):
            sl_inde.append(target_list[i * per_len:(i + 1) * per_len])
        sl_inde.append(target_list[full_times * per_len:])
        return sl_inde


def get_frame_count(path):
    cap = cv2.VideoCapture(path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames


def get_count(path):
    cap = cv2.VideoCapture(path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return int(total_frames)


def video_sampler(source_path, sampler_times, sampler_extension, sampler_type, manual=None):
    logger.info(f"Start sampling video: {source_path}", tags="VideoProcessor:video_sampler")
    cap = cv2.VideoCapture(source_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    logger.info(f"Total frames: {total_frames}", tags="VideoProcessor:video_sampler")
    if sampler_type == const.SamplerType.RANDOM:
        primary_sampler_point = []
        for i in range(sampler_times):
            primary_sampler_point.append(random.randint(0, total_frames - 1))
        logger.info(f"Primary sampler point: {primary_sampler_point}", tags="VideoProcessor:video_sampler")
        secondary_sampler_point = []
        for i in primary_sampler_point:
            for ti in range(sampler_extension):
                secondary_sampler_point.append(i + ti)
        logger.info(f"Secondary sampler point: {secondary_sampler_point}", tags="VideoProcessor:video_sampler")
        final_sampler_point = primary_sampler_point + secondary_sampler_point
        final_sampler_point.sort()
        final_sampler_point = list(set(final_sampler_point))
        logger.debug(f"Final sampler point: {final_sampler_point}", tags="VideoProcessor:video_sampler")
        return final_sampler_point
    elif sampler_type == const.SamplerType.FULL:
        final_sampler_point = list(range(total_frames))
        logger.debug(f"Final sampler point: {final_sampler_point}", tags="VideoProcessor:video_sampler")
        return final_sampler_point
    elif sampler_type == const.SamplerType.AVERAGE:
        primary_sampler_point = []
        period = total_frames // sampler_times
        for i in range(sampler_times):
            primary_sampler_point.append(i * period)
        logger.debug(f"Primary sampler point: {primary_sampler_point}", tags="VideoProcessor:video_sampler")
        secondary_sampler_point = []
        for i in primary_sampler_point:
            for ti in range(sampler_extension):
                secondary_sampler_point.append(i + ti)
        logger.debug(f"Secondary sampler point: {secondary_sampler_point}", tags="VideoProcessor:video_sampler")
        final_sampler_point = primary_sampler_point + secondary_sampler_point
        final_sampler_point.sort()
        final_sampler_point = list(set(final_sampler_point))
        logger.info(f"Final sampler point: {final_sampler_point}", tags="VideoProcessor:video_sampler")
        return final_sampler_point
    elif sampler_type == const.SamplerType.PSY:
        pass
    else:
        sampler_list = str(manual).split(",")
        final_sampler_point = []
        for i in sampler_list:
            final_sampler_point.append(int(i))
        logger.debug(f"Final sampler point: {final_sampler_point}", tags="VideoProcessor:video_sampler")
        return final_sampler_point


def extract_frame_by_index(video_path, frame_index, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.critical(f"Failed to open video file: {video_path}", tags="VideoProcessor:extract_frame_by_index")
        raise FileNotFoundError(f"Failed to open video file: {video_path}")
        return
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
        logger.debug(f"Extracted frame {frame_index} to {output_path}", tags="VideoProcessor:extract_frame_by_index")
    else:
        logger.error(f"Failed to extract frame {frame_index} from {video_path}", tags="VideoProcessor:extract_frame_by_index")
    cap.release()


def extract_frames(video_path, start_frame, end_frame, output_dir, formate="png", callback=None):
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(video_path):
        logger.error(f"Failed to open video file: {video_path}", tags="VideoProcessor:extract_frames")
        raise FileNotFoundError(f"Failed to open video file: {video_path}")

    try:
        container = av.open(video_path)
    except Exception as e:
        logger.error(f"Failed to open video file: {video_path}, error: {e}", tags="VideoProcessor:extract_frames")
        raise FileNotFoundError(f"Failed to open video file: {video_path}")

    try:
        stream = container.streams.video[0]
        stream.thread_type = 'AUTO'

        fps = float(stream.average_rate)
        tb = float(stream.time_base)

        if stream.frames:
            total_frames = stream.frames
        elif stream.duration:
            total_frames = int(round(float(stream.duration * stream.time_base) * fps))
        else:
            total_frames = 10 ** 8

        logger.info(f"total_frames: {total_frames}", tags="VideoProcessor:extract_frames")
        logger.info(f"fps: {fps:.2f}", tags="VideoProcessor:extract_frames")

        if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
            logger.warning(f"Invalid frame range: {start_frame} to {end_frame}", tags="VideoProcessor:extract_frames")
            return

        if start_frame > 0 and fps > 0 and tb > 0:
            start_ts = int(start_frame / fps / tb)
            container.seek(max(0, start_ts - 1), stream=stream)

        for frame in container.decode(stream):
            if frame.pts is not None:
                frame_idx = int(round(frame.pts * tb * fps))
            else:
                continue

            if frame_idx > end_frame:
                break

            if frame_idx < start_frame:
                continue

            img = frame.to_ndarray(format='bgr24')
            output_path = os.path.join(output_dir, f"frame_{frame_idx:06d}.{formate}")
            cv2.imwrite(output_path, img)

            if callback is not None and not isinstance(callback, float):
                total_count = (end_frame - start_frame + 1) * 1.0
                cur = (frame_idx - start_frame) * 1.0
                try:
                    if cur / total_count <= 0.98:
                        callback(cur / total_count)
                    else:
                        callback(1)
                except TypeError:
                    callback(1)

    finally:
        container.close()

    logger.info(f"\nOver! Extracted {end_frame - start_frame + 1} to {output_dir}",
                tags=f"VideoProcessor:extract_frames:{os.path.basename(video_path)}")


def ffmpeg_extract_frames(video_path, start_frame, end_frame, output_dir, formate="png", callback=None):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"Failed to open video file: {video_path}", tags="VideoProcessor:extract_frames")
        raise FileNotFoundError(f"Failed to open video file: {video_path}")
        return
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    logger.info(f"total_frames: {total_frames}", tags="VideoProcessor:extract_frames")
    logger.info(f"fps: {fps:.2f}", tags="VideoProcessor:extract_frames")
    if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
        logger.warning(f"Invalid frame range: {start_frame} to {end_frame}", tags="VideoProcessor:extract_frames")
        cap.release()
        return
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    for frame_num in range(start_frame, end_frame + 1):
        ret, frame = cap.read()
        if not ret:
            logger.critical(f"Failed to read {frame_num}", tags="VideoProcessor:extract_frames")
            raise RuntimeError(f"Failed to read frame {frame_num} from {video_path}")
            break
        output_path = os.path.join(output_dir, f"frame_{frame_num:06d}.{formate}")
        cv2.imwrite(output_path, frame)
        if frame_num % 1 == 0:
            logger.debug(f"Extracted frame {frame_num}/{end_frame}",
                         tags=f"VideoProcessor:extract_frames:{os.path.basename(video_path)}")
            total = ((end_frame - start_frame + 1) * 1.0)
            cur = ((frame_num - start_frame) * 1.0)
            if callback is not None and not isinstance(callback, float):
                try:
                    if cur / total <= 0.98:
                        callback(cur / total)
                    else:
                        callback(1)
                except TypeError:
                    callback(1)
    cap.release()
    logger.info(f"\nOver! Extracted {end_frame - start_frame + 1} to {output_dir}",
                tags=f"VideoProcessor:extract_frames:{os.path.basename(video_path)}")


def spitter(total_frame_count, split_size):
    logger.info(f"Executing spitter with total_frame_count: {total_frame_count} and split_size: {split_size}",
                tags="VideoProcessor:spitter")
    result = []
    start_index = 0
    while start_index < total_frame_count - 1:
        s_start_index = start_index
        start_index = start_index + split_size
        end_index = min(start_index, total_frame_count)
        result.append((s_start_index, end_index - 1))
    logger.debug(f"Spitter result: {result}", tags="VideoProcessor:spitter")
    return result


if __name__ == '__main__':
    pass
