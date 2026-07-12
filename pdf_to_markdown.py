"""
PDF to Markdown Converter using Surya OCR

This module provides functionality to convert PDF files to Markdown format
using surya-ocr for text recognition, layout analysis, reading order, and table recognition.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image

try:
    import pdf2image
    # #region agent log
    try:
        with open('/Users/habuild/codes/ocr/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "post-fix",
                "hypothesisId": "A",
                "location": "pdf_to_markdown.py:15",
                "message": "pdf2image import successful (post-fix)",
                "data": {"pdf2image_location": pdf2image.__file__ if hasattr(pdf2image, '__file__') else "unknown"},
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
                "location": "pdf_to_markdown.py:18",
                "message": "pdf2image import still failing (post-fix)",
                "data": {
                    "error": str(e),
                    "python_executable": sys.executable,
                    "sys_path": sys.path
                },
                "timestamp": int(__import__('time').time() * 1000)
            }) + '\n')
    except: pass
    # #endregion
    raise

try:
    # Import surya predictors using the correct API
    from surya.detection import DetectionPredictor
    from surya.foundation import FoundationPredictor
    from surya.recognition import RecognitionPredictor
    from surya.layout import LayoutPredictor
    from surya.table_rec import TableRecPredictor
    SURYA_IMPORT_STYLE = "predictors"
    
    SURYA_AVAILABLE = True
    
    # #region agent log
    try:
        with open('/Users/habuild/codes/ocr/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "run2",
                "hypothesisId": "A,B,C,D,E",
                "location": "pdf_to_markdown.py:71",
                "message": "Surya import successful, SURYA_AVAILABLE=True",
                "data": {"import_style": SURYA_IMPORT_STYLE},
                "timestamp": int(__import__('time').time() * 1000)
            }) + '\n')
    except: pass
    # #endregion
except ImportError as e:
    SURYA_AVAILABLE = False
    SURYA_IMPORT_STYLE = None
    
    # #region agent log
    try:
        with open('/Users/habuild/codes/ocr/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "run2",
                "hypothesisId": "A,B,C,D,E",
                "location": "pdf_to_markdown.py:72",
                "message": "Surya import completely failed, SURYA_AVAILABLE=False",
                "data": {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "error_args": str(e.args) if hasattr(e, 'args') else None,
                    "python_version": sys.version,
                    "python_executable": sys.executable
                },
                "timestamp": int(__import__('time').time() * 1000)
            }) + '\n')
    except: pass
    # #endregion
    
    # Error message will be handled by main.py with more detailed instructions
    pass


def pdf_to_images(pdf_path: str, dpi: int = 200) -> List[Image.Image]:
    """
    Convert PDF pages to PIL Images.
    
    Args:
        pdf_path: Path to the PDF file
        dpi: Resolution for image conversion (default: 200)
        
    Returns:
        List of PIL Images, one per page
    """
    try:
        images = pdf2image.convert_from_path(pdf_path, dpi=dpi)
        return images
    except Exception as e:
        raise Exception(f"Error converting PDF to images: {str(e)}")


def _extract_batch_result(result: Any, index: int = 0) -> Any:
    """
    Safely extract result from batch API response.
    
    Args:
        result: Batch API result (list or single value)
        index: Index to extract (default: 0)
        
    Returns:
        Extracted result or the result itself if not a list
    """
    if isinstance(result, list) and len(result) > index:
        return result[index]
    elif isinstance(result, list) and len(result) > 0:
        return result[0]
    return result


def process_page(
    image: Image.Image,
    det_predictor: DetectionPredictor,
    foundation_predictor: FoundationPredictor,
    rec_predictor: RecognitionPredictor,
    layout_predictor: LayoutPredictor,
    table_predictor: TableRecPredictor,
    languages: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Process a single page image with surya-ocr.
    
    Args:
        image: PIL Image of the page
        det_predictor: DetectionPredictor instance
        foundation_predictor: FoundationPredictor instance
        rec_predictor: RecognitionPredictor instance
        layout_predictor: LayoutPredictor instance
        table_predictor: TableRecPredictor instance
        languages: List of language codes (default: None for auto-detect)
        
    Returns:
        Dictionary containing processed page data
    """
    if not SURYA_AVAILABLE:
        raise ImportError("surya-ocr is not available. Please install it first.")
    
    # Detect text lines and recognize text
    try:
        from surya.common.surya.schema import TaskNames
        task_names = [TaskNames.ocr_with_boxes]
        ocr_result = rec_predictor(
            [image],
            task_names=task_names,
            det_predictor=det_predictor,
            math_mode=True
        )[0]  # Get first result
        text_lines = ocr_result.text_lines
    except Exception as e:
        print(f"Warning: Could not perform OCR: {e}")
        text_lines = []
    
    # Detect layout
    try:
        layout_result = layout_predictor([image])[0]  # Get first result
        layout_boxes = layout_result.bboxes
        # Convert layout boxes to dict format for compatibility
        layout_predictions = [
            {
                'type': box.label,
                'bbox': list(box.bbox),
                'position': box.position
            }
            for box in layout_boxes
        ]
    except Exception as e:
            print(f"Warning: Could not detect layout: {e}")
            layout_predictions = []
    
    # Reading order is embedded in layout boxes via position field
    # Sort by position to get reading order
    layout_predictions.sort(key=lambda x: x.get('position', 999))
    reading_order = {'order': list(range(len(layout_predictions)))}
    
    # Detect tables
    try:
        table_result = table_predictor([image])[0]  # Get first result
        # Convert table result to dict format
        table_predictions = {
            'cells': [cell.model_dump() for cell in table_result.cells],
            'rows': [row.model_dump() for row in table_result.rows],
            'cols': [col.model_dump() for col in table_result.cols],
            'bbox': table_result.image_bbox
        }
    except Exception as e:
            print(f"Warning: Could not recognize tables: {e}")
        table_predictions = None
    
    # Convert text lines to dict format for compatibility
    text_lines_dict = []
    for line in text_lines:
        text_lines_dict.append({
            'text': line.text,
            'bbox': list(line.bbox),
            'chars': [char.model_dump() for char in line.chars] if hasattr(line, 'chars') else []
        })
    
    return {
        'image': image,
        'text_lines': text_lines_dict,
        'layout': layout_predictions,
        'reading_order': reading_order,
        'tables': table_predictions
    }


