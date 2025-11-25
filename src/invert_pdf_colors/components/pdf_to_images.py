from pathlib import Path
from typing import Optional
from wand.image import Image
from PyPDF4 import PdfFileReader
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os

from ..logger import get_logger
from ..exception import InvertPDFColorsException
from ..utils import ensure_dir

logger = get_logger()


def _extract_single_page(args):
    """Helper function to extract a single page (for parallel processing)."""
    pdf_path, page_num, output_dir, dpi, fmt = args
    try:
        with Image(filename=f"{pdf_path}[{page_num}]", resolution=dpi) as img:
            img.format = fmt.upper()
            out_file = output_dir / f"page_{page_num}.{fmt}"
            img.save(filename=str(out_file))
        return True
    except Exception as e:
        logger.error(f"Failed to extract page {page_num}: {e}")
        return False


def extract_images(pdf_path: Path, output_dir: Path, dpi: int = 200, fmt: str = "jpg", max_workers=None) -> int:
    """
    Convert each page of a PDF into an image file in output_dir using parallel processing.
    
    Args:
        pdf_path: Path to input PDF
        output_dir: Directory to save extracted images
        dpi: Resolution for extraction
        fmt: Image format (jpg, png, etc.)
        max_workers: Number of parallel workers (default: CPU count * 2 for I/O bound)
    
    Returns:
        Number of pages exported
    """
    try:
        pdf_path = Path(pdf_path)
        output_dir = ensure_dir(Path(output_dir))

        with open(pdf_path, "rb") as f:
            reader = PdfFileReader(f)
            pages = reader.getNumPages()

        if pages == 0:
            logger.warning("PDF has no pages")
            return 0

        # Use ThreadPoolExecutor for I/O-bound PDF extraction (better than ProcessPool for I/O)
        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) * 2)  # Cap at 32 threads
        
        # Prepare tasks
        tasks = [(pdf_path, i, output_dir, dpi, fmt) for i in range(pages)]
        
        count = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_extract_single_page, task): task for task in tasks}
            
            for future in tqdm(as_completed(futures), total=len(tasks), desc="Extracting pages"):
                if future.result():
                    count += 1
        
        logger.info(f"Extracted {count}/{pages} pages to {output_dir} using {max_workers} workers")
        return count
    except Exception as e:
        logger.exception("Failed to extract images from PDF")
        raise InvertPDFColorsException(str(e))
