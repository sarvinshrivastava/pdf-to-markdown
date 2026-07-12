# PDF to Markdown Converter

A powerful command-line tool that converts PDF files to well-structured Markdown format using [surya-ocr](https://github.com/datalab-to/surya). This converter preserves document structure, extracts text with high accuracy, recognizes tables, maintains reading order, and extracts images.

## Features

- **High-Quality OCR**: Uses surya-ocr for text recognition in 90+ languages
- **Layout Analysis**: Detects and preserves document structure (titles, paragraphs, lists, tables, images)
- **Reading Order**: Maintains proper reading order across multi-column layouts
- **Table Recognition**: Converts tables to Markdown table format
- **Image Extraction**: Extracts images from PDFs and includes references in Markdown
- **Multi-language Support**: Auto-detects or specifies languages for OCR

## Installation

### Prerequisites

1. **Python 3.10 or higher** (required for surya-ocr)
   - Check your Python version: `python3 --version`
   - If you have Python 3.9 or lower, you'll need to install Python 3.10+:
     - **macOS**: `brew install python@3.10` or `brew install python@3.11`
     - **Linux**: Use your package manager or install from python.org
     - **Windows**: Download from python.org
   - After installing, use the correct Python: `python3.10` or `python3.11` instead of `python3`

2. **System Dependencies**:
   - **macOS**: Install poppler via Homebrew
     ```bash
     brew install poppler
     ```
   - **Ubuntu/Debian**: Install poppler-utils
     ```bash
     sudo apt-get install poppler-utils
     ```
   - **Windows**: Download poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/) and add to PATH

3. **PyTorch**: Install PyTorch appropriate for your system from [pytorch.org](https://pytorch.org/get-started/locally/)

### Install Python Dependencies

**Recommended: Use a Virtual Environment**

We recommend using a virtual environment to avoid conflicts with system Python packages.

**Quick Setup (Automated):**
```bash
./setup.sh
```

This script will:
- Find Python 3.10+ on your system
- Create a virtual environment
- Install all dependencies

**Manual Setup:**

1. **Create a virtual environment** with Python 3.10 or higher:
   ```bash
   # Find your Python 3.10+ installation
   python3.14 -m venv venv  # or python3.10, python3.11, etc.
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

**Note**: If you get an "externally-managed-environment" error, you're using system Python. Always use a virtual environment or the `setup.sh` script.

This will install:
- `surya-ocr` (from GitHub)
- `pdf2image` (for PDF to image conversion)
- `Pillow` (for image processing)
- `torch` (PyTorch, required by surya-ocr)

**Note**: The first time you run the converter, surya-ocr will download model weights automatically.

## Usage

**Important**: Always activate the virtual environment first:
```bash
source venv/bin/activate  # On macOS/Linux
```

### Basic Usage

Convert a PDF to Markdown with default settings:

```bash
python main.py input.pdf
```

This will create `input.md` in the same directory as the input PDF.

### Specify Output File

```bash
python main.py input.pdf --output output.md
```

### Customize Image Directory

```bash
python main.py input.pdf --images-dir extracted_images
```

### Adjust DPI for Better Quality

Higher DPI improves OCR accuracy but increases processing time:

```bash
python main.py input.pdf --dpi 300
```

### Specify Languages

For better accuracy with specific languages:

```bash
python main.py input.pdf --languages en fr de
```

Available language codes include: `en`, `fr`, `de`, `es`, `it`, `pt`, `ru`, `zh`, `ja`, `ko`, and many more. See [surya-ocr documentation](https://github.com/datalab-to/surya) for the full list.

### Complete Example

```bash
python main.py document.pdf \
  --output result.md \
  --images-dir images \
  --dpi 300 \
  --languages en
```

## Output Structure

The converter generates:

1. **Markdown File**: Contains the extracted text with proper structure:
   - Headings (from title detection)
   - Paragraphs
   - Lists (ordered and unordered)
   - Tables (in Markdown table format)
   - Image references

2. **Images Directory**: Contains extracted images from the PDF:
   - Named as `page_N_image_M.png`
   - Referenced in the Markdown file

## How It Works

1. **PDF to Images**: Converts each PDF page to a high-resolution image
2. **Text Detection**: Detects text lines and their bounding boxes
3. **Text Recognition**: Performs OCR on detected text lines
4. **Layout Analysis**: Identifies document structure (text, title, table, image, list)
5. **Reading Order**: Determines the correct reading order for multi-column layouts
6. **Table Recognition**: Extracts and structures table data
7. **Markdown Generation**: Converts all detected elements to Markdown format

## Examples

### Example 1: Academic Paper

```bash
python main.py paper.pdf --output paper.md --dpi 300
```

### Example 2: Multi-language Document

```bash
python main.py multilingual.pdf --languages en fr es
```

### Example 3: Document with Many Images

```bash
python main.py illustrated.pdf --images-dir figures --dpi 250
```

## Troubleshooting

### Error: "surya-ocr is not installed"

Make sure you've installed the dependencies:
```bash
pip install -r requirements.txt
```

### Error: "poppler not found"

Install poppler-utils for your system (see Prerequisites above).

### Poor OCR Quality

- Increase DPI: `--dpi 300` or higher
- Specify languages: `--languages en` (replace with your document's language)
- Ensure the PDF has good image quality

### Out of Memory Errors

- Reduce DPI: `--dpi 150`
- Process smaller PDFs or split large documents

### Tables Not Converting Properly

Surya-ocr returns tables in HTML format. The converter attempts to parse and convert them to Markdown. If a table doesn't convert correctly, it will be included as an HTML code block in the Markdown output.

## Limitations

- Very large PDFs may take significant time to process
- Complex layouts with overlapping elements may require manual adjustment
- Handwritten text recognition quality depends on clarity
- Some table structures may not convert perfectly and will be preserved as HTML

## Performance

Processing time depends on:
- Number of pages
- DPI setting (higher = slower)
- Document complexity
- Hardware (GPU acceleration available with surya-ocr)

Typical performance:
- 1 page @ 200 DPI: ~2-5 seconds (CPU)
- 10 pages @ 200 DPI: ~20-50 seconds (CPU)
- GPU acceleration can be 5-10x faster

## License

This project uses surya-ocr, which is licensed under GPL-3.0. See the [surya-ocr repository](https://github.com/datalab-to/surya) for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- [surya-ocr](https://github.com/datalab-to/surya) - The OCR engine powering this converter
- [pdf2image](https://github.com/Belval/pdf2image) - PDF to image conversion
- [Pillow](https://python-pillow.org/) - Image processing

## Support

For issues related to:
- **This converter**: Open an issue in this repository
- **surya-ocr**: See the [surya-ocr repository](https://github.com/datalab-to/surya)

