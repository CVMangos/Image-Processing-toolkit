import numpy as np
import cv2

class Filter:
    def __init__(self, original_img, kernel_size):
        self.original_img = original_img
        self.kernel_size = kernel_size
        self.filtered_img = None

    def median_filter(self):
        # Ensure original_img is a numpy array
        data = np.array(self.original_img)
        # Calculate the index for the middle element of the filter
        indexer = self.kernel_size // 2
        # Create an empty numpy array to store the filtered data
        data_final = np.zeros_like(data)
        
        # Loop through the rows of the data
        for i in range(len(data)):
            # Loop through the columns of the data
            for j in range(len(data[0])):
                # Create an empty list to store the values within the kernel
                values = []
                # Loop through the kernel size
                for m in range(-indexer, indexer + 1):
                    for n in range(-indexer, indexer + 1):
                        # Calculate the row and column indices for the current position
                        row_index = i + m
                        col_index = j + n
                        # Check if the indices are within the bounds of the image
                        if 0 <= row_index < len(data) and 0 <= col_index < len(data[0]):
                            # Append the value from the data to the values list
                            values.append(data[row_index][col_index])
                        else:
                            # Append 0 for out-of-bounds positions
                            values.append(0)
                
                # Sort the values list
                values.sort()
                # Assign the median value from the values list to the corresponding position in the final data
                data_final[i][j] = values[len(values) // 2]
        
        # Update the filtered_img attribute with the filtered data
        self.filtered_img = data_final
        return self.filtered_img

    def gaussian_filter(self, frequency_response=255):
        """
        Apply Gaussian filter to the original image.

        Args:
            frequency_response (int): The maximum frequency response of the filter.
                                      Defaults to 255.

        Returns:
            numpy.ndarray: The filtered image.
        """
        # The sigma value controls the spread of the Gaussian function.
        # A larger value means a wider spread.
        sigma = 1

        # Generate a Gaussian kernel
        kernel = self._gaussian_kernel(self.kernel_size, sigma)

        # Scale the kernel by the maximum frequency response
        kernel *= frequency_response / 255

        # Apply the Gaussian filter using cv2.filter2D()
        self.filtered_img = cv2.filter2D(self.original_img, -1, kernel)

        return self.filtered_img

    def average_filter(self):
        """
        Apply average filter to the original image.

        This function applies an average filter to the original image
        using the specified kernel size.

        Returns:
            numpy.ndarray: The filtered image.
        """
        # Create a kernel with a constant value of 1/kernel_size^2
        kernel = np.ones((self.kernel_size, self.kernel_size)) / (self.kernel_size ** 2)

        # Apply average filter using cv2.filter2D()
        self.filtered_img = cv2.filter2D(self.original_img, -1, kernel)

        return self.filtered_img

    def _gaussian_kernel(self, size, sigma):
        """
        Generate a Gaussian kernel.

        This function generates a Gaussian kernel with a size of `size` x `size`
        and a standard deviation of `sigma`. The kernel is normalized to have
        a sum of 1.

        Args:
            size (int): The size of the kernel.
            sigma (float): The standard deviation of the Gaussian distribution.

        Returns:
            numpy.ndarray: The Gaussian kernel.
        """
        # Create a 2D Gaussian kernel using a numpy array
        kernel = np.fromfunction(lambda x, y: (1 / (2 * np.pi * sigma ** 2)) * np.exp(
            -(x - size // 2) ** 2 / (2 * sigma ** 2) - (y - size // 2) ** 2 / (2 * sigma ** 2)), (size, size))

        # Normalize the kernel so that the sum of all elements is 1
        kernel /= np.sum(kernel)

        return kernel
