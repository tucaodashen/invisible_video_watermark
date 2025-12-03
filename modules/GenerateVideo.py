import json
import os
import subprocess
import uuid
from BasicSystem.const import Encoder, BitRateControl, FFmpegTune, FFmpegPreset
import sys
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="GenerateVideo", enable_udp=True, enable_console=True)
logger = get_logger()


ffmpeg_path = "ffmpeg.exe"


def execute_command(args):
    logger = get_logger()
    args.append("-y")
    process = subprocess.Popen(
        args,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # 实时处理 stderr 输出
    for line in process.stderr:
        # 处理进度信息（示例）
        if 'time=' in line:
            time_index = line.find('time=')
            if time_index != -1:
                time_str = line[time_index:].split()[0]
                print(f"Progress: {time_str}")

        # 打印到控制台
        #sys.stderr.write(line)
        sys.stderr.flush()
        logger.debug(str(line).replace('\n', ''),tags="GenerateVideo:execute_command")
        print(str(line).replace('\n', ''))

    # 等待命令完成
    return_code = process.wait()
    if return_code!= 0:
        logger.error(f"FFmpeg completed with return code: {return_code},file{args}")
    return return_code


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
                    debug=False):
    """
    Merges image sequences into a single video file using ffmpeg.
    """
    # 执行 FFmpeg 命令
    args = []

    args.append(ffmpeg_path)
    # fps
    args.append('-r')
    args.append(str(fps))
    #start_index
    if start_index is not None:
        args.append('-start_number')
        args.append(str(start_index))
    #input
    args.append('-i')
    args.append(input_files)

    #encoder
    if video_encoder == Encoder.NVIDIA_AV1:
        args.append('-pix_fmt')
        args.append('yuv420p')
    args.append('-c:v')
    if video_encoder == Encoder.NVIDIA_H264:
        args.append('h264_nvenc')
    elif video_encoder == Encoder.NVIDIA_HEVC:
        args.append('hevc_nvenc')
    elif video_encoder == Encoder.NVIDIA_AV1:
        args.append('av1_nvenc')
    elif video_encoder == Encoder.AMD_H264:
        args.append('h264_amf')
    elif video_encoder == Encoder.AMD_HEVC:
        args.append('hevc_amf')
    elif video_encoder == Encoder.X264:
        args.append('libx264')
    elif video_encoder == Encoder.Resolume_DXV:
        args.append('dxv')
    else:
        logger.critical(f"Unsupported video encoder: {video_encoder}",tags="GenerateVideo:merge_sequences")
        raise ValueError(f"Unsupported video encoder: {video_encoder}")

    if video_encoder != Encoder.Resolume_DXV:
        #bitratecontrol

        if bitrate_control == BitRateControl.CBR:
            args.append('-b:v')
            args.append(target_bitrate)
        elif bitrate_control == BitRateControl.VBR:
            args.append('-b:v')
            args.append(target_bitrate)
            args.append('-maxrate')
            args.append(maximum_bitrate)
            args.append('-bufsize')
            args.append(str(float(maximum_bitrate[:-1]) * 2) + "M")
        elif bitrate_control == BitRateControl.CQP:
            if video_encoder == Encoder.AMD_H264 or video_encoder == Encoder.AMD_HEVC:
                logger.critical("CQP is not supported for AMD encoders",tags="GenerateVideo:merge_sequences")
                raise ValueError("CQP is not supported for AMD encoders")
            elif video_encoder == Encoder.X264:
                args.append("-crf")
                args.append(target_bitrate)
            elif video_encoder == Encoder.NVIDIA_H264 or video_encoder == Encoder.NVIDIA_HEVC or video_encoder == Encoder.NVIDIA_AV1:
                args.append('-cq')
                args.append(target_bitrate)
        #preset
        if video_encoder not in [Encoder.AMD_H264, Encoder.AMD_HEVC]:
            args.append('-preset')
            if preset == FFmpegPreset.NVIDIA_P1:
                args.append('p1')
            elif preset == FFmpegPreset.NVIDIA_P2:
                args.append('p2')
            elif preset == FFmpegPreset.NVIDIA_P3:
                args.append('p3')
            elif preset == FFmpegPreset.NVIDIA_P4:
                args.append('p4')
            elif preset == FFmpegPreset.NVIDIA_P5:
                args.append('p5')
            elif preset == FFmpegPreset.NVIDIA_P6:
                args.append('p6')
            elif preset == FFmpegPreset.NVIDIA_P7:
                args.append('p7')
            elif preset == FFmpegPreset.X264_UlTRAFAST:
                args.append('ultrafast')
            elif preset == FFmpegPreset.X264_SUPERFAST:
                args.append('superfast')
            elif preset == FFmpegPreset.X264_VERYFAST:
                args.append('veryfast')
            elif preset == FFmpegPreset.X264_FASTER:
                args.append('faster')
            elif preset == FFmpegPreset.X264_FAST:
                args.append('fast')
            elif preset == FFmpegPreset.X264_MEDIUM:
                args.append('medium')
            elif preset == FFmpegPreset.X264_SLOW:
                args.append('slow')
            elif preset == FFmpegPreset.X264_SLOWER:
                args.append('slower')
            elif preset == FFmpegPreset.X264_VERYSLOW:
                args.append('veryslow')
            elif preset == FFmpegPreset.X264_PLACEBO:
                args.append('placebo')
        else:
            args.append("-quality")
            if preset == FFmpegPreset.AMD_QUALITY:
                args.append('quality')
            elif preset == FFmpegPreset.AMD_BALANCE:
                args.append('balanced')
            elif preset == FFmpegPreset.AMD_SPEED:
                args.append('speed')
        #aq&lf
        if psy is not None:
            if video_encoder == Encoder.NVIDIA_H264 or video_encoder == Encoder.NVIDIA_HEVC or video_encoder == Encoder.NVIDIA_AV1:
                args.append("-spatial-aq")
                args.append("1")
                args.append("-aq-strength")
                args.append(str(psy))
            elif video_encoder == Encoder.X264:
                args.append("-aq-mode")
                args.append("1")
                args.append("-aq-strength")
                args.append(str(psy))
            else:
                logger.critical("Psycho-visual is not supported for this encoder",tags="GenerateVideo:merge_sequences")
                raise ValueError("Psycho-visual is not supported for this encoder")
        if fc is not None:
            if video_encoder == Encoder.NVIDIA_H264 or video_encoder == Encoder.NVIDIA_HEVC or video_encoder == Encoder.NVIDIA_AV1:
                args.append("-rc-lookahead")
                args.append(str(fc))
            elif video_encoder == Encoder.X264:
                args.append("-lookahead")
                args.append(str(fc))
            else:
                logger.critical("Forward-compatibility is not supported for this encoder",tags="GenerateVideo:merge_sequences")
                raise ValueError("Forward-compatibility is not supported for this encoder")
        #tune
        if video_encoder != Encoder.AMD_H264 or Encoder.AMD_HEVC:
            if tune != FFmpegTune.NULL:
                args.append('-tune')
                if tune == FFmpegTune.X264_FILM:
                    args.append('film')
                elif tune == FFmpegTune.X264_ANIMATION:
                    args.append('animation')
                elif tune == FFmpegTune.X264_GRAIN:
                    args.append('grain')
                elif tune == FFmpegTune.X264_STILLIMAGE:
                    args.append('stillimage')
                elif tune == FFmpegTune.X264_FASTDECODE:
                    args.append('fastdecode')
                elif tune == FFmpegTune.X264_ZEROLANTENCY:
                    args.append('zerolatency')
                elif tune == FFmpegTune.NV_AV1_HQ or FFmpegTune.NV_AV1_SHQ or FFmpegTune.NV_H265_SHQ or FFmpegTune.NV_H264_HQ or FFmpegTune.NV_H265_HQ:
                    args.append('hq')
                elif tune == FFmpegTune.NV_AV1_LL or FFmpegTune.NV_H264_LL or FFmpegTune.NV_H265_LL:
                    args.append('ll')
                elif tune == FFmpegTune.NV_AV1_SLL or FFmpegTune.NV_H264_SLL or FFmpegTune.NV_H265_SLL:
                    args.append('ull')
        #2pass
        if two_pass and bitrate_control == BitRateControl.VBR and video_encoder == Encoder.NVIDIA_AV1 or video_encoder == Encoder.NVIDIA_H264 or video_encoder == Encoder.NVIDIA_HEVC:
            args.append("-multipass")
            args.append("fullres")

    #output
    args.append(output_file)

    logger.debug(f"FFmpeg command: {' '.join(args)}",tags="GenerateVideo:merge_sequences")
    # print(' '.join(args))
    if not debug:
        code = execute_command(args)
    else:
        code = 0
    return code