def table_to_markdown(table_data: Dict[str, Any]) -> str:
    """
    Convert surya table recognition output to Markdown table format.
    
    Args:
        table_data: Table data from surya table recognition
        
    Returns:
        Markdown formatted table string
    """
    if not table_data or not isinstance(table_data, dict):
        return ""
    
    try:
        # Surya table recognition returns cells, rows, and cols
        cells = table_data.get('cells', [])
        rows = table_data.get('rows', [])
        
        if not cells:
            return ""
        
        # Build a grid from cells
        # Find max row and col IDs
        max_row = max([cell.get('row_id', 0) for cell in cells] + [0])
        max_col = max([cell.get('col_id', 0) for cell in cells if cell.get('col_id') is not None] + [0])
        
        if max_row < 0 or max_col < 0:
            # Try to infer from cell positions
            return ""
        
        # Create a grid
        grid = [['' for _ in range(max_col + 1)] for _ in range(max_row + 1)]
        
        # Fill grid with cell text
        for cell in cells:
            row_id = cell.get('row_id', 0)
            col_id = cell.get('col_id', 0)
            if col_id is None:
                continue
            
            # Get text from cell
            text_lines = cell.get('text_lines', [])
            if text_lines:
                # Extract text from text lines
                cell_text = ' '.join([line.get('text', '') if isinstance(line, dict) else str(line) for line in text_lines])
            else:
                cell_text = str(cell.get('text', ''))
            
            if 0 <= row_id <= max_row and 0 <= col_id <= max_col:
                grid[row_id][col_id] = cell_text.strip()
        
        # Convert grid to markdown
        if not grid or not grid[0]:
            return ""
        
        markdown_lines = []
        num_cols = len(grid[0])
        
        # Header row (first row)
        header_cells = [str(grid[0][j]) if j < len(grid[0]) else "" for j in range(num_cols)]
        header_row = "| " + " | ".join(header_cells) + " |"
                    separator = "| " + " | ".join(["---"] * num_cols) + " |"
                    markdown_lines.append(header_row)
                    markdown_lines.append(separator)
                    
                    # Data rows
        for i in range(1, len(grid)):
            row_cells = [str(grid[i][j]) if j < len(grid[i]) else "" for j in range(num_cols)]
            row_str = "| " + " | ".join(row_cells) + " |"
                        markdown_lines.append(row_str)
                    
                    return "\n".join(markdown_lines) if markdown_lines else ""
        
    except Exception as e:
        return f"<!-- Table conversion error: {str(e)} -->"


def extract_image_from_region(image: Image.Image, bbox: List[float]) -> Image.Image:
    """
    Extract image region from page based on bounding box.
    
    Args:
        image: Full page image
        bbox: Bounding box [x1, y1, x2, y2] in image coordinates
        
    Returns:
        Extracted image region
    """
    x1, y1, x2, y2 = map(int, bbox)
    # Ensure coordinates are within image bounds
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(image.width, x2)
    y2 = min(image.height, y2)
    
    if x2 > x1 and y2 > y1:
        return image.crop((x1, y1, x2, y2))
    return None


