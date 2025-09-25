import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from core import tasks
import config


def start_app():
    # Cria a janela principal com tema moderno
    root = ttk.Window(themename="flatly")
    root.title(config.APP_NAME)
    root.geometry("600x500")
    root.resizable(False, False)

    # Variáveis da GUI
    input_folder_var = ttk.StringVar()
    output_folder_var = ttk.StringVar()
    max_size_kb_var = ttk.StringVar(value=str(config.DEFAULT_MAX_SIZE_KB))
    quality_var = ttk.StringVar(value=str(config.DEFAULT_QUALITY))
    max_width_var = ttk.StringVar(value=str(config.DEFAULT_MAX_WIDTH))
    max_height_var = ttk.StringVar(value=str(config.DEFAULT_MAX_HEIGHT))
    format_var = ttk.StringVar(value=config.DEFAULT_FORMAT)

    # Funções
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

    # Layout moderno
    frm_main = ttk.Frame(root, padding=20)
    frm_main.pack(fill=BOTH, expand=True)

    # Input & Output folders
    ttk.Label(frm_main, text="Input Folder:").grid(row=0, column=0, sticky=W, pady=5)
    ttk.Entry(frm_main, textvariable=input_folder_var, width=45).grid(row=0, column=1, pady=5, padx=5)
    ttk.Button(frm_main, text="Select", bootstyle=SUCCESS, command=select_input_folder).grid(row=0, column=2, padx=5)

    ttk.Label(frm_main, text="Output Folder:").grid(row=1, column=0, sticky=W, pady=5)
    ttk.Entry(frm_main, textvariable=output_folder_var, width=45).grid(row=1, column=1, pady=5, padx=5)
    ttk.Button(frm_main, text="Select", bootstyle=SUCCESS, command=select_output_folder).grid(row=1, column=2, padx=5)

    # Settings frame
    frm_settings = ttk.LabelFrame(frm_main, text="Settings", padding=15)
    frm_settings.grid(row=2, column=0, columnspan=3, pady=15, sticky="ew")

    ttk.Label(frm_settings, text="Max Size (KB):").grid(row=0, column=0, sticky=W, pady=5)
    ttk.Entry(frm_settings, textvariable=max_size_kb_var, width=10).grid(row=0, column=1, pady=5)

    ttk.Label(frm_settings, text="Quality (1-100):").grid(row=1, column=0, sticky=W, pady=5)
    ttk.Entry(frm_settings, textvariable=quality_var, width=10).grid(row=1, column=1, pady=5)

    ttk.Label(frm_settings, text="Max Width:").grid(row=2, column=0, sticky=W, pady=5)
    ttk.Entry(frm_settings, textvariable=max_width_var, width=10).grid(row=2, column=1, pady=5)

    ttk.Label(frm_settings, text="Max Height:").grid(row=3, column=0, sticky=W, pady=5)
    ttk.Entry(frm_settings, textvariable=max_height_var, width=10).grid(row=3, column=1, pady=5)

    ttk.Label(frm_settings, text="Output Format:").grid(row=4, column=0, sticky=W, pady=5)
    ttk.Entry(frm_settings, textvariable=format_var, width=10).grid(row=4, column=1, pady=5)

    # Process button
    ttk.Button(frm_main, text="Process Images", bootstyle=PRIMARY, width=30, command=start_processing).grid(
        row=3, column=0, columnspan=3, pady=20
    )

    root.mainloop()


if __name__ == "__main__":
    start_app()