def setup_sequence(path):
    name_args = ""
    temp = str(str(os.listdir(path)[0]).split('.')[0]).split('_')[1]
    length = len(str(temp))
    name = str(str(os.listdir(path)[0]).split('.')[0]).split('_')[0] + "_%0{numlen}d.{prefix}".format(numlen=length,
                                                                                                      prefix=str(str(
                                                                                                          os.listdir(
                                                                                                              path)[
                                                                                                              0]).split(
                                                                                                          '.')[1]))
    logger.debug(f"sequence name: {name}",tags="GenerateVideo:merge_sequences")
    return name


def merge_video_sequnece(input_list, output_path,logger,audio_file,output_format):
    name = str(uuid.uuid4())
    args = []
    strings = ""
    for i in input_list:
        temp = f"file '{i}'\n"
        strings += temp
    if os.path.exists(f"{name}.txt"):
        os.remove(f"{name}.txt")
    with open(f"{name}.txt", 'w') as f:
        f.write(strings)

    args.append(ffmpeg_path)
    args.append('-f')
    args.append('concat')
    args.append('-safe')
    args.append('0')
    args.append('-i')
    args.append(f"{name}.txt")
    if audio_file is not None:
        for i in audio_file:
            args.append('-i')
            args.append(i)
    #mapping
    if audio_file is not None:
        args.append('-map')
        args.append('0:v:0')
        for i in range(len(audio_file)):
            args.append('-map')
            args.append(f'{i+1}:a:0')
    args.append('-map')
    args.append("0")
    args.append('-c')
    args.append('copy')
    # audio_encoder
    if audio_file is not None:
        if output_format == 'mov':
            for i in range(len(audio_file)):
                args.append('-c:a')
                args.append('aac')
        elif output_format == 'mp4' or output_format == 'mkv':
            for i in range(len(audio_file)):
                args.append(f'-c:a:{i}')
                args.append('copy')
        else:
            for i in range(len(audio_file)):
                args.append('-c:a')
                args.append('aac')
    args.append(output_path)
    logger.debug(f"FFmpeg command: {' '.join(args)}",tags="GenerateVideo:merge_sequences")
    code = execute_command(args)
    if os.path.exists(f"{name}.txt"):
        os.remove(f"{name}.txt")
    logger.debug(f"merge video sequence {name} success",tags="GenerateVideo:merge_sequences")
    return code


