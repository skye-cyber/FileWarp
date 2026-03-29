# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy import VideoFileClip
# import os


def trim_moviepy(input_path, output_path, start, end):
    # This has progress bar support built-in
    clip = VideoFileClip(str(input_path))
    subclip = clip.subclipped(start, end)

    # Progress bar appears automatically
    subclip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        # verbose=True,  # Shows progress
        # logger=None,  # Or use 'bar' for tqdm style
    )
    clip.close()


if __name__ == "__main__":
    input_path = "/home/skye/Videos/Im.Nobody.S01E21.1080p.x264-[T4TSA.cc].mkv"
    output_path = "/home/skye/Videos/trimed.mkv"
    trim_moviepy(input_path, output_path, 166, 350)
