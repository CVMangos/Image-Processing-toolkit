import cv2
import numpy as np


class EdgeDetector:
    def __init__(self, original_img):
        self.gray = cv2.convertScaleAbs(original_img)

    def sobel_detector(self):
        """
        Compute the gradient of an image using the Sobel operator.

        The Sobel operator is defined as:

            G_x = [1 0 -1]
                  [2 0 -2]
                  [1 0 -1]

        and:

            G_y = [1 2 1]
                  [0 0 0]
                  [-1 -2 -1]

        The gradient magnitude is computed as the Euclidean norm of the gradient vector
        (magnitude = sqrt(G_x^2 + G_y^2)). The resulting gradient magnitude image is
        scaled to fit in the range [0, 255]

        Returns:
            gradient_magnitude (ndarray): image of gradient magnitude values
        """

        # Define Sobel kernels
        sobel_x = np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]])

        sobel_y = np.array([[-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1]])

        # Convolve the image with the kernels
        gradient_x = cv2.filter2D(self.gray, -1, sobel_x)
        gradient_y = cv2.filter2D(self.gray, -1, sobel_y)

        # Compute gradient magnitude
        gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

        # Scale gradient magnitude to fit in range [0, 255]
        gradient_magnitude *= 255.0 / gradient_magnitude.max()

        return gradient_magnitude.astype(np.uint8)


    def roberts_detector(self):
        """
        Compute the gradient of an image using the Roberts operator.

        The Roberts operator is defined as:

            G_x = [1 0]
                  [0 -1]

        and:

            G_y = [0 1]
                  [-1 0]

        The gradient magnitude is computed as the Euclidean norm of the gradient vector
        (magnitude = sqrt(G_x^2 + G_y^2)). The resulting gradient magnitude image is
        scaled to fit in the range [0, 255]

        Returns:
            gradient_magnitude (ndarray): image of gradient magnitude values
        """
        kernel_x = np.array([[1, 0], [0, -1]])
        kernel_y = np.array([[0, 1], [-1, 0]])

        roberts_x = cv2.filter2D(self.gray, -1, kernel_x)
        roberts_y = cv2.filter2D(self.gray, -1, kernel_y)
        roberts = np.sqrt(roberts_x ** 2 + roberts_y ** 2)

        return roberts.astype(np.uint8)


    def canny_detector(self):
        """
        Compute the Canny edge detector on the image.

        The Canny edge detector is based on the following steps:

        1. Apply Gaussian blur to reduce noise
        2. Compute gradient magnitude and direction
        3. Non-maximum suppression: only keep the points where the gradient magnitude is
           the largest in a particular direction
        4. Hysteresis thresholding: keep only the points that have a strong gradient
           magnitude (above high threshold) and have a neighboring point with a gradient
           magnitude above the low threshold

        Returns:
            edge_image (ndarray): image of edge pixels
        """
        # Step 2: Apply Gaussian blur
        blurred_image = cv2.GaussianBlur(self.gray, (5, 5), 0)
        low_threshold = 5
        high_threshold = 20
        # Step 3: Compute gradient magnitude and direction
        gradient_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
        gradient_direction = np.arctan2(gradient_y, gradient_x) * (180 / np.pi)

        # Step 4: Non-maximum suppression
        suppressed_image = np.zeros_like(gradient_magnitude)
        for i in range(1, gradient_magnitude.shape[0] - 1):
            for j in range(1, gradient_magnitude.shape[1] - 1):
                angle = gradient_direction[i, j]
                if (0 <= angle < 22.5) or (157.5 <= angle <= 180) or (-22.5 <= angle < 0) or (-180 <= angle < -157.5):
                    if (gradient_magnitude[i, j] >= gradient_magnitude[i, j - 1]) and \
                            (gradient_magnitude[i, j] >= gradient_magnitude[i, j + 1]):
                        suppressed_image[i, j] = gradient_magnitude[i, j]
                elif (22.5 <= angle < 67.5) or (-157.5 <= angle < -112.5):
                    if (gradient_magnitude[i, j] >= gradient_magnitude[i - 1, j - 1]) and \
                            (gradient_magnitude[i, j] >= gradient_magnitude[i + 1, j + 1]):
                        suppressed_image[i, j] = gradient_magnitude[i, j]
                elif (67.5 <= angle < 112.5) or (-112.5 <= angle < -67.5):
                    if (gradient_magnitude[i, j] >= gradient_magnitude[i - 1, j]) and \
                            (gradient_magnitude[i, j] >= gradient_magnitude[i + 1, j]):
                        suppressed_image[i, j] = gradient_magnitude[i, j]
                elif (112.5 <= angle < 157.5) or (-67.5 <= angle < -22.5):
                    if (gradient_magnitude[i, j] >= gradient_magnitude[i - 1, j + 1]) and \
                            (gradient_magnitude[i, j] >= gradient_magnitude[i + 1, j - 1]):
                        suppressed_image[i, j] = gradient_magnitude[i, j]

        # Step 5: Hysteresis thresholding
        edge_image = np.zeros_like(suppressed_image)
        weak_edges = (suppressed_image > low_threshold) & (suppressed_image <= high_threshold)
        strong_edges = suppressed_image > high_threshold
        edge_image[strong_edges] = 255
        for i in range(1, edge_image.shape[0] - 1):
            for j in range(1, edge_image.shape[1] - 1):
                if weak_edges[i, j]:
                    if np.any(strong_edges[i - 1:i + 2, j - 1:j + 2]):
                        edge_image[i, j] = 255

        return edge_image.astype(np.uint8)

    def prewitt_detector(self):
        """
        Compute the gradient of an image using the Prewitt operator.

        The Prewitt operator is defined as:

            G_x = [(-1, 0, 1), (-1, 0, 1), (-1, 0, 1)]
                  [(-1, -1, -1), (0, 0, 0), (1, 1, 1)]

        The gradient magnitude is computed as the Euclidean norm of the gradient vector
        (magnitude = sqrt(G_x^2 + G_y^2)). The resulting gradient magnitude image is
        scaled to fit in the range [0, 255]

        Returns:
            gradient_magnitude (ndarray): image of gradient magnitude values
        """
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        prewitt_x = cv2.filter2D(self.gray, -1, kernel_x)
        prewitt_y = cv2.filter2D(self.gray, -1, kernel_y)
        prewitt = np.sqrt(prewitt_x ** 2 + prewitt_y ** 2)

        return prewitt.astype(np.uint8)
        return prewitt.astype(np.uint8)
