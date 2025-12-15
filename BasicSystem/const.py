from enum import Enum



__version__ = "v0.1.0_Omicron"

COMPATIBLE_VERSIONS = ["v0.1.0_Omicron"]

owner = "tucaodashen"
name = "invisible_video_watermark"


class File_Return_Type(Enum):
    PATH = 0
    ATTRIBUTE = 1

class OutputFormat(Enum):
    JPG = 1
    PNG = 2
    BMP = 3
    MP4 = 4
    AVI = 5

class ProcessMode(Enum):
    SingleFileSingleThread = 1
    SingleFileMultiThread = 2
    MultiFileSingleThread = 3
    MultiFileMultiThread = 4

class Encoder(Enum):
    NVIDIA_H264 = 1
    NVIDIA_HEVC = 2
    NVIDIA_AV1 = 3
    AMD_H264 = 4
    AMD_HEVC = 5
    X264 = 6
    Resolume_DXV = 7

class BitRateControl(Enum):
    CBR = 1
    VBR = 2
    CQVBR = 3
    CQP = 4

class FFmpegTune(Enum):
    NV_H264_HQ = 1
    NV_H264_LL = 2
    NV_H264_SLL = 3
    NV_H265_SHQ = 4
    NV_H265_HQ = 5
    NV_H265_LL = 6
    NV_H265_SLL = 7
    NV_AV1_SHQ = 8
    NV_AV1_HQ = 9
    NV_AV1_LL = 10
    NV_AV1_SLL = 11
    X264_FILM = 12
    X264_ANIMATION = 13
    X264_GRAIN = 14
    X264_STILLIMAGE = 15
    X264_PSNR = 16
    X264_SSIM = 17
    X264_FASTDECODE = 18
    X264_ZEROLANTENCY = 19
    NULL = 20


class FFmpegPreset(Enum):
    NVIDIA_P1 = 1
    NVIDIA_P2 = 2
    NVIDIA_P3 = 3
    NVIDIA_P4 = 4
    NVIDIA_P5 = 5
    NVIDIA_P6 = 6
    NVIDIA_P7 = 7
    AMD_QUALITY = 8
    AMD_BALANCE = 9
    AMD_SPEED = 10
    X264_SUPERFAST = 11
    X264_VERYFAST = 12
    X264_FASTER = 13
    X264_FAST = 14
    X264_MEDIUM = 15
    X264_SLOW = 16
    X264_SLOWER = 17
    X264_VERYSLOW = 18
    X264_PLACEBO = 19
    X264_UlTRAFAST = 20


class WatermarkAlgorithm(Enum):
    TEXT_GOUFEI = 1
    TEXT_RIVAGAN = 3
    TEXT_FREQM = 4
    IMAGE_FIREKEEPER = 5
    IMAGE_GUOFEI = 6

class SourceType(Enum):
    IMAGE = 0
    VIDEO = 1

class SamplerType(Enum):
    RANDOM = 0
    FULL = 1
    AVERAGE = 2
    PSY = 3
    MANUAL = 4

process_unit_template = {
    "version":__version__,
    "file":None,
    "watermark_method":None,
    "attachment_data":None,
    "output_name":None,
    "output_path":None,
    "slice_length":None,
    "sample_times":None,
    "sample_extend":None,
    "process_limit":None,
    "sample_type":None,
    "manual_sample_sheet":None,
    "watermark_content":None,
    "BitRateControl":None,
    "MaximumBitRate":None,
    "TargetBitRate":None,
    "FFmpegEncoder":None,
    "FFmpegTune":None,
    "FFmpegPresent":None,
    "FFmpegForeward":None,
    "FFmpegSelfAdaptive":None,
    "output_format":None,
    "two_pass":None,
}

rollbar_token = "758277cc22ea4655b27f5cfbce61c7b51b3fe548b91539cd99784ed5995ec6622595257bc724b3cefff6dd36a3f4daa1"



