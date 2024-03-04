import numpy as np

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

    def gaussian_filter(self):
        """
        Apply Gaussian filter to the original image.
        """
        sigma = 1
        kernel = self._gaussian_kernel(self.kernel_size, sigma)

        self.filtered_img = self._apply_filter(kernel)

        return self.filtered_img

    def average_filter(self):
        """
        Apply average filter to the original image.
        """
        kernel = np.ones((self.kernel_size, self.kernel_size)) / (self.kernel_size ** 2)

        self.filtered_img = self._apply_filter(kernel)

        return self.filtered_img

    def _gaussian_kernel(self, size, sigma):
        """
        Generate a Gaussian kernel.
        """
        kernel = np.fromfunction(lambda x, y: (1 / (2 * np.pi * sigma ** 2)) * np.exp(
            -(x - size // 2) ** 2 / (2 * sigma ** 2) - (y - size // 2) ** 2 / (2 * sigma ** 2)), (size, size))
        kernel /= np.sum(kernel)
        return kernel

    def _apply_filter(self, kernel):
        """
        Apply a given kernel filter to the original image.
        """
        pad_width = self.kernel_size // 2
        padded_img = np.pad(self.original_img, pad_width, mode='constant')

        filtered_img = np.zeros_like(self.original_img)

        for i in range(pad_width, padded_img.shape[0] - pad_width):
            for j in range(pad_width, padded_img.shape[1] - pad_width):
                neighbors = padded_img[i - pad_width:i + pad_width + 1, j - pad_width:j + pad_width + 1]
                filtered_value = np.sum(neighbors * kernel)
                filtered_img[i - pad_width, j - pad_width] = filtered_value

        return filtered_img