import os
import re
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor

def format_name(text):
    """
    Formats a given text to be used as a filename.

    Args:
        text (str): The input text to format.

    Returns:
        str: The formatted text in lowercase, with special characters removed and spaces replaced by hyphens.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = text.replace(" ", "-")
    return text

def calculate_resize_factor(original_width, original_height, max_width=2262, max_height=1501):
    """
    Calculates the scaling factor to resize an image while maintaining its aspect ratio.

    Args:
        original_width (int): The original width of the image.
        original_height (int): The original height of the image.
        max_width (int, optional): The maximum allowed width. Defaults to 2262.
        max_height (int, optional): The maximum allowed height. Defaults to 1501.

    Returns:
        float: The scaling factor to resize the image.
    """
    scale_width = max_width / original_width
    scale_height = max_height / original_height
    scale_factor = min(scale_width, scale_height)
    return scale_factor

def resize_image(img, max_width=2262, max_height=1501):
    """
    Resizes an image to fit within the specified maximum dimensions while maintaining its aspect ratio.

    Args:
        img (PIL.Image): The image to resize.
        max_width (int, optional): The maximum allowed width. Defaults to 2262.
        max_height (int, optional): The maximum allowed height. Defaults to 1501.

    Returns:
        PIL.Image: The resized image.
    """
    width, height = img.size
    scale_factor = calculate_resize_factor(width, height, max_width, max_height)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img

def compress_webp(input_path, output_path, max_size_kb=1024, quality=80, max_resolution=None):
    """
    Compresses an image to WebP format, ensuring the file size does not exceed the specified limit.

    Args:
        input_path (str): The path to the input image file.
        output_path (str): The path to save the compressed image.
        max_size_kb (int, optional): The maximum allowed file size in kilobytes. Defaults to 1024.
        quality (int, optional): The initial quality of the compression (1-100). Defaults to 80.
        max_resolution (tuple, optional): The maximum resolution (width, height) for resizing. Defaults to None.
    """
    max_size_bytes = max_size_kb * 1024

    with Image.open(input_path) as img:
        if max_resolution:
            img = resize_image(img, max_resolution[0], max_resolution[1])

        from io import BytesIO
        buffer = BytesIO()
        
        img.save(buffer, "WEBP", quality=quality, method=6)
        file_size = buffer.tell()

        while file_size > max_size_bytes and quality > 10:
            buffer.seek(0)
            buffer.truncate()
            quality -= 5
            img.save(buffer, "WEBP", quality=quality, method=6)
            file_size = buffer.tell()

        with open(output_path, "wb") as f:
            f.write(buffer.getvalue())

def process_image_task(args):
    """
    Processes a single image task by compressing it.

    Args:
        args (tuple): A tuple containing:
            - input_path (str): The path to the input image file.
            - output_path (str): The path to save the compressed image.
            - max_size_kb (int): The maximum allowed file size in kilobytes.
            - quality (int): The quality of the compression (1-100).
            - max_resolution (tuple): The maximum resolution (width, height) for resizing.
    """
    input_path, output_path, max_size_kb, quality, max_resolution = args
    try:
        compress_webp(input_path, output_path, max_size_kb, quality, max_resolution)
        print(f"Processed: {input_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_images(input_folder, output_folder, city, street, max_size_kb=1024, quality=80, max_resolution=None):
    """
    Processes all WebP images in the input folder, compresses them, and saves them to the output folder.

    Args:
        input_folder (str): The folder containing the original images.
        output_folder (str): The folder to save the compressed images.
        city (str): The city name to include in the output filenames.
        street (str): The street name to include in the output filenames.
        max_size_kb (int, optional): The maximum allowed file size in kilobytes. Defaults to 1024.
        quality (int, optional): The quality of the compression (1-100). Defaults to 80.
        max_resolution (tuple, optional): The maximum resolution (width, height) for resizing. Defaults to None.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    formatted_city = format_name(city)
    formatted_street = format_name(street)

    tasks = []
    counter = 1

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".webp"):
            input_path = os.path.join(input_folder, filename)
            output_filename = f"{formatted_city}-{formatted_street}-{counter}.webp"
            output_path = os.path.join(output_folder, output_filename)
            tasks.append((input_path, output_path, max_size_kb, quality, max_resolution))
            counter += 1

    with ThreadPoolExecutor() as executor:
        executor.map(process_image_task, tasks)

    messagebox.showinfo("Completed", "All images have been processed!")

def select_input_folder():
    """
    Opens a dialog to select the input folder and updates the input_folder_var.
    """
    folder = filedialog.askdirectory(title="Select the folder with original images")
    if folder:
        input_folder_var.set(folder)

def select_output_folder():
    """
    Opens a dialog to select the output folder and updates the output_folder_var.
    """
    folder = filedialog.askdirectory(title="Select the folder to save compressed images")
    if folder:
        output_folder_var.set(folder)

def start_processing():
    """
    Starts the image processing workflow by validating inputs and calling process_images.
    """
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    city = city_var.get().strip()
    street = street_var.get().strip()
    max_size_kb = int(max_size_kb_var.get())
    quality = int(quality_var.get())
    max_width = int(max_width_var.get())
    max_height = int(max_height_var.get())

    if not input_folder or not output_folder:
        messagebox.showwarning("Warning", "Select input and output folders!")
        return
    if not city or not street:
        messagebox.showwarning("Warning", "Fill in the city and street fields!")
        return

    process_images(input_folder, output_folder, city, street, max_size_kb, quality, (max_width, max_height))

# GUI Setup
root = tk.Tk()
root.title("WebP Image Compressor")

# Variables for GUI inputs
input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
city_var = tk.StringVar()
street_var = tk.StringVar()
max_size_kb_var = tk.StringVar(value="400")  # Default value for max_size_kb
quality_var = tk.StringVar(value="80")      # Default value for quality
max_width_var = tk.StringVar(value="2262")  # Default value for max_width
max_height_var = tk.StringVar(value="1501") # Default value for max_height

# GUI Layout
tk.Label(root, text="Folder with original images:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=input_folder_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Select", command=select_input_folder).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Folder to save compressed images:").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Select", command=select_output_folder).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="City:").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=city_var, width=50).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Street:").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=street_var, width=50).grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Max Size (KB):").grid(row=4, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=max_size_kb_var, width=10).grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Quality (1-100):").grid(row=5, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=quality_var, width=10).grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Max Width:").grid(row=6, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=max_width_var, width=10).grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Max Height:").grid(row=7, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=max_height_var, width=10).grid(row=7, column=1, padx=5, pady=5)

tk.Button(root, text="Process Images", command=start_processing).grid(row=8, column=1, pady=10)

# Start the GUI event loop
root.mainloop()