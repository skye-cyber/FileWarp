import subprocess
import os
import tempfile
import json
from pathlib import Path
from typing import Union, List, Tuple, Optional, Dict
import logging
from concurrent.futures import ThreadPoolExecutor
import shutil
from models import VideoCodec, AudioCodec, VideoQuality, VideoInfo, TrimRange

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoEditor:
    """
    Advanced video manipulation class with efficient trimming capabilities.

    Features:
    - Memory-efficient processing using FFmpeg streaming
    - CPU-efficient with smart encoding presets
    - Multiple trim operations support
    - Thread-based parallel processing for batch operations
    - Comprehensive error handling and logging
    """

    def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
        """
        Initialize video editor with FFmpeg paths.

        Args:
            ffmpeg_path: Path to ffmpeg executable
            ffprobe_path: Path to ffprobe executable
        """
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
        self._temp_dir = tempfile.mkdtemp(prefix="video_editor_")

        # Verify FFmpeg is available
        self._check_ffmpeg()

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
        """
        Extract comprehensive video information using ffprobe.

        Args:
            video_path: Path to video file

        Returns:
            VideoInfo object containing video metadata
        """
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

        # Initialize default values
        duration = float(data.get("format", {}).get("duration", 0))
        file_size = int(data.get("format", {}).get("size", 0))

        video_stream = None
        audio_stream = None

        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video" and not video_stream:
                video_stream = stream
            elif stream.get("codec_type") == "audio" and not audio_stream:
                audio_stream = stream

        # Parse video stream info
        width = height = 0
        fps = 0
        video_codec = ""
        bitrate = 0

        if video_stream:
            width = int(video_stream.get("width", 0))
            height = int(video_stream.get("height", 0))

            # Calculate FPS
            avg_frame_rate = video_stream.get("avg_frame_rate", "0/0").split("/")
            if len(avg_frame_rate) == 2 and float(avg_frame_rate[1]) != 0:
                fps = float(avg_frame_rate[0]) / float(avg_frame_rate[1])

            video_codec = video_stream.get("codec_name", "")
            bitrate = int(video_stream.get("bit_rate", 0))

        # Parse audio stream info
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
        fast_seek: bool = True,
        copy_streams: bool = False,
    ) -> Path:
        """
        Trim video with optimal performance and memory usage.

        Args:
            input_path: Source video path
            output_path: Output video path
            trim_ranges: Single trim range or list of ranges to extract
            video_codec: Video codec to use
            audio_codec: Audio codec to use
            quality: Encoding quality preset
            crf: Constant Rate Factor (18-28 for good quality)
            preserve_audio: Whether to keep audio
            fast_seek: Use fast seeking for better performance
            copy_streams: Copy streams without re-encoding (faster, less accurate)

        Returns:
            Path to output file
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        # Normalize trim ranges
        ranges = self._normalize_trim_ranges(trim_ranges)

        # Validate trim ranges
        self._validate_trim_ranges(input_path, ranges)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if len(ranges) == 1:
            # Single trim - direct processing
            return self._trim_single_range(
                input_path,
                output_path,
                ranges[0],
                video_codec,
                audio_codec,
                quality,
                crf,
                preserve_audio,
                fast_seek,
                copy_streams,
            )
        else:
            # Multiple ranges - concatenate
            return self._trim_multiple_ranges(
                input_path,
                output_path,
                ranges,
                video_codec,
                audio_codec,
                quality,
                crf,
                preserve_audio,
                fast_seek,
                copy_streams,
            )

    def trim_start(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        start_time: float,
        **kwargs,
    ) -> Path:
        """Trim from start_time to end of video"""
        video_info = self.get_video_info(input_path)
        return self.trim_video(
            input_path, output_path, (start_time, video_info.duration), **kwargs
        )

    def trim_end(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        end_time: float,
        **kwargs,
    ) -> Path:
        """Trim from beginning to end_time"""
        return self.trim_video(input_path, output_path, (0, end_time), **kwargs)

    def trim_start_end(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        start_time: float,
        end_time: float,
        **kwargs,
    ) -> Path:
        """Trim both start and end"""
        return self.trim_video(
            input_path, output_path, (start_time, end_time), **kwargs
        )

    def _normalize_trim_ranges(self, ranges) -> List[TrimRange]:
        """Normalize various input formats to list of TrimRange objects"""
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
        """Validate trim ranges against video duration"""
        video_info = self.get_video_info(input_path)

        for i, trim_range in enumerate(ranges):
            if trim_range.start > video_info.duration:
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
        fast_seek: bool = True,
        copy_streams: bool = False,
    ) -> List[str]:
        """
        Build optimized FFmpeg command for video processing.

        The command is optimized for:
        - Memory efficiency (streaming processing)
        - CPU efficiency (appropriate encoding presets)
        - Fast seeking when applicable
        """
        cmd = [self.ffmpeg_path, "-y"]  # Overwrite output

        # Add fast seeking if enabled and trim range provided
        if fast_seek and trim_range and trim_range.start > 0:
            cmd.extend(["-ss", str(trim_range.start)])

        cmd.extend(["-i", str(input_path)])

        # Add accurate seeking if not using fast seek
        if not fast_seek and trim_range and trim_range.start > 0:
            cmd.extend(["-ss", str(trim_range.start)])

        # Add trim end time
        if trim_range:
            cmd.extend(["-t", str(trim_range.duration)])

        # Video encoding options
        if copy_streams:
            cmd.extend(["-c:v", "copy"])
        else:
            cmd.extend(["-c:v", video_codec.value, "-preset", quality.value])

            # Set CRF if provided
            if crf:
                cmd.extend(["-crf", str(crf)])
            elif video_codec == VideoCodec.H264:
                cmd.extend(["-crf", "23"])  # Default good quality

        # Audio encoding options
        if preserve_audio and audio_codec != AudioCodec.NONE:
            if copy_streams:
                cmd.extend(["-c:a", "copy"])
            else:
                cmd.extend(["-c:a", audio_codec.value])
        else:
            cmd.extend(["-an"])  # No audio

        # Additional optimizations for fast seeking
        if fast_seek and trim_range and trim_range.start > 0:
            # Use copyts to preserve timestamps for accurate seeking
            cmd.extend(["-copyts"])

        # Add output path
        cmd.extend([str(output_path)])

        return cmd

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
        fast_seek: bool,
        copy_streams: bool,
    ) -> Path:
        """Process a single trim range"""

        cmd = self._build_ffmpeg_command(
            input_path,
            output_path,
            trim_range,
            video_codec,
            audio_codec,
            quality,
            crf,
            preserve_audio,
            fast_seek,
            copy_streams,
        )

        logger.info(f"Trimming video: {input_path.name} -> {output_path.name}")
        logger.debug(f"FFmpeg command: {' '.join(cmd)}")

        try:
            # Run FFmpeg with real-time output for progress monitoring
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # Monitor progress (optional - can be expanded)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"FFmpeg error: {stderr}")

        except Exception as e:
            if output_path.exists():
                output_path.unlink()  # Clean up partial output
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
        fast_seek: bool,
        copy_streams: bool,
    ) -> Path:
        """
        Extract multiple trim ranges and concatenate them.

        This method is memory-efficient as it processes one range at a time
        and uses FFmpeg's concat demuxer for concatenation.
        """
        temp_files = []

        try:
            # Process each range to temporary files
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = []

                for i, trim_range in enumerate(ranges):
                    temp_file = Path(self._temp_dir) / f"segment_{i:03d}.mp4"
                    temp_files.append(temp_file)

                    future = executor.submit(
                        self._trim_single_range,
                        input_path,
                        temp_file,
                        trim_range,
                        video_codec,
                        audio_codec,
                        quality,
                        crf,
                        preserve_audio,
                        fast_seek,
                        copy_streams,
                    )
                    futures.append(future)

                # Wait for all segments to complete
                for future in futures:
                    future.result()

            # Create concat file
            concat_file = Path(self._temp_dir) / "concat.txt"
            with open(concat_file, "w") as f:
                for temp_file in temp_files:
                    f.write(f"file '{temp_file.absolute()}'\n")

            # Concatenate segments
            concat_cmd = [
                self.ffmpeg_path,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",  # Copy streams (no re-encoding)
                str(output_path),
            ]

            logger.info(f"Concatenating {len(temp_files)} segments...")

            result = subprocess.run(concat_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to concatenate segments: {result.stderr}")

        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                if temp_file.exists():
                    temp_file.unlink()

            # Clean up concat file
            concat_file = Path(self._temp_dir) / "concat.txt"
            if concat_file.exists():
                concat_file.unlink()

        return output_path

    def batch_trim(
        self,
        video_paths: List[Union[str, Path]],
        output_dir: Union[str, Path],
        trim_specs: Union[TrimRange, List[TrimRange], Dict],
        **kwargs,
    ) -> List[Path]:
        """
        Batch trim multiple videos with optional different trim specs per video.

        Args:
            video_paths: List of input video paths
            output_dir: Directory for output files
            trim_specs: Either a single trim spec for all videos, or a dictionary
                       mapping input paths to their trim specs
            **kwargs: Additional arguments passed to trim_video

        Returns:
            List of output paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_paths = []

        for video_path in video_paths:
            video_path = Path(video_path)

            # Determine trim spec for this video
            if isinstance(trim_specs, dict):
                trim_spec = trim_specs.get(str(video_path), trim_specs.get(video_path))
                if trim_spec is None:
                    raise ValueError(f"No trim specification for video: {video_path}")
            else:
                trim_spec = trim_specs

            # Generate output filename
            stem = video_path.stem
            output_path = output_dir / f"{stem}_trimmed{video_path.suffix}"

            # Trim video
            result = self.trim_video(video_path, output_path, trim_spec, **kwargs)
            output_paths.append(result)

            logger.info(f"Processed: {video_path.name} -> {result.name}")

        return output_paths

    def __del__(self):
        """Cleanup temporary directory on object destruction"""
        if hasattr(self, "_temp_dir") and os.path.exists(self._temp_dir):
            try:
                shutil.rmtree(self._temp_dir)
            except Exception as e:
                logger.warning(f"Failed to clean up temp directory: {e}")


