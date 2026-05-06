import json
import os
import uuid
import re
import glob
import fractions

import av
import cv2
import numpy as np

from BasicSystem.const import Encoder, BitRateControl, FFmpegTune, FFmpegPreset
from BasicSystem.log_client import setup_logger, get_logger

setup_logger(default_tags="GenerateVideo", enable_udp=True, enable_console=True)
logger = get_logger()


_ENCODER_MAP = {
    Encoder.NVIDIA_H264: 'h264_nvenc',
    Encoder.NVIDIA_HEVC: 'hevc_nvenc',
    Encoder.NVIDIA_AV1: 'av1_nvenc',
    Encoder.AMD_H264: 'h264_amf',
    Encoder.AMD_HEVC: 'hevc_amf',
    Encoder.X264: 'libx264',
    Encoder.Resolume_DXV: 'dxv',
}

_NVIDIA_ENCODERS = {Encoder.NVIDIA_H264, Encoder.NVIDIA_HEVC, Encoder.NVIDIA_AV1}
_AMD_ENCODERS = {Encoder.AMD_H264, Encoder.AMD_HEVC}

_NVIDIA_PRESET_MAP = {
    FFmpegPreset.NVIDIA_P1: 'p1',
    FFmpegPreset.NVIDIA_P2: 'p2',
    FFmpegPreset.NVIDIA_P3: 'p3',
    FFmpegPreset.NVIDIA_P4: 'p4',
    FFmpegPreset.NVIDIA_P5: 'p5',
    FFmpegPreset.NVIDIA_P6: 'p6',
    FFmpegPreset.NVIDIA_P7: 'p7',
}

_AMD_PRESET_MAP = {
    FFmpegPreset.AMD_QUALITY: 'quality',
    FFmpegPreset.AMD_BALANCE: 'balanced',
    FFmpegPreset.AMD_SPEED: 'speed',
}

_X264_PRESET_MAP = {
    FFmpegPreset.X264_UlTRAFAST: 'ultrafast',
    FFmpegPreset.X264_SUPERFAST: 'superfast',
    FFmpegPreset.X264_VERYFAST: 'veryfast',
    FFmpegPreset.X264_FASTER: 'faster',
    FFmpegPreset.X264_FAST: 'fast',
    FFmpegPreset.X264_MEDIUM: 'medium',
    FFmpegPreset.X264_SLOW: 'slow',
    FFmpegPreset.X264_SLOWER: 'slower',
    FFmpegPreset.X264_VERYSLOW: 'veryslow',
    FFmpegPreset.X264_PLACEBO: 'placebo',
}

_X264_TUNE_MAP = {
    FFmpegTune.X264_FILM: 'film',
    FFmpegTune.X264_ANIMATION: 'animation',
    FFmpegTune.X264_GRAIN: 'grain',
    FFmpegTune.X264_STILLIMAGE: 'stillimage',
    FFmpegTune.X264_FASTDECODE: 'fastdecode',
    FFmpegTune.X264_ZEROLANTENCY: 'zerolatency',
}

_NV_TUNE_HQ = {FFmpegTune.NV_AV1_HQ, FFmpegTune.NV_AV1_SHQ, FFmpegTune.NV_H265_SHQ,
               FFmpegTune.NV_H264_HQ, FFmpegTune.NV_H265_HQ}
_NV_TUNE_LL = {FFmpegTune.NV_AV1_LL, FFmpegTune.NV_H264_LL, FFmpegTune.NV_H265_LL}
_NV_TUNE_SLL = {FFmpegTune.NV_AV1_SLL, FFmpegTune.NV_H264_SLL, FFmpegTune.NV_H265_SLL}


def check_codec_available(codec_name, mode='w'):
    try:
        codec = av.codec.Codec(codec_name, mode)
        if codec is None:
            return False
        ctx = codec.create()
        if codec.type == 'video' and mode == 'w':
            ctx.width = 320
            ctx.height = 240
            ctx.pix_fmt = 'yuv420p'
            ctx.time_base = fractions.Fraction(1, 30)
            ctx.framerate = fractions.Fraction(30, 1)
        ctx.open()
        return True
    except Exception:
        return False


