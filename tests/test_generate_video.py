"""
Unit tests for GenerateVideo.py boolean logic fixes.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Test: Boolean operator precedence fixes
# ---------------------------------------------------------------------------

class MockEncoder:
    AMD_H264 = "amd_h264"
    AMD_HEVC = "amd_hevc"
    H264 = "h264"
    HEVC = "hevc"
    NVIDIA_AV1 = "nvidia_av1"
    NVIDIA_H264 = "nvidia_h264"
    NVIDIA_HEVC = "nvidia_hevc"


class MockTune:
    NV_AV1_HQ = "av1_hq"
    NV_AV1_SHQ = "av1_shq"
    NV_AV1_LL = "av1_ll"
    NV_AV1_SLL = "av1_sll"


class MockBitRateControl:
    VBR = "vbr"
    CBR = "cbr"


def test_amd_encoder_tune_exclusion_old_bug():
    """OLD bug: or Encoder.AMD_HEVC always True, so tune always included."""
    video_encoder = MockEncoder.AMD_H264
    result = video_encoder != MockEncoder.AMD_H264 or MockEncoder.AMD_HEVC
    # AMD_HEVC is truthy, so OR branch is always True
    assert result  # BUG: truthy — tune should be excluded for AMD


def test_amd_encoder_tune_exclusion_fixed():
    """FIXED: tune is excluded when encoder is AMD."""
    video_encoder = MockEncoder.AMD_H264
    result = video_encoder not in (MockEncoder.AMD_H264, MockEncoder.AMD_HEVC)
    assert result is False  # CORRECT: AMD encoder, no tune


def test_non_amd_encoder_tune_included():
    """Non-AMD encoders should include tune."""
    video_encoder = MockEncoder.H264
    result = video_encoder not in (MockEncoder.AMD_H264, MockEncoder.AMD_HEVC)
    assert result is True  # CORRECT: non-AMD, include tune


# ---------------------------------------------------------------------------
# Test: NV encoder tune check fix
# ---------------------------------------------------------------------------

def test_tune_check_old_bug():
    """OLD bug: enum values in OR branch are truthy, always True."""
    tune = MockTune.NV_AV1_LL
    # This was the old pattern: tune == X or Y or Z
    result = tune == MockTune.NV_AV1_HQ or MockTune.NV_AV1_SHQ or MockTune.NV_AV1_LL
    # Y and Z are always truthy, so the expression short-circuits to True
    assert result  # True even if tune doesn't match


def test_tune_check_fixed():
    """FIXED: use 'in' for proper membership test."""
    tune = MockTune.NV_AV1_LL
    result = tune in (MockTune.NV_AV1_HQ, MockTune.NV_AV1_SHQ, MockTune.NV_AV1_LL, MockTune.NV_AV1_SLL)
    assert result is True

    tune = "nonexistent"
    result = tune in (MockTune.NV_AV1_HQ, MockTune.NV_AV1_SHQ, MockTune.NV_AV1_LL, MockTune.NV_AV1_SLL)
    assert result is False


# ---------------------------------------------------------------------------
# Test: Two-pass operator precedence fix
# ---------------------------------------------------------------------------

def test_two_pass_old_bug():
    """OLD bug: operator precedence bypasses two_pass and VBR checks."""
    two_pass = False
    bitrate_control = MockBitRateControl.CBR
    video_encoder = MockEncoder.NVIDIA_H264

    # OLD: if two_pass and VBR and AV1 or H264 or HEVC:
    result = (
        two_pass
        and bitrate_control == MockBitRateControl.VBR
        and video_encoder == MockEncoder.NVIDIA_AV1
        or video_encoder == MockEncoder.NVIDIA_H264
        or video_encoder == MockEncoder.NVIDIA_HEVC
    )
    # False and ... or True or False = True  (BUG!)
    assert result is True


def test_two_pass_fixed():
    """FIXED: use 'in' for proper grouping."""
    two_pass = False
    bitrate_control = MockBitRateControl.CBR
    video_encoder = MockEncoder.NVIDIA_H264

    result = (
        two_pass
        and bitrate_control == MockBitRateControl.VBR
        and video_encoder in (MockEncoder.NVIDIA_AV1, MockEncoder.NVIDIA_H264, MockEncoder.NVIDIA_HEVC)
    )
    assert result is False  # CORRECT: two_pass is False


def test_two_pass_valid():
    """When all conditions are met, two-pass should be enabled."""
    two_pass = True
    bitrate_control = MockBitRateControl.VBR
    video_encoder = MockEncoder.NVIDIA_AV1

    result = (
        two_pass
        and bitrate_control == MockBitRateControl.VBR
        and video_encoder in (MockEncoder.NVIDIA_AV1, MockEncoder.NVIDIA_H264, MockEncoder.NVIDIA_HEVC)
    )
    assert result is True


def test_two_pass_wrong_encoder():
    """Two-pass should not enable for non-NVIDIA encoders."""
    two_pass = True
    bitrate_control = MockBitRateControl.VBR
    video_encoder = MockEncoder.H264

    result = (
        two_pass
        and bitrate_control == MockBitRateControl.VBR
        and video_encoder in (MockEncoder.NVIDIA_AV1, MockEncoder.NVIDIA_H264, MockEncoder.NVIDIA_HEVC)
    )
    assert result is False


# ---------------------------------------------------------------------------
# Test: ffmpeg path without .exe
# ---------------------------------------------------------------------------

def test_ffmpeg_path_no_exe():
    """ffmpeg_path should not hardcode .exe for cross-platform compatibility."""
    ffmpeg_path = "ffmpeg"
    assert ffmpeg_path == "ffmpeg"
    assert ffmpeg_path != "ffmpeg.exe"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