# Example usage and demonstration
if __name__ == "__main__":
    # Initialize the editor
    editor = VideoEditor()

    # Example 1: Basic trimming
    print("=== Basic Trimming Examples ===")

    # Trim from start (remove first 10 seconds)
    # editor.trim_start("input.mp4", "output_start.mp4", 10)

    # Trim from end (keep only first 30 seconds)
    # editor.trim_end("input.mp4", "output_end.mp4", 30)

    # Trim both start and end (extract segment from 10s to 30s)
    # editor.trim_start_end("input.mp4", "output_segment.mp4", 10, 30)

    # Example 2: Multiple trim ranges
    print("\n=== Multiple Trim Ranges ===")
    ranges = [
        (0, 30),  # First 30 seconds
        (60, 90),  # 60s to 90s
        (120, 150),  # 120s to 150s
    ]

    # This will extract these three segments and concatenate them
    # editor.trim_video("input.mp4", "output_compilation.mp4", ranges)

    # Example 3: Batch processing
    print("\n=== Batch Processing ===")
    videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

    # Same trim for all videos
    # editor.batch_trim(videos, "trimmed_videos", (10, 60))

    # Different trims per video
    trim_specs = {
        "video1.mp4": (0, 30),
        "video2.mp4": (15, 45),
        "video3.mp4": [(0, 20), (40, 60)],  # Multiple segments
    }
    # editor.batch_trim(videos, "custom_trims", trim_specs)

    # Example 4: Get video information
    print("\n=== Video Information ===")
    # info = editor.get_video_info("input.mp4")
    # print(f"Duration: {info.duration}s")
    # print(f"Resolution: {info.width}x{info.height}")
    # print(f"FPS: {info.fps}")
    # print(f"Codec: {info.codec}")
    # print(f"Has Audio: {info.has_audio}")

    print("\nVideoEditor class loaded successfully!")
    print(
        "Note: Examples are commented out. Uncomment with actual video files to test."
    )