def _parse_bitrate_string(bitrate_str):
    bitrate_str = str(bitrate_str).upper().strip()
    if bitrate_str.endswith('M'):
        return int(float(bitrate_str[:-1]) * 1_000_000)
    elif bitrate_str.endswith('K'):
        return int(float(bitrate_str[:-1]) * 1_000)
    else:
        return int(bitrate_str)


def _resolve_image_sequence(input_files):
    directory = os.path.dirname(input_files)
    if not os.path.isdir(directory):
        directory = os.path.dirname(input_files) or '.'
    extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp'}
    files = sorted([
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.splitext(f)[1].lower() in extensions
    ])
    if not files:
        pattern_name = os.path.basename(input_files)
        glob_pattern = re.sub(r'%0*\d*d', '*', pattern_name)
        files = sorted([
            f for f in glob.glob(os.path.join(directory, glob_pattern))
            if os.path.splitext(f)[1].lower() in extensions
        ])
    return files


def _apply_encoder_options(stream, fps, video_encoder, bitrate_control, target_bitrate,
                           maximum_bitrate, tune, preset, fc, psy, two_pass, dxv_alpha=False):
    codec_ctx = stream.codec_context

    if video_encoder == Encoder.Resolume_DXV:
        if dxv_alpha:
            stream.pix_fmt = 'rgba'
        else:
            stream.pix_fmt = 'yuv420p'
        return

    if video_encoder == Encoder.NVIDIA_AV1:
        stream.pix_fmt = 'yuv420p'

    if bitrate_control == BitRateControl.CBR:
        stream.bit_rate = _parse_bitrate_string(target_bitrate)
    elif bitrate_control == BitRateControl.VBR:
        stream.bit_rate = _parse_bitrate_string(target_bitrate)
        codec_ctx.options['maxrate'] = str(_parse_bitrate_string(maximum_bitrate))
        bufsize = str(_parse_bitrate_string(maximum_bitrate) * 2)
        codec_ctx.options['bufsize'] = bufsize
    elif bitrate_control == BitRateControl.CQP:
        if video_encoder in _AMD_ENCODERS:
            raise ValueError("CQP is not supported for AMD encoders")
        elif video_encoder == Encoder.X264:
            codec_ctx.options['crf'] = str(target_bitrate)
        elif video_encoder in _NVIDIA_ENCODERS:
            codec_ctx.options['cq'] = str(target_bitrate)

    if video_encoder not in _AMD_ENCODERS:
        if video_encoder in _NVIDIA_ENCODERS:
            p_val = _NVIDIA_PRESET_MAP.get(preset)
            if p_val:
                codec_ctx.options['preset'] = p_val
        elif video_encoder == Encoder.X264:
            p_val = _X264_PRESET_MAP.get(preset)
            if p_val:
                codec_ctx.options['preset'] = p_val
    else:
        p_val = _AMD_PRESET_MAP.get(preset)
        if p_val:
            codec_ctx.options['quality'] = p_val

    if psy:
        if video_encoder in _NVIDIA_ENCODERS:
            codec_ctx.options['spatial-aq'] = '1'
            codec_ctx.options['aq-strength'] = str(psy)
        elif video_encoder == Encoder.X264:
            codec_ctx.options['aq-mode'] = '1'
            codec_ctx.options['aq-strength'] = str(psy)
        else:
            raise ValueError("Psycho-visual is not supported for this encoder")

    if fc:
        if video_encoder in _NVIDIA_ENCODERS:
            codec_ctx.options['rc-lookahead'] = str(fc)
        elif video_encoder == Encoder.X264:
            codec_ctx.options['rc-lookahead'] = str(fc)
        else:
            raise ValueError("Forward-compatibility is not supported for this encoder")

    if video_encoder not in _AMD_ENCODERS:
        if tune not in (FFmpegTune.NULL, None):
            if video_encoder == Encoder.X264:
                t_val = _X264_TUNE_MAP.get(tune)
                if t_val:
                    codec_ctx.options['tune'] = t_val
            elif video_encoder in _NVIDIA_ENCODERS:
                if tune in _NV_TUNE_HQ:
                    codec_ctx.options['tune'] = 'hq'
                elif tune in _NV_TUNE_LL:
                    codec_ctx.options['tune'] = 'll'
                elif tune in _NV_TUNE_SLL:
                    codec_ctx.options['tune'] = 'ull'

    if two_pass and bitrate_control == BitRateControl.VBR and video_encoder in _NVIDIA_ENCODERS:
        codec_ctx.options['multipass'] = 'fullres'


