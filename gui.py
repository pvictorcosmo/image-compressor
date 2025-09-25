import tkinter as tk
from tkinter import filedialog, messagebox
from core import tasks
import config


def start_app():
    root = tk.Tk()
    root.title(config.APP_NAME)

    # GUI state variables
    input_folder_var = tk.StringVar()
    output_folder_var = tk.StringVar()
    max_size_kb_var = tk.StringVar(value=str(config.DEFAULT_MAX_SIZE_KB))
    quality_var = tk.StringVar(value=str(config.DEFAULT_QUALITY))
    max_width_var = tk.StringVar(value=str(config.DEFAULT_MAX_WIDTH))
    max_height_var = tk.StringVar(value=str(config.DEFAULT_MAX_HEIGHT))
    format_var = tk.StringVar(value=config.DEFAULT_FORMAT)

    def select_input_folder():
        folder = filedialog.askdirectory(title="Select input folder")
        if folder:
            input_folder_var.set(folder)

    def select_output_folder():
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            output_folder_var.set(folder)

    def start_processing():
        input_folder = input_folder_var.get()
        output_folder = output_folder_var.get()

        if not input_folder or not output_folder:
            messagebox.showwarning("Warning", "Select input and output folders!")
            return

        try:
            tasks.process_images_task(
                input_folder,
                output_folder,
                max_size_kb=int(max_size_kb_var.get()),
                quality=int(quality_var.get()),
                max_resolution=(int(max_width_var.get()), int(max_height_var.get())),
                fmt=format_var.get(),
            )
            messagebox.showinfo("Completed", "All images have been processed!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Layout
    tk.Label(root, text="Input Folder:").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=input_folder_var, width=50).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Select", command=select_input_folder).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Select", command=select_output_folder).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(root, text="Max Size (KB):").grid(row=2, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=max_size_kb_var, width=10).grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Quality (1-100):").grid(row=3, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=quality_var, width=10).grid(row=3, column=1, padx=5, pady=5)

    tk.Label(root, text="Max Width:").grid(row=4, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=max_width_var, width=10).grid(row=4, column=1, padx=5, pady=5)

    tk.Label(root, text="Max Height:").grid(row=5, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=max_height_var, width=10).grid(row=5, column=1, padx=5, pady=5)

    tk.Label(root, text="Output Format:").grid(row=6, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=format_var, width=10).grid(row=6, column=1, padx=5, pady=5)

    tk.Button(root, text="Process Images", command=start_processing).grid(row=7, column=1, pady=10)

    root.mainloop()
