from dataclasses import dataclass
from enum import Enum
from typing import Optional
from pathlib import Path


class VideoCodec(Enum):
    """Supported video codecs for encoding"""

    H264 = "libx264"
    H265 = "libx265"
    VP9 = "libvpx-vp9"
    COPY = "copy"  # Stream copy (no re-encoding)


class AudioCodec(Enum):
    """Supported audio codecs for encoding"""

    AAC = "aac"
    MP3 = "libmp3lame"
    COPY = "copy"  # Stream copy (no re-encoding)
    NONE = "none"  # Remove audio


class VideoQuality(Enum):
    """Preset quality settings"""

    ULTRA_FAST = "ultrafast"  # Fastest encoding, largest file
    FAST = "fast"
    MEDIUM = "medium"  # Default balance
    SLOW = "slow"  # Better compression, slower encoding
    VERYS_LOW = "veryslow"  # Best compression, very slow


@dataclass
class VideoInfo:
    """Container for video metadata"""

    path: Path
    duration: float
    width: int
    height: int
    fps: float
    codec: str
    bitrate: int
    audio_codec: Optional[str]
    audio_channels: Optional[int]
    file_size: int
    has_video: bool
    has_audio: bool


@dataclass
class TrimRange:
    """Represents a trim range in seconds"""

    start: float
    end: float

    def __post_init__(self):
        if self.start < 0:
            raise ValueError("Start time cannot be negative")
        if self.end <= self.start:
            raise ValueError("End time must be greater than start time")

    @property
    def duration(self) -> float:
        return self.end - self.start
