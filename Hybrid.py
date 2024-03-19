import numpy as np
from Filters import Filter
import cv2
from numpy.fft import fft2, ifft2, fftshift, ifftshift

class Hybrid:
    def __init__(self):
        self.filtered_img_one = None
        self.filtered_img_two = None

    def low_pass(self, image, smoothing_degree):
        """
        Applies a low-pass filter to the given image using the
        Butterworth low-pass filter.

        Parameters:
            image: The image to apply the filter to.
            smoothing_degree: The degree of smoothing.

        Returns:
            The low-pass filtered image.
        """
        # Compute the 2D discrete Fourier Transform of the image
        fft_img = fftshift(fft2(image))

        # Get the image dimensions
        rows, cols = image.shape

        # Compute the center of the image
        crow, ccol = rows // 2, cols // 2

        # Set the cutoff frequency
        cutoff_frequency = 10

        # Convert the smoothing degree to a normalized value
        smoothing_degree = (smoothing_degree + 1) / 25.6

        # Create a 2D mask for the low-pass filter
        mask = np.zeros((rows, cols), np.float32)
        for i in range(rows):
            for j in range(cols):
                # Compute the distance between the current pixel and the center
                distance = np.sqrt((i - crow)**2 + (j - ccol)**2)

                # Apply the low-pass filter to the current pixel
                mask[i, j] = np.exp(-0.5 * (distance / cutoff_frequency) ** smoothing_degree)

        # Apply the low-pass filter to the image
        low_pass_fft = fft_img * mask

        # Compute the inverse 2D discrete Fourier Transform
        low_pass = ifft2(ifftshift(low_pass_fft))

        # Store the filtered image
        self.filtered_img_one = low_pass

        # Get the absolute value of the filtered image
        low_pass = np.abs(low_pass)

        # Normalize the filtered image
        low_pass = normalize_image(low_pass)

        # Convert the filtered image to 8-bit integer
        low_pass = low_pass.astype(np.uint8)

        # Return the low-pass filtered image
        return low_pass
    
    
    def high_pass(self, image, edge_degree):
        """
        Applies a high-pass filter to the given image using the
        Butterworth high-pass filter.

        Parameters:
            image: The image to apply the filter to.
            edge_degree: The degree of edge enhancement.

        Returns:
            The high-pass filtered image.
        """
        # Compute the 2D discrete Fourier Transform of the image
        fft_img = fftshift(fft2(image))

        # Get the image dimensions
        rows, cols = image.shape

        # Compute the center of the image
        crow, ccol = rows // 2, cols // 2

        # Set the cutoff frequency
        cutoff_frequency = 10

        # Convert the edge degree to a normalized value
        edge_degree = (edge_degree + 1) / 25.6

        # Create a 2D mask for the high-pass filter
        mask = np.zeros((rows, cols), np.float32)
        for i in range(rows):
            for j in range(cols):
                # Compute the distance between the current pixel and the center
                distance = np.sqrt((i - crow)**2 + (j - ccol)**2)

                # Apply the high-pass filter to the current pixel
                mask[i, j] = 1 - np.exp(-0.5 * (distance / cutoff_frequency) ** edge_degree)

        # Apply the high-pass filter to the image
        high_pass_fft = fft_img * mask

        # Compute the inverse 2D discrete Fourier Transform
        high_pass = ifft2(ifftshift(high_pass_fft))

        # Store the filtered image
        self.filtered_img_two = high_pass

        # Get the absolute value of the filtered image
        high_pass = np.abs(high_pass)

        # Normalize the filtered image
        high_pass = normalize_image(high_pass)

        # Convert the filtered image to 8-bit integer
        high_pass = high_pass.astype(np.uint8)

        # Return the high-pass filtered image
        return high_pass


    def generate_hybrid(self):
        """
        Generate hybrid image using the high-pass and low-pass filtered images.

        Returns
        -------
        hybrid_image : ndarray
            Hybrid image after combining the high-pass and low-pass filtered images.
        """
        img1 = self.filtered_img_one
        img2 = self.filtered_img_two
        if img1 is None or img2 is None:
            return
        # Resize the images to the minimum of their height and width if necessary
        if img2.shape != img1.shape:
            min_height = min(img1.shape[0], img2.shape[0])
            min_width = min(img1.shape[1], img2.shape[1])
            img1 = resize_complex_array(img1, (min_width, min_height))
            img2 = resize_complex_array(img2, (min_width, min_height))
        # Combine the high-pass and low-pass filtered images to generate the hybrid image
        hybrid_image = np.abs(img1 + img2)
        # Normalize and convert the hybrid image to 8-bit integer
        hybrid_image = normalize_image(hybrid_image).astype(np.uint8)
        return hybrid_image
    

def normalize_image(image):
    """
    Normalize the pixel values of an image to the range [0, 255].

    Parameters
    ----------
    image : ndarray
        Input image to be normalized.

    Returns
    -------
    normalized_image : ndarray
        Normalized image with pixel values in the range [0, 255].
    """
    # Get the minimum and maximum pixel values
    min_val = np.min(image)
    max_val = np.max(image)

    # Check if min_val and max_val are equal
    if min_val == max_val:
        return image

    # Perform normalization
    normalized_image = ((image - min_val) / (max_val - min_val)) * 255

    # Convert the normalized image to 8-bit integer type
    normalized_image = normalized_image.astype(np.uint8)

    return normalized_image

def resize_complex_array(complex_array, new_shape):
    """
    Resize a complex-valued image to a new shape.

    Parameters
    ----------
    complex_array : ndarray
        Input complex-valued image.
    new_shape : tuple
        New shape of the output image.

    Returns
    -------
    resized_complex_array : ndarray
        Resized complex-valued image.
    """

    # Get real and imaginary parts of the input image
    real_part = np.real(complex_array)
    imag_part = np.imag(complex_array)

    # Resize the real and imaginary parts of the image separately
    resized_real_part = cv2.resize(real_part, new_shape[::-1])
    resized_imag_part = cv2.resize(imag_part, new_shape[::-1])

    # Combine the resized real and imaginary parts to form the resized complex image
    resized_complex_array = resized_real_part + 1j * resized_imag_part

    return resized_complex_array