def merge_sequences(input_files,
                    output_file,
                    fps,
                    bitrate_control,
                    maximum_bitrate,
                    target_bitrate,
                    video_encoder,
                    tune,
                    preset,
                    start_index=None,
                    audio_file=None,
                    fc=False,
                    psy=False,
                    two_pass=False,
                    output_format=None,
                    debug=False,
                    dxv_alpha=False):
    codec_name = _ENCODER_MAP.get(video_encoder)
    if codec_name is None:
        logger.critical(f"Unsupported video encoder: {video_encoder}", tags="GenerateVideo:merge_sequences")
        raise ValueError(f"Unsupported video encoder: {video_encoder}")

    image_files = _resolve_image_sequence(input_files)
    if not image_files:
        raise FileNotFoundError(f"No image files found matching pattern: {input_files}")

    logger.debug(f"Encoding {len(image_files)} frames to {output_file}", tags="GenerateVideo:merge_sequences")
    if debug:
        return 0

    use_alpha = bool(dxv_alpha and video_encoder == Encoder.Resolume_DXV)
    imread_flags = cv2.IMREAD_UNCHANGED if use_alpha else cv2.IMREAD_COLOR
    ndarray_format = 'bgra' if use_alpha else 'bgr24'

    output_container = av.open(output_file, 'w', format=output_format)
    try:
        video_stream = output_container.add_stream(codec_name, rate=fps)
        _apply_encoder_options(
            video_stream, fps, video_encoder, bitrate_control, target_bitrate,
            maximum_bitrate, tune, preset, fc, psy, two_pass, dxv_alpha=use_alpha
        )

        first_img = cv2.imread(image_files[0], imread_flags)
        if first_img is None:
            raise RuntimeError(f"Cannot read image: {image_files[0]}")
        h, w = first_img.shape[:2]
        video_stream.width = w
        video_stream.height = h

        for idx, img_path in enumerate(image_files):
            img = cv2.imread(img_path, imread_flags)
            if img is None:
                logger.warning(f"Cannot read image: {img_path}", tags="GenerateVideo:merge_sequences")
                continue
            if img.shape[:2] != (h, w):
                img = cv2.resize(img, (w, h))

            frame = av.VideoFrame.from_ndarray(img, format=ndarray_format)
            frame.pts = idx

            for packet in video_stream.encode(frame):
                output_container.mux(packet)

        for packet in video_stream.encode(None):
            output_container.mux(packet)
    finally:
        try:
            output_container.close()
        except Exception:
            pass

    logger.success(f"Encoded video: {output_file}", tags="GenerateVideo:merge_sequences")
    return 0


def setup_sequence(path):
    files = sorted(os.listdir(path))
    if not files:
        raise FileNotFoundError(f"No files found in {path}")
    first = files[0]
    temp = str(first.split('.')[0]).split('_')[1]
    length = len(str(temp))
    name = str(first.split('.')[0]).split('_')[0] + "_%0{numlen}d.{prefix}".format(
        numlen=length,
        prefix=str(first.split('.')[1]))
    logger.debug(f"sequence name: {name}", tags="GenerateVideo:merge_sequences")
    return name


