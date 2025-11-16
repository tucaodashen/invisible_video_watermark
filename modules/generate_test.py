from modules import GenerateVideo
from BasicSystem import const


GenerateVideo.merge_sequences(
    "",
    "",
    30,
    const.BitRateControl.VBR,
    "10M",
    "6M"
    ,const.Encoder.X264
    ,const.FFmpegTune.X264_FILM,
    const.FFmpegPreset.X264_PLACEBO,
    debug=True
)
# -ToDo: CPU编码器莫名错误记得解决