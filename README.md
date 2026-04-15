# FileWarp

A Python file **conversion**, **manipulation**, and **analysis** toolkit.
This is a Linux command-line interface (CLI) utility that converts documents from one format to another, analyzes files, manipulates files, and more.

## Name Variations

```shell
filewarp -h
Filewarp -h
warp -h
```

## Installation

### Using pip

```shell
pip install filewarp
```

### Install from GitHub

```shell
pip install git+https://github.com/skye-cyber/FileWarp.git
```

## Usage

To run the CLI app, use the following command:

```shell
filewarp [OPTIONS] COMMAND [ARGS]...
```

Replace `[OPTIONS]` with global options and `COMMAND` with the specific operation you want to execute.

## Available Commands

| Command | Description |
|---------|-------------|
| `convert-doc` | Convert documents between formats (PDF, DOCX, etc.) |
| `convert-audio` | Convert audio files between formats (MP3, WAV, etc.) |
| `convert-video` | Convert video files between formats (MP4, MKV, etc.) |
| `convert-image` | Convert image files between formats (PNG, JPG, etc.) |
| `ocr` | Extract text from images using OCR |
| `pdf-join` | Join multiple PDF files |
| `extract-audio` | Extract audio from video files |
| `extract-pages` | Extract specific pages from PDF |
| `extract-images` | Extract images from PDF |
| `scan-pdf` | Scan PDF and extract text |
| `scan-as-image` | Scan PDF as images then extract text |
| `scan-long` | Scan document as long image (effective for complex layouts) |
| `pdf2long-image` | Convert PDF to long image |
| `doc-to-image` | Convert documents to images |
| `images-to-pdf` | Convert images to PDF |
| `images-to-word` | Convert images to Word document |
| `grayscale` | Convert images to grayscale |
| `resize-image` | Resize or compress images |
| `join-audio` | Join multiple audio files into one |
| `analyze-video` | Analyze video file properties |
| `edit-video` | Edit videos (trim, cut, etc.) |
| `convert-svg` | Convert SVG files to other formats |
| `html2word` | Convert HTML files to Word documents |
| `markdown2word` | Convert Markdown to Word with Mermaid rendering |
| `text2word` | Convert styled text to Word document |
| `record` | Record audio from microphone |
| `voice-type` | Use voice to type text |
| `audio-effects` | Apply audio effects and voice changes |

## Examples

### 1. Document Conversion

```shell
filewarp convert-doc example.docx --to pdf
```

**Supported Formats for Document Conversion:**
- PDF to (Word, TXT, Audio[TTS])
- PDF to TXT
- PDF to Audio (Ogg, MP3, WAV, etc.)
- DOCX to (PDF, PPTX/PPT, TXT, Audio)
- TXT to (PDF, Word, Audio)
- PPTX to DOCX
- XLSX to (SQL, CSV, TXT, Word)

This command converts `example.docx` to PDF. The output file retains the base name of the input file but uses the specified extension (`pdf`).

### 2. Audio Conversion

```shell
filewarp convert-audio example.mp3 --to wav
```

**Supported Audio Formats:**
- WAV, MP3, Ogg, FLV, OGV, AVI, MKV, MOV, WebM

### 3. Optical Character Recognition (OCR)

```shell
filewarp ocr image.jpg
```

Extracts text from the specified image.

### 4. Video Conversion

```shell
filewarp convert-video example.mp4 --to avi
```

**Supported Video Formats:**
- MP4, AVI, OGV, WebM, MOV, MKV, FLV, WMV

### 5. Image Conversion

```shell
filewarp convert-image example.png --to jpg
```

**Supported Image Formats:**
- JPEG: `.jpg`
- PNG: `.png`
- GIF: `.gif`
- BMP: `.bmp`
- TIFF: `.tiff`
- EXR: `.exr`
- PDF: `.pdf`
- WebP: `.webp`
- ICNS: `.icns`
- PSD: `.psd`
- SVG: `.svg`
- EPS: `.eps`

### 6. Join PDF Files

```shell
filewarp pdf-join file1.pdf file2.pdf
```

Joins multiple PDF files into a single PDF.

### 7. Extract Audio from Video

```shell
filewarp extract-audio video.mp4
```

Extracts audio from the specified video file.

### 8. Extract Pages from PDF

```shell
filewarp extract-pages document.pdf 1 3 5
```

Extracts pages 1, 3, and 5 from the PDF.

### 9. Convert Images to PDF

```shell
filewarp images-to-pdf image1.jpg image2.png
```

Converts multiple images into a single PDF.

### 10. Convert Images to Word

```shell
filewarp images-to-word image1.jpg image2.png
```

Converts multiple images into a Word document.

### 11. Convert to Grayscale

```shell
filewarp grayscale image.jpg
```

Converts the image to grayscale.

### 12. Resize Image

```shell
filewarp resize-image image.jpg --size 800x600
```

Resizes the image to the specified dimensions.

### 13. Join Audio Files

```shell
filewarp join-audio audio1.mp3 audio2.mp3
```

Joins multiple audio files into one.

### 14. Analyze Video

```shell
filewarp analyze-video video.mp4
```

Analyzes the video file properties.

### 15. Edit Video

```shell
filewarp edit-video video.mp4 --trim_start 10
```

Trims the first 10 seconds from the video.

### 16. Convert SVG

```shell
filewarp convert-svg image.svg --to png
```

Converts SVG to PNG.

### 17. HTML to Word

```shell
filewarp html2word document.html
```

Converts HTML to Word document.

### 18. Markdown to Word

```shell
filewarp markdown2word document.md
```

Converts Markdown to Word document.

### 19. Text to Word

```shell
filewarp text2word document.txt
```

Converts text to Word document.

### 20. Record Audio

```shell
filewarp record
```

Records audio from the microphone.

### 21. Voice Typing

```shell
filewarp voice-type
```

Uses voice to type text.

### 22. Audio Effects

```shell
filewarp audio-effects audio.mp3 --effect high
```

Applies audio effects to the file.

## Help

To see supported operations or input/output formats for a specific command, use:

```shell
filewarp COMMAND --help
```

For example:

```shell
filewarp convert-doc --help
```

This displays detailed help for the `convert-doc` command.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).
