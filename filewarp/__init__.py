"""
....////////   ///  ///      /////////   ///////  //////    //////   ////////
   //         ///  ///      //          //    // //  //   //    // ///
  /////////  ///  ///      ////////    //     ///   //   //----//  //
 //         ///  //////// //_____     //           //   //    //   //////////

Converter document file(s) to different format ie pdf_to_docx.
    example filewarp --convert_doc example.docx -t pdf

Convert audio file(s) to and from different format ie mp3 to wav
        example filewarp --convert_audio example.mp3 -t wav

Convert video file(s) to and from different format ie mp4 to mkv.
        example filewarp --convert_video example.mp4 -t mkv

Convert image file(s) to and from different format ie png to jpg.
        example filewarp --convert_image example.jpg -t png

Extract audio from a video. example filewarp -xA example.mp4

Analyze a given video.
        example filewarp --analyze_video example.mp4

hange size of an image compress/decompress
        example filewarp --resize_image example.png -t_size 2mb -t png

Scan pdf file and extract text
                        example filewarp --scan example.pdf

Convert pdf file to long image
                        example filewarp --doc_long_image example.pdf

Scan [doc, docx, pdf]
        file and extract text,-> very effective
                    example filewarp --scanAsImg example.pdf

Extract text from an image.
        example filewarp --OCR image.png
"""

from audiobot.cli import cli as audiobot

from .core.image.core import (
    GrayscaleConverter,
    ImageCompressor,
    ImageConverter,
    ImageDocxConverter,
    ImagePdfConverter,
)
from .core.pdf.core import PageExtractor, PDF2LongImageConverter, PDFCombine
from .core.recorder import SoundRecorder
from .core.video.core import VideoConverter

# from .cli.main import CliInit as main, OperationMapper
from .cli.cli import main
from .cli.converter import DocConverter
from voice.VoiceType import VoiceTypeEngine


__version__ = "2.1.2"

__all__ = [
    "audiobot",
    "GrayscaleConverter",
    "ImageConverter",
    "ImageCompressor",
    "PDF2LongImageConverter",
    "ImagePdfConverter",
    "ImageDocxConverter",
    "PDFCombine",
    "PageExtractor",
    "VideoConverter",
    "SoundRecorder",
    "DocConverter",
    # "OperationMapper",
    "VoiceTypeEngine",
    "main",
]
