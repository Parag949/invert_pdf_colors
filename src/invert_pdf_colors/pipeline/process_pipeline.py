from pathlib import Path

from ..logger import get_logger
from ..exception import InvertPDFColorsException
from ..utils import ensure_dir
from ..components.pdf_to_images import extract_images
from ..components.invert_images import invert_directory
from ..components.images_to_pdf import images_to_pdf

logger = get_logger()


def run_pipeline(input_pdf: Path, work_dir: Path, output_pdf: Path, dpi_extract: int = 200, dpi_output=(300, 300)) -> None:
    """
    End-to-end pipeline: PDF -> images -> inverted images -> PDF
    """
    try:
        work_dir = ensure_dir(Path(work_dir))
        pages_dir = ensure_dir(work_dir / "pages")
        inverted_dir = ensure_dir(work_dir / "inverted")

        extract_images(Path(input_pdf), pages_dir, dpi=dpi_extract)
        invert_directory(pages_dir, inverted_dir, dpi=dpi_output)
        ensure_dir(Path(output_pdf).parent)
        images_to_pdf(inverted_dir, Path(output_pdf), dpi=dpi_output)
        logger.info("Pipeline completed successfully")
    except Exception as e:
        logger.exception("Pipeline failed")
        raise InvertPDFColorsException(str(e))
