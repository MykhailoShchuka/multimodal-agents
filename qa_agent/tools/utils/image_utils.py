import io
import base64
from PIL import Image


def compress_image_for_base64(image, max_size=(800, 800), quality=65):
    """Compress PIL.Image to JPEG base64 within max_size while preserving aspect ratio."""
    compressed_image = image.copy()
    original_width, original_height = compressed_image.size
    max_width, max_height = max_size
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    scale_factor = min(width_ratio, height_ratio, 1.0)
    if scale_factor < 1.0:
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        compressed_image = compressed_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    if compressed_image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', compressed_image.size, (255, 255, 255))
        if compressed_image.mode == 'P':
            compressed_image = compressed_image.convert('RGBA')
        background.paste(compressed_image, mask=compressed_image.split()[-1] if compressed_image.mode == 'RGBA' else None)
        compressed_image = background
    buffer = io.BytesIO()
    compressed_image.save(buffer, format='JPEG', quality=quality, optimize=True)
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()


def compress_image_bytes_to_base64(image_bytes: bytes, max_size=(800, 800), quality: int = 65) -> str:
    """Compress raw image bytes to JPEG base64 with resizing.

    Accepts bytes (e.g., PNG screenshot), downsizes preserving aspect ratio to fit within
    max_size, converts to RGB on white background if needed, and encodes as JPEG base64.
    """
    with Image.open(io.BytesIO(image_bytes)) as img:
        return compress_image_for_base64(img, max_size=max_size, quality=quality)
