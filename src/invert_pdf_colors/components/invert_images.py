from pathlib import Path
from PIL import Image, ImageOps
from tqdm import tqdm

from ..logger import get_logger
from ..exception import InvertPDFColorsException
from ..utils import ensure_dir, list_images

logger = get_logger()


def invert_directory(input_dir: Path, output_dir: Path, dpi=(300, 300)) -> int:
    """Invert colors of all images in input_dir and write to output_dir. Returns count."""
    try:
        input_dir = Path(input_dir)
        output_dir = ensure_dir(Path(output_dir))
        count = 0
        for img_path in tqdm(list_images(input_dir), desc="Inverting images"):
            with Image.open(img_path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")
                inverted = ImageOps.invert(img)
                inverted.info['dpi'] = dpi
                out_path = output_dir / f"inverted_{img_path.name}"
                inverted.save(out_path, format="JPEG", quality=95, dpi=dpi)
                count += 1
        logger.info(f"Inverted {count} images into {output_dir}")
        return count
    except Exception as e:
        logger.exception("Failed to invert images")
        raise InvertPDFColorsException(str(e))
