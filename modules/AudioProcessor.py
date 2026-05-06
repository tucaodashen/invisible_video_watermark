import os
import av
from BasicSystem.log_client import setup_logger, get_logger

setup_logger(default_tags="AudioProcessor", enable_udp=True, enable_console=True)
logger = get_logger()


def extract_audio_to_flac(video_path, output_audio_path,
                          audio_track=0, fps=None, bitrate=None):
    if fps is None:
        try:
            container = av.open(video_path)
            video_streams = [s for s in container.streams if s.type == 'video']
            if video_streams:
                vs = video_streams[0]
                fps = float(vs.average_rate)
                logger.debug(f"Identify video fps {fps}", tags=f"AudioProcessor:extract_audio_to_flac:{os.path.basename(video_path)}")
            else:
                fps = 30.0
                logger.warning(f"Can not identify video fps,use default fps {fps}", tags=f"AudioProcessor:extract_audio_to_flac:{os.path.basename(video_path)}")
            container.close()
        except Exception as e:
            fps = 30.0
            logger.warning(f"Occur error when extract audio to flac: {e}，use default fps {fps}", tags=f"AudioProcessor:extract_audio_to_flac:{os.path.basename(video_path)}")

    try:
        input_container = av.open(video_path)
        audio_streams = [s for s in input_container.streams if s.type == 'audio']

        if audio_track >= len(audio_streams):
            logger.warning(f"Audio track {audio_track} not found, total: {len(audio_streams)}",
                           tags=f"AudioProcessor:extract_audio_to_flac:{os.path.basename(video_path)}")
            input_container.close()
            return False

        audio_stream = audio_streams[audio_track]

        output_container = av.open(output_audio_path, 'w')
        audio_out = output_container.add_stream('flac', rate=44100)
        audio_out.codec_context.options['compression_level'] = '5'

        if bitrate:
            audio_out.codec_context.options['bit_rate'] = str(_parse_bitrate_for_audio(bitrate))

        for frame in input_container.decode(audio_stream):
            for packet in audio_out.encode(frame):
                output_container.mux(packet)
        for packet in audio_out.encode(None):
            output_container.mux(packet)

        output_container.close()
        input_container.close()

        logger.success(f"Success extract audio to flac: {output_audio_path}",
                       tags=f"AudioProcessor:extract_audio_to_flac:{os.path.basename(video_path)}")
        return True
    except Exception as e:
        logger.error(f"Extract audio to flac error: {e}",
                     tags=f"AudioProcessor:extract_audio_to_flac:{os.path.basename(video_path)}")
        return False


def _parse_bitrate_for_audio(bitrate):
    if isinstance(bitrate, str):
        bitrate_str = bitrate.upper().strip()
        if bitrate_str.endswith('M'):
            return int(float(bitrate_str[:-1]) * 1_000_000)
        elif bitrate_str.endswith('K'):
            return int(float(bitrate_str[:-1]) * 1_000)
        else:
            return int(bitrate_str)
    return int(bitrate)


def get_audio_tracks_info(video_path):
    text = []
    try:
        container = av.open(video_path)
        audio_streams = [stream for stream in container.streams if stream.type == 'audio']

        text.append("Found audio tracks:")
        for i, stream in enumerate(audio_streams):
            text.append(f"Track {i}:")
            text.append(f"  Decoder: {stream.codec_context.name if stream.codec_context else '未知'}")
            text.append(f"  Sample Rate: {stream.codec_context.sample_rate if stream.codec_context else '未知'} Hz")
            text.append(f"  Channels: {stream.codec_context.channels if stream.codec_context else '未知'}")
            text.append(f"  Language: {stream.metadata.get('language', '未知')}")
            text.append(f"  Title: {stream.metadata.get('title', '无标题')}")
            logger.debug(f"Audio track {i} details: {stream}",
                         tags=f"AudioProcessor:get_audio_tracks_info:{os.path.basename(video_path)}")

        container.close()
        return len(audio_streams)
    except Exception as e:
        logger.error(f"Error when get audio tracks info: {e}",
                     tags=f"AudioProcessor:get_audio_tracks_info:{os.path.basename(video_path)}")
        return 0
