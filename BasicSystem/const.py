from enum import Enum



__version__ = "0.0.1_Omicron"

COMPATIBLE_VERSIONS = ["0.0.1_Omicron"]

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

class FFmpegEncoder(Enum):
    X264 = 1
    NVIDIA_HEVC = 2
    NVIDIA_H264 = 3
    NVIDIA_AV1 = 4
    AMD_HW_H264 = 5
    AMD_HW_HEVC = 6
    Resolume_DXV = 7

class WatermarkAlgorithm(Enum):
    TEXT_GOUFEI = 1
    TEXT_RIVAGAN = 3
    TEXT_FREQM = 4
    IMAGE_FIREKEEPER = 5
    IMAGE_GUOFEI = 6

class SourceType(Enum):
    IMAGE = 0
    VIDEO = 1



