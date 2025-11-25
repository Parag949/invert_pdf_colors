from pathlib import Path
from typing import Tuple
from PIL import Image
from tqdm import tqdm

from ..logger import get_logger
from ..exception import InvertPDFColorsException
from ..utils import list_images

logger = get_logger()


def images_to_pdf(input_dir: Path, output_pdf_path: Path, dpi: Tuple[int, int] = (300, 300)) -> int:
    """Combine images in input_dir into a single PDF at output_pdf_path. Returns number of pages."""
    try:
        input_dir = Path(input_dir)
        output_pdf_path = Path(output_pdf_path)
        images = list_images(input_dir)
        if not images:
            raise InvertPDFColorsException("No images found to combine into PDF")

        pil_images = []
        for idx, img_path in enumerate(tqdm(images, desc="Building PDF")):
            img = Image.open(img_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            pil_images.append(img)

        first, rest = pil_images[0], pil_images[1:]
        first.save(output_pdf_path, "PDF", resolution=dpi[0], save_all=True, append_images=rest)

        # Close images
        for im in pil_images:
            im.close()

        logger.info(f"Wrote PDF with {len(images)} pages to {output_pdf_path}")
        return len(images)
    except Exception as e:
        logger.exception("Failed to create PDF from images")
        raise InvertPDFColorsException(str(e))
