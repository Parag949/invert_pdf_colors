from pathlib import Path
from PIL import Image, ImageOps
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

from ..logger import get_logger
from ..exception import InvertPDFColorsException
from ..utils import ensure_dir, list_images

logger = get_logger()


def _invert_single_image(args):
    """Helper function to invert a single image (for parallel processing)."""
    img_path, output_dir, dpi = args
    try:
        with Image.open(img_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            inverted = ImageOps.invert(img)
            inverted.info['dpi'] = dpi
            out_path = output_dir / f"inverted_{img_path.name}"
            inverted.save(out_path, format="JPEG", quality=95, dpi=dpi)
        return True
    except Exception as e:
        logger.error(f"Failed to invert {img_path}: {e}")
        return False


def invert_directory(input_dir: Path, output_dir: Path, dpi=(300, 300), max_workers=None) -> int:
    """
    Invert colors of all images in input_dir and write to output_dir using parallel processing.
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save inverted images
        dpi: DPI settings for output images
        max_workers: Number of parallel workers (default: CPU count)
    
    Returns:
        Number of successfully inverted images
    """
    try:
        input_dir = Path(input_dir)
        output_dir = ensure_dir(Path(output_dir))
        
        image_list = list_images(input_dir)
        if not image_list:
            logger.warning("No images found to invert")
            return 0
        
        # Use all available CPU cores if not specified
        if max_workers is None:
            max_workers = os.cpu_count() or 1
        
        # Prepare arguments for parallel processing
        tasks = [(img_path, output_dir, dpi) for img_path in image_list]
        
        count = 0
        # Use ProcessPoolExecutor for true parallel processing (bypasses GIL)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            futures = {executor.submit(_invert_single_image, task): task for task in tasks}
            
            # Process results with progress bar
            for future in tqdm(as_completed(futures), total=len(tasks), desc="Inverting images"):
                if future.result():
                    count += 1
        
        logger.info(f"Inverted {count}/{len(image_list)} images into {output_dir} using {max_workers} workers")
        return count
    except Exception as e:
        logger.exception("Failed to invert images")
        raise InvertPDFColorsException(str(e))
