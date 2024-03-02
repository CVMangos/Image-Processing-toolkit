from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QVBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from imageViewPort import ImageViewport
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface by loading the UI page, setting the window title and icon,
        initializing various attributes, connecting signals to slots, loading UI elements, and 
        setting the window to full screen.

        Parameters:
            None

        Returns:
            None

        """
        # Load the UI Page
        self.ui = uic.loadUi('Mainwindow.ui', self)
        self.setWindowTitle("Image Processing ToolBox")
        # self.setWindowIcon(QIcon("icons/mixer.png"))
        self.load_ui_elements()
        self.ui.kernalSize_3.setChecked(True)

    def load_ui_elements(self):

        self.input_ports = []
        self.out_ports = []

        # Define lists of original UI view ports, output ports
        self.ui_view_ports = [self.ui.filterInput, self.ui.edgeInput,
                              self.ui.thresholdInput, self.ui.hybridIntput1, self.ui.hybridIntput2]
        
        self.ui_out_ports = [self.ui.filterOutput, self.ui.edgeOutput,
                              self.ui.thresholdOutput, self.ui.hybridOutput1, self.ui.hybridOutput2]
        
        # Create image viewports and bind browse_image function to the event
        self.input_ports.extend([
            self.create_image_viewport(self.ui_view_ports[i], lambda event, index=i: self.browse_image(event, index)) for i in range(5)])

        # Create output viewports
        self.out_ports.extend([self.create_image_viewport(self.ui_out_ports[i], mouse_double_click_event_handler=None) for i in range(5)])

        # Create import buttons
        self.import_buttons = [self.ui.importButton, self.ui.importButton_2,
                               self.ui.importButton_3, self.ui.importButton_hybrid1, self.ui.importButton_hybrid2]
        
        for i in range(len(self.import_buttons)):
            self.import_buttons[i].clicked.connect(lambda event, index=i: self.browse_image(event, index))



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
            image_port = self.input_ports[index]
            image_port.set_image(image_path)


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
        new_port = viewport_class(self)
        layout = QVBoxLayout(parent)
        layout.addWidget(new_port)

        if mouse_double_click_event_handler:
            new_port.mouseDoubleClickEvent = mouse_double_click_event_handler

        return new_port

    def create_image_viewport(self, parent, mouse_double_click_event_handler):
        return self.create_viewport(parent, ImageViewport, mouse_double_click_event_handler)
    

    
def main():
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