def convert_to_markdown(
    processed_pages: List[Dict[str, Any]],
    output_dir: str,
    images_dir: Optional[str] = None
) -> str:
    """
    Convert processed page data to Markdown format.
    
    Args:
        processed_pages: List of processed page dictionaries
        output_dir: Directory for output files
        images_dir: Directory for extracted images (relative to output_dir)
        
    Returns:
        Complete Markdown content as string
    """
    markdown_lines = []
    images_dir_path = Path(output_dir) / (images_dir or "images")
    images_dir_path.mkdir(parents=True, exist_ok=True)
    
    for page_num, page_data in enumerate(processed_pages):
        if page_num > 0:
            markdown_lines.append("\n---\n")  # Page separator
        
        markdown_lines.append(f"# Page {page_num + 1}\n\n")
        
        # Get layout blocks and sort by reading order
        layout_blocks = page_data.get('layout', [])
        reading_order = page_data.get('reading_order', {})
        text_lines = page_data.get('text_lines', [])
        tables = page_data.get('tables')  # Can be None or a dict
        image = page_data.get('image')
        
        # Create a mapping of layout blocks to their order
        block_order = {}
        ordered_blocks = []
        
        # Handle different reading order formats
        if reading_order:
            if isinstance(reading_order, dict):
                # Format: {'order': [indices]}
                order_indices = reading_order.get('order', [])
                if order_indices:
                    for order_idx in order_indices:
                        if isinstance(order_idx, int) and 0 <= order_idx < len(layout_blocks):
                            ordered_blocks.append((order_idx, layout_blocks[order_idx]))
            elif isinstance(reading_order, list):
                # Format: [ordered block indices or block objects]
                for item in reading_order:
                    if isinstance(item, int) and 0 <= item < len(layout_blocks):
                        ordered_blocks.append((item, layout_blocks[item]))
                    elif isinstance(item, dict):
                        # Already ordered blocks
                        ordered_blocks.append((len(ordered_blocks), item))
        
        # If no reading order, use layout blocks as-is
        if not ordered_blocks:
            ordered_blocks = [(i, block) for i, block in enumerate(layout_blocks)]
        
        # Sort by order index and create block_order dict
        ordered_blocks.sort(key=lambda x: x[0])
        block_order = {i: block for i, (_, block) in enumerate(ordered_blocks)}
        
        # Process blocks in reading order
        processed_blocks = set()
        for order_idx in sorted(block_order.keys()):
            if order_idx in processed_blocks:
                continue
            processed_blocks.add(order_idx)
            
            block = block_order[order_idx]
            block_type = block.get('type', 'text').lower() if isinstance(block, dict) else 'text'
            
            if block_type == 'title':
                # Extract text from this region
                bbox = block.get('bbox', []) if isinstance(block, dict) else []
                text = extract_text_from_region(text_lines, bbox)
                if text:
                    # Determine heading level (simplified - could be enhanced)
                    markdown_lines.append(f"## {text}\n\n")
            
            elif block_type == 'text':
                bbox = block.get('bbox', []) if isinstance(block, dict) else []
                text = extract_text_from_region(text_lines, bbox)
                if text:
                    markdown_lines.append(f"{text}\n\n")
            
            elif block_type == 'table':
                # Find corresponding table data
                bbox = block.get('bbox', []) if isinstance(block, dict) else []
                table_data = find_table_by_bbox(tables, bbox) if tables else None
                if table_data:
                    table_md = table_to_markdown(table_data)
                    if table_md:
                        markdown_lines.append(f"{table_md}\n\n")
            
            elif block_type == 'image' or block_type == 'figure':
                bbox = block.get('bbox', []) if isinstance(block, dict) else []
                if image and bbox:
                    img_region = extract_image_from_region(image, bbox)
                    if img_region:
                        img_filename = f"page_{page_num + 1}_image_{len(processed_blocks)}.png"
                        img_path = images_dir_path / img_filename
                        img_region.save(img_path)
                        rel_path = f"{images_dir or 'images'}/{img_filename}"
                        markdown_lines.append(f"![Image]({rel_path})\n\n")
            
            elif block_type == 'list':
                bbox = block.get('bbox', []) if isinstance(block, dict) else []
                text = extract_text_from_region(text_lines, bbox)
                if text:
                    # Simple list formatting (could be enhanced)
                    lines = text.split('\n')
                    for line in lines:
                        if line.strip():
                            markdown_lines.append(f"- {line.strip()}\n")
                    markdown_lines.append("\n")
        
        # If no layout blocks, just extract all text
        if not layout_blocks and text_lines:
            all_texts = []
            for line in text_lines:
                if isinstance(line, dict):
                    text = line.get('text', '') or line.get('text_line', '') or line.get('content', '')
                elif isinstance(line, list) and len(line) > 1:
                    text = line[1]
                else:
                    text = str(line) if line else ''
                if text:
                    all_texts.append(str(text))
            if all_texts:
                markdown_lines.append(f"{' '.join(all_texts)}\n\n")
    
    return "".join(markdown_lines)


