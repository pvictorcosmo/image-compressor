# Image Compressor & Resizer
> A modern tool to resize, compress, convert, and process images efficiently.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Pillow Downloads](https://img.shields.io/pypi/dm/Pillow.svg)](https://pypi.org/project/Pillow/)

This project was created to solve a real problem at work: handling large sets of images that needed to be resized, compressed, converted, and processed for web and mobile applications without losing quality. The tool allows you to **batch process multiple images**, automatically resizing them to a maximum resolution, compressing them to a target file size, and converting between formats (WebP, PNG, JPEG). It is designed to save time, optimize storage, and ensure consistency when managing image assets.

![](header.png)

## Installation

Clone the repository:

```sh
git clone https://github.com/yourusername/image-compressor-resizer.git
cd image-compressor-resizer
```

Create a virtual environment (recommended) and install dependencies:

```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Usage example

Run the GUI application:

```sh
python gui.py
```

1. Select the input folder containing the images.
2. Select the output folder where processed images will be saved.
3. Adjust settings such as maximum file size, quality, resolution, and output format.
4. Click "Process Images" to start batch processing.

This tool is suitable for developers, designers, and anyone who needs to **resize, compress, convert, and process images** efficiently for web or mobile applications.

## Meta

**Paulo Victor Cosmo** – [LinkedIn](https://www.linkedin.com/in/paulo-victor-cosmo-batista-537047218/) – pvictorcosmo@gmail.com

Distributed under the MIT license. See `LICENSE` for more information.

[Project Repository](https://github.com/pvictorcosmo/image-compressor)


## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
