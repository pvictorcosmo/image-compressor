# core/tasks.py
import os
from .processor import process_image
from .utils import ensure_directory


def process_images_task(input_folder, output_folder, max_size_kb, quality, max_resolution, fmt):
    """
    Process all images in a folder.
    """
    ensure_directory(output_folder)

    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)

        if not os.path.isfile(file_path):
            continue

        try:
            output_path = os.path.join(
                output_folder, f"{os.path.splitext(file_name)[0]}.{fmt.lower()}"
            )
            process_image(file_path, output_path, max_size_kb, quality, max_resolution, fmt)
            print(f"✅ Processed: {file_name}")
        except Exception as e:
            print(f"❌ Failed: {file_name} -> {e}")
