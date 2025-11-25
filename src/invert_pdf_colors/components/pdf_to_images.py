from pathlib import Path
from typing import Optional
from wand.image import Image
from PyPDF4 import PdfFileReader

from ..logger import get_logger
from ..exception import InvertPDFColorsException
from ..utils import ensure_dir

logger = get_logger()


def extract_images(pdf_path: Path, output_dir: Path, dpi: int = 200, fmt: str = "jpg") -> int:
    """
    Convert each page of a PDF into an image file in output_dir.

    Returns the number of pages exported.
    """
    try:
        pdf_path = Path(pdf_path)
        output_dir = ensure_dir(Path(output_dir))

        with open(pdf_path, "rb") as f:
            reader = PdfFileReader(f)
            pages = reader.getNumPages()

        for i in range(pages):
            with Image(filename=f"{pdf_path}[{i}]", resolution=dpi) as img:
                img.format = fmt.upper()
                out_file = output_dir / f"page_{i}.{fmt}"
                img.save(filename=str(out_file))
        logger.info(f"Extracted {pages} pages to {output_dir}")
        return pages
    except Exception as e:
        logger.exception("Failed to extract images from PDF")
        raise InvertPDFColorsException(str(e))