def extract_text_from_region(text_lines: List[Dict[str, Any]], bbox: List[float]) -> str:
    """
    Extract text from lines that overlap with the given bounding box.
    
    Args:
        text_lines: List of text line dictionaries with bbox and text
        bbox: Bounding box [x1, y1, x2, y2]
        
    Returns:
        Concatenated text from overlapping lines
    """
    if not bbox or len(bbox) < 4:
        return ""
    
    x1, y1, x2, y2 = bbox
    texts = []
    
    for line in text_lines:
        # Handle different line formats
        if isinstance(line, dict):
            line_bbox = line.get('bbox', [])
            # Try different possible keys for text
            text = line.get('text', '') or line.get('text_line', '') or line.get('content', '')
        elif isinstance(line, list) and len(line) >= 2:
            # Format: [bbox, text] or similar
            line_bbox = line[0] if isinstance(line[0], list) else []
            text = line[1] if len(line) > 1 else ''
        else:
            continue
        
        if len(line_bbox) >= 4:
            lx1, ly1, lx2, ly2 = line_bbox[:4]
            # Check if line overlaps with region (using polygon overlap for better accuracy)
            # Simple bbox overlap check
            if not (lx2 < x1 or lx1 > x2 or ly2 < y1 or ly1 > y2):
                if text:
                    texts.append(str(text))
    
    return " ".join(texts)


def find_table_by_bbox(tables: Optional[Dict[str, Any]], bbox: List[float]) -> Optional[Dict[str, Any]]:
    """
    Find table data that matches the given bounding box.
    
    Args:
        tables: Table dictionary (can be None)
        bbox: Bounding box to match
        
    Returns:
        Matching table data or None
    """
    if not tables or not isinstance(tables, dict) or not bbox or len(bbox) < 4:
        return None
    
    # Check if table bbox overlaps with the given bbox
    table_bbox = tables.get('bbox', [])
    if len(table_bbox) >= 4:
    x1, y1, x2, y2 = bbox
            tx1, ty1, tx2, ty2 = table_bbox[:4]
            # Check if bboxes overlap significantly
            overlap_x = max(0, min(x2, tx2) - max(x1, tx1))
            overlap_y = max(0, min(y2, ty2) - max(y1, ty1))
            overlap_area = overlap_x * overlap_y
            
            bbox_area = (x2 - x1) * (y2 - y1)
            if bbox_area > 0 and overlap_area / bbox_area > 0.5:
            return tables
    
    return None


def convert_pdf_to_markdown(
    pdf_path: str,
    output_path: Optional[str] = None,
    images_dir: Optional[str] = None,
    languages: Optional[List[str]] = None,
    dpi: int = 200
) -> str:
    """
    Main function to convert PDF to Markdown.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output Markdown file (default: same name as PDF with .md extension)
        images_dir: Directory name for extracted images (default: "images")
        languages: List of language codes for OCR (default: None for auto-detect)
        dpi: DPI for PDF to image conversion (default: 200)
        
    Returns:
        Path to the created Markdown file
    """
    if not SURYA_AVAILABLE:
        raise ImportError("surya-ocr is not available. Please install it first.")
    
    # Set default output path
    if output_path is None:
        output_path = str(Path(pdf_path).with_suffix('.md'))
    
    output_dir = str(Path(output_path).parent)
    
    # Load predictors (they will be cached after first load)
    print("Loading surya models...")
    det_predictor = DetectionPredictor()
    foundation_predictor = FoundationPredictor()
    rec_predictor = RecognitionPredictor(foundation_predictor)
    layout_predictor = LayoutPredictor(foundation_predictor)
    table_predictor = TableRecPredictor()
    
    # Convert PDF to images
    print(f"Converting PDF to images (DPI: {dpi})...")
    images = pdf_to_images(pdf_path, dpi=dpi)
    print(f"Found {len(images)} pages")
    
    # Process each page
    processed_pages = []
    for i, image in enumerate(images):
        print(f"Processing page {i + 1}/{len(images)}...")
        page_data = process_page(
            image,
            det_predictor,
            foundation_predictor,
            rec_predictor,
            layout_predictor,
            table_predictor,
            languages
        )
        processed_pages.append(page_data)
    
    # Convert to Markdown
    print("Converting to Markdown...")
    markdown_content = convert_to_markdown(processed_pages, output_dir, images_dir)
    
    # Write Markdown file
    print(f"Writing Markdown to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Conversion complete! Output: {output_path}")
    return output_path