def get_video_parameters_simple(video_path: str) -> str:
    """
    获取简化的视频参数（只包含关键信息）

    Args:
        video_path: 视频文件路径

    Returns:
        包含关键视频参数的易读字符串
    """
    if not os.path.exists(video_path):
        return f"错误: 视频文件不存在: {video_path}"

    try:
        # 修复1：去掉路径的双引号，直接传递路径
        # 修复2：使用正确的命令格式处理包含空格和中文的路径
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', video_path  # 直接传递，不要加引号
        ]

        # 修复3：使用更安全的子进程调用方式
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        data = json.loads(result.stdout)

        # 获取基本信息
        file_size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)

        # 查找视频流
        video_stream = None
        audio_stream = None
        for stream in data.get('streams', []):
            if stream['codec_type'] == 'video':
                video_stream = stream
            elif stream['codec_type'] == 'audio':
                audio_stream = stream

        result_str = "视频关键参数:\n"
        result_str += f"    文件: {os.path.basename(video_path)}\n"
        result_str += f"    大小: {file_size_mb} MB\n"

        if video_stream:
            width = video_stream.get('width', '未知')
            height = video_stream.get('height', '未知')
            duration = round(float(video_stream.get('duration', 0)), 2)
            fps = video_stream.get('r', video_stream.get('avg_frame_rate', '未知'))

            result_str += f"    分辨率: {width}×{height}\n"
            result_str += f"    时长: {duration}秒\n"
            result_str += f"    帧率: {fps}\n"
            result_str += f"    编码: {video_stream.get('codec_name', '未知')}"

        return result_str

    except subprocess.CalledProcessError as e:
        # 尝试解码错误输出
        try:
            error_msg = e.stderr.decode('utf-8', errors='replace')
        except:
            error_msg = e.stderr.decode('gbk', errors='replace') if isinstance(e.stderr, bytes) else str(e.stderr)

        return f"ffprobe 执行失败: {e}\n错误输出: {error_msg}"

    except json.JSONDecodeError as e:
        return f"解析JSON数据失败: {e}"

    except Exception as e:
        return f"获取视频参数时出错: {e}"

def get_audio_parameters_simple(video_path: str) -> str:
    """
    获取简化的视频参数（只包含关键信息）

    Args:
        video_path: 视频文件路径

    Returns:
        包含关键视频参数的易读字符串
    """
    if not os.path.exists(video_path):
        return f"错误: 视频文件不存在: {video_path}"

    try:
        # 修复1：去掉路径的双引号，直接传递路径
        # 修复2：使用正确的命令格式处理包含空格和中文的路径
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', video_path  # 直接传递，不要加引号
        ]

        # 修复3：使用更安全的子进程调用方式
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        data = json.loads(result.stdout)

        # 获取基本信息
        file_size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)

        # 查找视频流
        video_stream = None
        audio_stream = None
        for stream in data.get('streams', []):
            if stream['codec_type'] == 'video':
                video_stream = stream
            elif stream['codec_type'] == 'audio':
                audio_stream = stream

        result_str = ""

        if audio_stream:
            result_str += f"    音频: {audio_stream.get('codec_name', '未知')} "
            result_str += f"    {audio_stream.get('sample_rate', '未知')}Hz "
            result_str += f"    {audio_stream.get('channels', '未知')}声道\n"

        return result_str

    except subprocess.CalledProcessError as e:
        # 尝试解码错误输出
        try:
            error_msg = e.stderr.decode('utf-8', errors='replace')
        except:
            error_msg = e.stderr.decode('gbk', errors='replace') if isinstance(e.stderr, bytes) else str(e.stderr)

        return f"ffprobe 执行失败: {e}\n错误输出: {error_msg}"

    except json.JSONDecodeError as e:
        return f"解析JSON数据失败: {e}"

    except Exception as e:
        return f"获取视频参数时出错: {e}"




if __name__ == '__main__':
    merge_video_sequnece(['1.mov','2.mov','3.mov'], 'output.mov', "logger", ['1.mp3', '2.mp3','3.mp3'], 'mov')