def merge_video_sequnece(input_list, output_path, logger_inst, audio_file, output_format):
    name = str(uuid.uuid4())

    first_vid = av.open(input_list[0])
    first_vstream = first_vid.streams.video[0]
    ref_w = first_vstream.codec_context.width
    ref_h = first_vstream.codec_context.height
    ref_fps = first_vstream.average_rate
    ref_pix_fmt = first_vstream.codec_context.pix_fmt
    ref_codec = first_vstream.codec_context.name
    first_vid.close()

    output_container = av.open(output_path, 'w')
    try:
        video_out = output_container.add_stream(ref_codec, rate=ref_fps)
        video_out.width = ref_w
        video_out.height = ref_h
        video_out.pix_fmt = ref_pix_fmt

        for video_path in input_list:
            in_cont = av.open(video_path)
            for frame in in_cont.decode(in_cont.streams.video[0]):
                img = frame.to_ndarray(format='bgr24')
                vf = av.VideoFrame.from_ndarray(img, format='bgr24')
                for packet in video_out.encode(vf):
                    output_container.mux(packet)
            in_cont.close()

        for packet in video_out.encode(None):
            output_container.mux(packet)

        if audio_file:
            for audio_path in audio_file:
                a_in = av.open(audio_path)
                a_in_stream = a_in.streams.audio[0]

                if output_format == 'mov':
                    a_out = output_container.add_stream('aac')
                    a_out.codec_context.sample_rate = a_in_stream.codec_context.sample_rate or 44100
                    a_out.codec_context.options['channels'] = str(a_in_stream.codec_context.channels or 2)
                    a_out.codec_context.options['layout'] = str(a_in_stream.layout or 'stereo')
                    for frame in a_in.decode(a_in_stream):
                        for packet in a_out.encode(frame):
                            output_container.mux(packet)
                    for packet in a_out.encode(None):
                        output_container.mux(packet)
                else:
                    a_out = output_container.add_stream(template=a_in_stream)
                    for packet in a_in.demux(a_in_stream):
                        packet.stream = a_out
                        output_container.mux(packet)
                a_in.close()

    except Exception as e:
        try:
            logger_inst.error(f"merge_video_sequnece error: {e}", tags="GenerateVideo:merge_sequences")
        except Exception:
            pass
        raise
    finally:
        output_container.close()

    if logger_inst:
        try:
            logger_inst.debug(f"merge video sequence {name} success", tags="GenerateVideo:merge_sequences")
        except Exception:
            pass
    return 0


def get_video_parameters_simple(video_path: str) -> str:
    if not os.path.exists(video_path):
        return f"错误: 视频文件不存在: {video_path}"

    try:
        container = av.open(video_path)
        streams = container.streams

        file_size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)

        video_stream = next((s for s in streams if s.type == 'video'), None)

        result_str = "视频关键参数:\n"
        result_str += f"    文件: {os.path.basename(video_path)}\n"
        result_str += f"    大小: {file_size_mb} MB\n"

        if video_stream:
            width = video_stream.width or video_stream.codec_context.width
            height = video_stream.height or video_stream.codec_context.height
            duration = round(float(video_stream.duration * video_stream.time_base)
                             if video_stream.duration else 0, 2)
            fps = video_stream.average_rate
            codec_name = video_stream.codec_context.name if video_stream.codec_context else '未知'

            result_str += f"    分辨率: {width}×{height}\n"
            result_str += f"    时长: {duration}秒\n"
            result_str += f"    帧率: {fps}\n"
            result_str += f"    编码: {codec_name}"

        container.close()
        return result_str

    except Exception as e:
        return f"获取视频参数时出错: {e}"


def get_audio_parameters_simple(video_path: str) -> str:
    if not os.path.exists(video_path):
        return f"错误: 视频文件不存在: {video_path}"

    try:
        container = av.open(video_path)
        streams = container.streams

        audio_stream = next((s for s in streams if s.type == 'audio'), None)

        result_str = ""

        if audio_stream:
            codec_name = audio_stream.codec_context.name if audio_stream.codec_context else '未知'
            sample_rate = audio_stream.codec_context.sample_rate if audio_stream.codec_context else '未知'
            channels = audio_stream.codec_context.channels if audio_stream.codec_context else '未知'
            result_str += f"    音频: {codec_name} "
            result_str += f"    {sample_rate}Hz "
            result_str += f"    {channels}声道\n"

        container.close()
        return result_str

    except Exception as e:
        return f"获取视频参数时出错: {e}"


if __name__ == '__main__':
    pass
