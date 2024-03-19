# Image Processing Toolbox

## Overview

The Image Processing Toolbox is a comprehensive toolkit for various image processing tasks, including filtering, noise generation, edge detection, histogram manipulation, and hybrid image generation.

## Features

### Filter Class
Apply different types of filters such as median, Gaussian, and average filters to remove noise and enhance image quality.

### Noise Class
Add different types of noise like salt and pepper noise, Gaussian noise, and uniform noise to simulate real-world scenarios and test algorithms.

### EdgeDetector Class
Implement various edge detection algorithms including Sobel, Roberts, Canny, and Prewitt for identifying edges and boundaries within an image.

### Decoding Class
Perform histogram equalization and image normalization to improve contrast and appearance, facilitating better analysis and interpretation.

### Thresholding Class
Segment images into regions of interest using global and local thresholding algorithms, crucial for tasks like image segmentation.

### Hybrid Class
Create hybrid images by blending low-pass and high-pass filtered images to produce visually interesting effects.

## User Interface (UI) Details

The UI of the Image Processing Toolbox provides an intuitive interface for users to interact with the various image processing functionalities. Here are some key components and functionalities of the UI:

- **Main Window:** The main window of the application displays the toolbox's title and icon, providing easy access to the image processing tools.

- **Tool Selection:** Users can select different image processing tools, such as filters, noise generation, edge detection, histogram manipulation, and hybrid image generation, using tabs or dropdown menus.

- **Image Input:** Users can browse and select input images using file dialogs. The selected images are displayed in input viewports for visualization and processing.

- **Image Output:** Processed images are displayed in output viewports, allowing users to compare the results with the original images.

- **Interactive Controls:** Interactive controls, such as buttons, sliders, and combo boxes, are provided for applying different image processing operations, changing parameter settings, and generating hybrid images.

- **Histogram Visualization:** Histograms and distribution plots of input images are displayed for visual analysis and comparison. Users can observe changes in image characteristics after applying certain operations.


## Getting Started

1. **Installation**: To run the application, you need to have the required Python packages installed. You can create a virtual environment and install the necessary dependencies listed in the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Application**: Run the application using Python. The GUI will open, allowing you to load, process, and analyze signals.

   ```bash
   python main.py
   ```