from pathlib import Path
from typing import Tuple
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from ..logger import get_logger
from ..exception import InvertPDFColorsException
from ..utils import list_images

logger = get_logger()


def _load_and_convert_image(img_path):
    """Helper function to load and convert a single image (for parallel processing)."""
    try:
        img = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img
    except Exception as e:
        logger.error(f"Failed to load {img_path}: {e}")
        return None


def images_to_pdf(input_dir: Path, output_pdf_path: Path, dpi: Tuple[int, int] = (300, 300), max_workers=None) -> int:
    """
    Combine images in input_dir into a single PDF at output_pdf_path using parallel loading.
    
    Args:
        input_dir: Directory containing images
        output_pdf_path: Output PDF file path
        dpi: DPI for PDF
        max_workers: Number of parallel workers for loading (default: CPU count * 2)
    
    Returns:
        Number of pages in PDF
    """
    try:
        input_dir = Path(input_dir)
        output_pdf_path = Path(output_pdf_path)
        images = list_images(input_dir)
        if not images:
            raise InvertPDFColorsException("No images found to combine into PDF")

        # Use ThreadPoolExecutor for I/O-bound image loading
        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) * 2)
        
        pil_images = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all image loading tasks
            futures = {executor.submit(_load_and_convert_image, img_path): img_path for img_path in images}
            
            # Collect results in order
            for img_path in tqdm(images, desc="Loading images"):
                # Find the corresponding future
                future = next(f for f in futures if futures[f] == img_path)
                img = future.result()
                if img:
                    pil_images.append(img)
        
        if not pil_images:
            raise InvertPDFColorsException("No valid images loaded")
        
        logger.info(f"Loaded {len(pil_images)} images, creating PDF...")
        
        # Create PDF
        first, rest = pil_images[0], pil_images[1:]
        first.save(output_pdf_path, "PDF", resolution=dpi[0], save_all=True, append_images=rest)

        # Close images
        for im in pil_images:
            im.close()

        logger.info(f"Wrote PDF with {len(pil_images)} pages to {output_pdf_path}")
        return len(pil_images)
    except Exception as e:
        logger.exception("Failed to create PDF from images")
        raise InvertPDFColorsException(str(e))
