import cv2
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QVBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import sys

# from cv2.linemod import Detector
from Edge_Detector import EdgeDetector
from imageViewPort import ImageViewport
from filterNoiseClass import FilterNoise
from functools import partial


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.reset_buttons = None
        self.clear_buttons = None
        self.import_buttons = None
        self.ui_out_ports = None
        self.ui_view_ports = None
        self.out_ports = None
        self.input_ports = None
        self.ui = None
        self.original_img = None
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI by loading the UI page, setting the window title, loading UI elements, and checking a specific UI element.
        """
        # Load the UI Page
        self.ui = uic.loadUi('Mainwindow.ui', self)
        self.setWindowTitle("Image Processing ToolBox")
        self.setWindowIcon(QIcon("icons/image-layer-svgrepo-com.png"))
        self.load_ui_elements()
        self.ui.kernalSize_3.setChecked(True)
        self.ui.medianFilter.clicked.connect(partial(self.apply_filter, filter_type="median_filter"))
        self.ui.averageFilter.clicked.connect(partial(self.apply_filter, filter_type="average_filter"))
        self.ui.gaussianFilter.clicked.connect(partial(self.apply_filter, filter_type="gaussian_filter"))
        self.ui.sobelEdge.clicked.connect(partial(self.apply_edge_detector, detector_type="sobel_detector"))
        self.ui.robertsEdge.clicked.connect(partial(self.apply_edge_detector, detector_type="roberts_detector"))
        self.ui.cannyEdge.clicked.connect(partial(self.apply_edge_detector, detector_type="canny_detector"))
        self.ui.prewittEdge.clicked.connect(partial(self.apply_edge_detector, detector_type="prewitt_detector"))

    def load_ui_elements(self):
        """
        Load UI elements and set up event handlers.
        """
        # Initialize input and output port lists
        self.input_ports = []
        self.out_ports = []

        # Define lists of original UI view ports, output ports
        self.ui_view_ports = [self.ui.filterInput, self.ui.edgeInput,
                              self.ui.thresholdInput, self.ui.hybridIntput1, self.ui.hybridIntput2]

        self.ui_out_ports = [self.ui.filterOutput, self.ui.edgeOutput,
                             self.ui.thresholdOutput, self.ui.hybridOutput1, self.ui.hybridOutput2]

        # Create image viewports for input ports and bind browse_image function to the event
        self.input_ports.extend([
            self.create_image_viewport(self.ui_view_ports[i], lambda event, index=i: self.browse_image(event, index))
            for i in range(5)])

        # Create image viewports for output ports
        self.out_ports.extend(
            [self.create_image_viewport(self.ui_out_ports[i], mouse_double_click_event_handler=None) for i in range(5)])

        # Initialize import buttons
        self.import_buttons = [self.ui.importButton, self.ui.importButton_2,
                               self.ui.importButton_3, self.ui.importButton_hybrid1, self.ui.importButton_hybrid2]

        # Bind browse_image function to import buttons
        self.bind_buttons(self.import_buttons, self.browse_image)

        # Initialize clear buttons
        self.clear_buttons = [self.ui.clearButton, self.ui.clearButton_2,
                              self.ui.clearButton_3]

        # Bind clear_image function to clear buttons
        self.bind_buttons(self.clear_buttons, self.clear_image)

        # Initialize reset buttons
        self.reset_buttons = [self.ui.resetButton, self.ui.resetButton_2,
                              self.ui.resetButton_3]

        # Bind reset_image function to reset buttons
        self.bind_buttons(self.reset_buttons, self.reset_image)

    def bind_buttons(self, buttons, function):
        """
        Bind a function to a list of buttons.

        Args:
            buttons (list): List of buttons to bind the function to.
            function (callable): The function to bind to the buttons.

        Returns:
            None
        """
        for i, button in enumerate(buttons):
            button.clicked.connect(lambda event, index=i: function(event, index))

    def browse_image(self, event, index: int):
        """
        Browse for an image file and set it for the ImageViewport at the specified index.

        Args:
            event: The event that triggered the image browsing.
            index: The index of the ImageViewport to set the image for.
        """
        file_filter = "Raw Data (*.png *.jpg *.jpeg *.jfif)"
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', './', filter=file_filter)

        if image_path and 0 <= index < len(self.input_ports):
            # Get the input port at the specified index
            input_port = self.input_ports[index]
            output_port = self.out_ports[index]

            # Set the image for the input port
            input_port.set_image(image_path)

            # outport image will always be grayscale
            output_port.set_image(image_path, grey_flag=True)

    def create_viewport(self, parent, viewport_class, mouse_double_click_event_handler=None):
        """
        Creates a viewport of the specified class and adds it to the specified parent widget.

        Args:
            parent: The parent widget to which the viewport will be added.
            viewport_class: The class of the viewport to be created.
            mouse_double_click_event_handler: The event handler function to be called when a mouse double-click event occurs (optional).

        Returns:
            The created viewport.

        """
        # Create a new instance of the viewport_class
        new_port = viewport_class(self)

        # Create a QVBoxLayout with parent as the parent widget
        layout = QVBoxLayout(parent)

        # Add the new_port to the layout
        layout.addWidget(new_port)

        # If a mouse_double_click_event_handler is provided, set it as the mouseDoubleClickEvent handler for new_port
        if mouse_double_click_event_handler:
            new_port.mouseDoubleClickEvent = mouse_double_click_event_handler

        # Return the new_port instance
        return new_port

    def create_image_viewport(self, parent, mouse_double_click_event_handler):
        """
        Creates an image viewport within the specified parent with the provided mouse double click event handler.
        """
        return self.create_viewport(parent, ImageViewport, mouse_double_click_event_handler)

    def clear_image(self, event, index: int):
        """
        Clears the image at the specified index in the input_ports list.

        Args:
            event: The event triggering the image clearing.
            index (int): The index of the image to be cleared in the input_ports list.
        """
        self.input_ports[index].clear()
        self.out_ports[index].clear()

    def reset_image(self, event, index: int):
        """
        Resets the image at the specified index in the input_ports list.

        Args:
            event: The event triggering the image clearing.
            index (int): The index of the image to be cleared in the input_ports list.
        """
        self.input_ports[index].reset()

    def apply_filter(self, filter_type):
        """
        Apply median filter to the image and update the output port with the filtered image.
        """
        output_port = self.out_ports[1]
        img = output_port.resized_img
        if img is None or img.size == 0:
            print("Error: Empty or None image received.")
            return

        filter = FilterNoise(img)
        try:
            filter_method = getattr(filter, filter_type)
            filtered_image = filter_method()
            output_port.original_img = filtered_image
            output_port.update_display()
        except Exception as e:
            print(f"Error applying median filter: {e}")

    def apply_edge_detector(self, detector_type):
        self.original_img = cv2.cvtColor(self.input_ports[1].resized_img.copy(), cv2.COLOR_BGR2GRAY)
        output_port = self.out_ports[1]
        img = self.original_img
        if img is None or img.size == 0:
            print("Error: Empty or None image received.")
            return

        detector = EdgeDetector(img)
        try:
            detect = getattr(detector, detector_type)
            detected_edges = detect()
            output_port.original_img = detected_edges
            output_port.update_display()
        except Exception as e:
            print(f"Error Detecting edges: {e}")


def main():
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
