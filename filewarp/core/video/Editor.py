import subprocess
import tempfile
import json
import re
import shutil
from pathlib import Path
from typing import Union, List, Tuple, Optional

# from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from tqdm import tqdm
from .models import VideoCodec, AudioCodec, VideoQuality, VideoInfo, TrimRange
from ...utils.logging_utils import logger


class VideoEditor:
    """
    Optimized video editor with progress tracking and frame-accurate seeking.
    """

    def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
        self._temp_dir = Path(tempfile.mkdtemp(prefix="video_editor_"))
        self._check_ffmpeg()

        # Thread lock for progress bar safety if using ThreadPoolExecutor
        self._progress_lock = Lock()

    def _check_ffmpeg(self):
        """Verify FFmpeg and FFprobe are accessible"""
        try:
            subprocess.run(
                [self.ffmpeg_path, "-version"], capture_output=True, check=True
            )
            subprocess.run(
                [self.ffprobe_path, "-version"], capture_output=True, check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(
                "FFmpeg/FFprobe not found. Please install FFmpeg and ensure it's in PATH."
            ) from e

    def get_video_info(self, video_path: Union[str, Path]) -> VideoInfo:
        """Extract comprehensive video information using ffprobe."""
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        cmd = [
            self.ffprobe_path,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        duration = float(data.get("format", {}).get("duration", 0))
        file_size = int(data.get("format", {}).get("size", 0))

        video_stream = None
        audio_stream = None

        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video" and not video_stream:
                video_stream = stream
            elif stream.get("codec_type") == "audio" and not audio_stream:
                audio_stream = stream

        width = height = 0
        fps = 0
        video_codec = ""
        bitrate = 0

        if video_stream:
            width = int(video_stream.get("width", 0))
            height = int(video_stream.get("height", 0))

            avg_frame_rate = video_stream.get("avg_frame_rate", "0/0").split("/")
            if len(avg_frame_rate) == 2 and float(avg_frame_rate[1]) != 0:
                fps = float(avg_frame_rate[0]) / float(avg_frame_rate[1])

            video_codec = video_stream.get("codec_name", "")
            bitrate = int(video_stream.get("bit_rate", 0))

        audio_codec = None
        audio_channels = None
        if audio_stream:
            audio_codec = audio_stream.get("codec_name", "")
            audio_channels = int(audio_stream.get("channels", 0))

        return VideoInfo(
            path=video_path,
            duration=duration,
            width=width,
            height=height,
            fps=fps,
            codec=video_codec,
            bitrate=bitrate,
            audio_codec=audio_codec,
            audio_channels=audio_channels,
            file_size=file_size,
            has_video=video_stream is not None,
            has_audio=audio_stream is not None,
        )

    def trim_video(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        trim_ranges: Union[
            TrimRange, List[TrimRange], Tuple[float, float], List[Tuple[float, float]]
        ],
        video_codec: VideoCodec = VideoCodec.H264,
        audio_codec: AudioCodec = AudioCodec.AAC,
        quality: VideoQuality = VideoQuality.MEDIUM,
        crf: Optional[int] = None,
        preserve_audio: bool = True,
        copy_streams: bool = False,
        show_progress: bool = True,
        seek_buffer: float = 5.0,  # Seconds before target for accurate seeking
    ) -> Path:
        """
        Trim video with progress tracking and frame-accurate seeking.

        Args:
            seek_buffer: Seconds to seek before target for accurate keyframe alignment (default 5s)
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        ranges = self._normalize_trim_ranges(trim_ranges)
        self._validate_trim_ranges(input_path, ranges)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if len(ranges) == 1:
            return self._trim_single_range(
                input_path,
                output_path,
                ranges[0],
                video_codec,
                audio_codec,
                quality,
                crf,
                preserve_audio,
                copy_streams,
                show_progress,
                seek_buffer,
            )
        else:
            return self._trim_multiple_ranges(
                input_path,
                output_path,
                ranges,
                video_codec,
                audio_codec,
                quality,
                crf,
                preserve_audio,
                copy_streams,
                show_progress,
                seek_buffer,
            )

    def _build_ffmpeg_command(
        self,
        input_path: Path,
        output_path: Path,
        trim_range: Optional[TrimRange] = None,
        video_codec: VideoCodec = VideoCodec.H264,
        audio_codec: AudioCodec = AudioCodec.AAC,
        quality: VideoQuality = VideoQuality.MEDIUM,
        crf: Optional[int] = None,
        preserve_audio: bool = True,
        copy_streams: bool = False,
        seek_buffer: float = 5.0,
    ) -> List[str]:
        """
        Build optimized FFmpeg command using double -ss technique:
        1. Fast seek to keyframe before target (input seeking)
        2. Accurate seek to exact frame (output seeking)
        3. Timestamp correction to prevent frozen frames
        """
        cmd = [self.ffmpeg_path, "-hide_banner", "-y"]

        # Input seeking (fast, inaccurate to keyframe)
        if trim_range and trim_range.start > 0:
            # Seek to buffer seconds before target to ensure we hit a keyframe
            seek_pos = max(0, trim_range.start - seek_buffer)
            cmd.extend(["-ss", str(seek_pos)])

        cmd.extend(["-i", str(input_path)])

        # Output seeking (accurate, from keyframe to exact frame)
        if trim_range:
            if trim_range.start > 0:
                # Skip the buffer we added earlier
                cmd.extend(["-ss", str(seek_buffer)])

            # Duration of actual content to extract
            cmd.extend(["-t", str(trim_range.duration)])

        # Video encoding options
        if copy_streams:
            cmd.extend(["-c:v", "copy"])
            # CRITICAL: Fix timestamp gaps when copying streams
            cmd.extend(
                ["-avoid_negative_ts", "make_zero", "-fflags", "+genpts", "-async", "1"]
            )
        else:
            quality_value = quality if isinstance(quality, str) else quality.value
            cmd.extend(
                [
                    "-c:v",
                    video_codec.value,
                    "-preset",
                    quality_value,
                    "-pix_fmt",
                    "yuv420p",  # Ensure compatibility
                ]
            )

            if crf:
                cmd.extend(["-crf", str(crf)])
            elif video_codec == VideoCodec.H264:
                cmd.extend(["-crf", "23"])

        # Audio encoding options
        if preserve_audio and audio_codec != AudioCodec.NONE:
            if copy_streams:
                cmd.extend(["-c:a", "copy"])
            else:
                cmd.extend(["-c:a", audio_codec.value])
        else:
            cmd.extend(["-an"])

        # Additional flags to prevent "long video with short content" bug
        if copy_streams:
            cmd.extend(["-vsync", "cfr"])  # Constant frame rate to fix timing

        cmd.extend([str(output_path)])
        return cmd

    def _parse_ffmpeg_time(self, line: str) -> Optional[float]:
        """Parse time from FFmpeg stderr output (format: time=00:01:23.45)"""
        match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
        if match:
            hours, minutes, seconds = map(float, match.groups())
            return hours * 3600 + minutes * 60 + seconds
        return None

    def _trim_single_range(
        self,
        input_path: Path,
        output_path: Path,
        trim_range: TrimRange,
        video_codec: VideoCodec,
        audio_codec: AudioCodec,
        quality: VideoQuality,
        crf: Optional[int],
        preserve_audio: bool,
        copy_streams: bool,
        show_progress: bool,
        seek_buffer: float,
    ) -> Path:
        """Process single trim range with progress tracking."""

        cmd = self._build_ffmpeg_command(
            input_path,
            output_path,
            trim_range,
            video_codec,
            audio_codec,
            quality,
            crf,
            preserve_audio,
            copy_streams,
            seek_buffer,
        )

        logger.debug(f"FFmpeg command: {' '.join(cmd)}")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # FFmpeg outputs to stderr, capture both
                universal_newlines=True,
                bufsize=1,
            )

            if show_progress:
                # Create progress bar
                pbar = tqdm(
                    total=int(trim_range.duration),
                    desc=f"Trimming {input_path.name[:20]}",
                    unit="s",
                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}s [{elapsed}<{remaining}]",
                )

                last_update = 0

                for line in process.stdout:
                    current_time = self._parse_ffmpeg_time(line)
                    if current_time is not None:
                        # Update progress (cap at duration)
                        progress = min(int(current_time), int(trim_range.duration))
                        if progress > last_update:
                            pbar.update(progress - last_update)
                            last_update = progress

                pbar.close()
            else:
                # Just wait for completion without progress
                process.communicate()

            return_code = process.wait()

            if return_code != 0:
                raise RuntimeError(f"FFmpeg exited with code {return_code}")

            # Verify output file exists and has size
            if not output_path.exists() or output_path.stat().st_size == 0:
                raise RuntimeError("Output file is empty or was not created")

        except Exception as e:
            # Clean up partial output on failure
            if output_path.exists():
                try:
                    output_path.unlink()
                except:
                    pass
            raise RuntimeError(f"Failed to trim video: {e}") from e

        return output_path

    def _trim_multiple_ranges(
        self,
        input_path: Path,
        output_path: Path,
        ranges: List[TrimRange],
        video_codec: VideoCodec,
        audio_codec: AudioCodec,
        quality: VideoQuality,
        crf: Optional[int],
        preserve_audio: bool,
        copy_streams: bool,
        show_progress: bool,
        seek_buffer: float,
    ) -> Path:
        """Extract multiple ranges and concatenate with progress tracking."""
        temp_files = []
        concat_file = None

        try:
            # Process segments sequentially (FFmpeg isn't thread-safe for encoding)
            total_duration = sum(r.duration for r in ranges)

            with tqdm(
                total=int(total_duration), desc="Total Progress", unit="s"
            ) as main_pbar:
                for i, trim_range in enumerate(ranges):
                    temp_file = self._temp_dir / f"segment_{i:03d}.mp4"
                    temp_files.append(temp_file)

                    # Process segment
                    self._trim_single_range(
                        input_path,
                        temp_file,
                        trim_range,
                        video_codec,
                        audio_codec,
                        quality,
                        crf,
                        preserve_audio,
                        copy_streams,
                        False,
                        seek_buffer,  # Disable individual progress
                    )

                    # Update main progress
                    main_pbar.update(int(trim_range.duration))

            # Create concat list
            concat_file = self._temp_dir / "concat.txt"
            with open(concat_file, "w") as f:
                for temp_file in temp_files:
                    # Escape single quotes in path for FFmpeg concat demuxer
                    path_str = str(temp_file.absolute()).replace("'", "'\\''")
                    f.write(f"file '{path_str}'\n")

            # Concatenate with progress
            concat_cmd = [
                self.ffmpeg_path,
                "-hide_banner",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                "-avoid_negative_ts",
                "make_zero",
                str(output_path),
            ]

            logger.debug(f"Concat command: {' '.join(concat_cmd)}")

            result = subprocess.run(
                concat_cmd, capture_output=True, text=True, check=True
            )

        except Exception as e:
            if output_path.exists():
                output_path.unlink()
            raise RuntimeError(f"Failed to concatenate segments: {e}") from e

        finally:
            # Cleanup temp files
            for temp_file in temp_files:
                if temp_file.exists():
                    temp_file.unlink()
            if concat_file and concat_file.exists():
                concat_file.unlink()

        return output_path

    def _normalize_trim_ranges(self, ranges):
        """Normalize various input formats to list of TrimRange objects."""
        if isinstance(ranges, TrimRange):
            return [ranges]
        elif isinstance(ranges, tuple) and len(ranges) == 2:
            return [TrimRange(ranges[0], ranges[1])]
        elif isinstance(ranges, list):
            normalized = []
            for r in ranges:
                if isinstance(r, TrimRange):
                    normalized.append(r)
                elif isinstance(r, tuple) and len(r) == 2:
                    normalized.append(TrimRange(r[0], r[1]))
                else:
                    raise ValueError(f"Invalid trim range format: {r}")
            return normalized
        else:
            raise ValueError(f"Invalid trim ranges format: {ranges}")

    def _validate_trim_ranges(self, input_path: Path, ranges: List[TrimRange]):
        """Validate trim ranges against video duration."""
        video_info = self.get_video_info(input_path)

        for i, trim_range in enumerate(ranges):
            if trim_range.start < 0:
                raise ValueError(f"Trim range {i}: start time cannot be negative")
            if trim_range.start >= video_info.duration:
                raise ValueError(
                    f"Trim range {i}: start time {trim_range.start}s "
                    f"exceeds video duration {video_info.duration}s"
                )
            if trim_range.end > video_info.duration:
                logger.warning(
                    f"Trim range {i}: end time {trim_range.end}s "
                    f"exceeds video duration {video_info.duration}s. "
                    f"Truncating to video end."
                )
                trim_range.end = video_info.duration
            if trim_range.end <= trim_range.start:
                raise ValueError(
                    f"Trim range {i}: end time must be greater than start time"
                )

    def batch_trim(
        self,
        video_paths: List[Union[str, Path]],
        output_dir: Union[str, Path],
        trim_specs: Union[TrimRange, List[TrimRange], dict],
        **kwargs,
    ) -> List[Path]:
        """Batch trim with global progress tracking."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_paths = []

        for video_path in tqdm(video_paths, desc="Processing videos", unit="file"):
            video_path = Path(video_path)

            if isinstance(trim_specs, dict):
                trim_spec = trim_specs.get(str(video_path), trim_specs.get(video_path))
                if trim_spec is None:
                    raise ValueError(f"No trim specification for video: {video_path}")
            else:
                trim_spec = trim_specs

            stem = video_path.stem
            output_path = output_dir / f"{stem}_trimmed{video_path.suffix}"

            try:
                result = self.trim_video(
                    video_path, output_path, trim_spec, show_progress=True, **kwargs
                )
                output_paths.append(result)
            except Exception as e:
                logger.error(f"Failed to process {video_path.name}: {e}")
                raise

        return output_paths

    def __del__(self):
        """Cleanup temporary directory on object destruction."""
        try:
            if (
                hasattr(self, "_temp_dir")
                and self._temp_dir
                and self._temp_dir.exists()
            ):
                shutil.rmtree(self._temp_dir, ignore_errors=True)
        except Exception as e:
            logger.warning(f"Failed to clean up temp directory: {e}")
