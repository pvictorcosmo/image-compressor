# core/processor.py
import os
from PIL import Image


def process_image(input_path, output_path, max_size_kb, quality, max_resolution, fmt):
    """
    Process a single image: resize, compress and save to desired format.
    """
    with Image.open(input_path) as img:
        # Resize
        img.thumbnail(max_resolution)

        # Save once
        img.save(output_path, fmt, quality=quality, optimize=True)

        # Ensure size under max_size_kb
        while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
            quality -= 5
            img.save(output_path, fmt, quality=quality, optimize=True)
