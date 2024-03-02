from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QImage, QPainter
import logging
import cv2

class ImageViewport(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_img = None
        self.resized_img = None

    def set_image(self, image_path):
        """
        Set the image for the object.

        Args:
            image_path (str): The path to the image file.

        Returns:
            None
        """
        try:
            # Open the image file 
            image = cv2.imread(image_path)

            if image is None:
                raise FileNotFoundError(f"Failed to load image: {image_path}")

            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Set the original_img attribute 
            self.original_img = image

            self.update_display()

        except FileNotFoundError as e:
            logging.error(e)
        except Exception as e:
            logging.error(f"Error displaying image: {e}")

    def update_display(self):
        if self.original_img is not None:
            self.repaint()

    def paintEvent(self, event):
        super().paintEvent(event)

        """
        Override the paintEvent method to draw the resized image on the widget.
        """

        if self.original_img is not None:
            painter_img = QPainter(self)
            height, width, _ = self.original_img.shape
            aspect_ratio = width / height

            # Resize the image while preserving aspect ratio
            target_width = min(self.width(), int(self.height() * aspect_ratio))
            target_height = min(self.height(), int(self.width() / aspect_ratio))
            resized_img = cv2.resize(self.original_img, (target_width, target_height))

            # Calculate the position to center the image
            x_offset = (self.width() - target_width) // 2
            y_offset = (self.height() - target_height) // 2

            # Convert image to QImage
            image = QImage(resized_img.data, resized_img.shape[1], resized_img.shape[0], resized_img.strides[0], QImage.Format.Format_RGB888)

            # Draw the image on the widget with the calculated offsets
            pixmap = QPixmap.fromImage(image)
            painter_img.drawPixmap(x_offset, y_offset, pixmap)


    def clear(self):
        self.original_img = None
        self.resized_img = None
        self.update_display()