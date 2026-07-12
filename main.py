#!/usr/bin/env python3
"""
PDF to Markdown Converter CLI

A command-line tool to convert PDF files to Markdown format using surya-ocr.
"""

import argparse
import sys
import json
from pathlib import Path

try:
    from pdf_to_markdown import convert_pdf_to_markdown, SURYA_AVAILABLE
    # #region agent log
    try:
        with open('/Users/habuild/codes/ocr/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "A",
                "location": "main.py:14",
                "message": "pdf_to_markdown import successful (post-fix)",
                "data": {"SURYA_AVAILABLE": SURYA_AVAILABLE},
                "timestamp": int(__import__('time').time() * 1000)
            }) + '\n')
    except: pass
    # #endregion
except ImportError as e:
    # #region agent log
    try:
        with open('/Users/habuild/codes/ocr/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "A",
                "location": "main.py:17",
                "message": "pdf_to_markdown import still failing (post-fix)",
                "data": {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "python_executable": sys.executable
                },
                "timestamp": int(__import__('time').time() * 1000)
            }) + '\n')
    except: pass
    # #endregion
    raise


def main():
    parser = argparse.ArgumentParser(
        description='Convert PDF files to Markdown format using surya-ocr',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py document.pdf
  python main.py document.pdf --output output.md
  python main.py document.pdf --images-dir extracted_images
  python main.py document.pdf --output result.md --images-dir imgs --dpi 300
        """
    )
    
    parser.add_argument(
        'pdf_path',
        type=str,
        help='Path to the input PDF file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Path to the output Markdown file (default: same name as PDF with .md extension)'
    )
    
    parser.add_argument(
        '--images-dir',
        type=str,
        default='images',
        help='Directory name for extracted images (default: "images")'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=200,
        help='DPI for PDF to image conversion (default: 200)'
    )
    
    parser.add_argument(
        '--languages',
        type=str,
        nargs='+',
        default=None,
        help='Language codes for OCR (e.g., --languages en fr de). Default: auto-detect'
    )
    
    args = parser.parse_args()
    
    # Check if surya is available
    if not SURYA_AVAILABLE:
        import sys as sys_module
        python_version = sys_module.version_info
        python_major = python_version.major
        python_minor = python_version.minor
        
        print("Error: surya-ocr is not available.", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"Current Python version: {python_major}.{python_minor}.{python_version.micro}", file=sys.stderr)
        print(f"Required Python version: 3.10 or higher", file=sys.stderr)
        print(f"", file=sys.stderr)
        
        if python_major < 3 or (python_major == 3 and python_minor < 10):
            print("Your Python version is too old. Please install Python 3.10 or higher:", file=sys.stderr)
            print("", file=sys.stderr)
            print("  macOS (Homebrew):", file=sys.stderr)
            print("    brew install python@3.10", file=sys.stderr)
            print("    # Then use: python3.10 main.py ...", file=sys.stderr)
            print("", file=sys.stderr)
            print("  Or download from: https://www.python.org/downloads/", file=sys.stderr)
            print("", file=sys.stderr)
            print("After installing Python 3.10+, install dependencies:", file=sys.stderr)
            print("  python3.10 -m pip install -r requirements.txt", file=sys.stderr)
        else:
            print("Please install surya-ocr using:", file=sys.stderr)
            print("  pip install git+https://github.com/datalab-to/surya.git", file=sys.stderr)
            print("", file=sys.stderr)
            print("Or install all dependencies:", file=sys.stderr)
            print("  pip install -r requirements.txt", file=sys.stderr)
        
        sys.exit(1)
    
    # Validate input PDF path
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"Error: Input file must be a PDF: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Convert PDF to Markdown
        output_path = convert_pdf_to_markdown(
            pdf_path=str(pdf_path),
            output_path=args.output,
            images_dir=args.images_dir,
            languages=args.languages,
            dpi=args.dpi
        )
        
        print(f"\n✓ Successfully converted PDF to Markdown!")
        print(f"  Input:  {pdf_path}")
        print(f"  Output: {output_path}")
        if args.images_dir:
            images_path = Path(output_path).parent / args.images_dir
            if images_path.exists():
                image_count = len(list(images_path.glob('*.png'))) + len(list(images_path.glob('*.jpg')))
                if image_count > 0:
                    print(f"  Images: {image_count} images extracted to {images_path}")
        
    except KeyboardInterrupt:
        print("\n\nConversion interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError during conversion: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

