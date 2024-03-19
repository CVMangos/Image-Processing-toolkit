import numpy as np
import cv2


class thresholding:
    def __init__(self, original_img):
        self.gray = cv2.convertScaleAbs(original_img)
        self.threshold = 127
        self.block_size = 11

    def global_thresholding(self):
        """
        Applies global thresholding to the image.

        Global thresholding is a simple thresholding algorithm where all pixels with a
        grayscale value above the threshold are set to white (255), and all pixels with
        a grayscale value below the threshold are set to black (0).

        Returns:
            thresholded_image (ndarray): thresholded image
        """
        return np.where(self.gray > self.threshold, 255, 0).astype(np.uint8)

    def local_thresholding(self):
        """
        Applies local thresholding to the image.

        Local thresholding is an adaptive thresholding algorithm that divides the image into smaller blocks and computes a
        local threshold for each block based on the mean of the grayscale values in that block. The pixels in each block are
        then thresholded based on their grayscale values relative to the local threshold.

        Returns:
            local_thresholded_image (ndarray): local thresholded image
        """
        # Create meshgrids for block indices with adjusted step size
        rows, cols = np.meshgrid(np.arange(0, self.gray.shape[0] - self.block_size + 1, self.block_size),
                                 np.arange(0, self.gray.shape[1] - self.block_size + 1, self.block_size),
                                 indexing='ij')
        
        # Extract blocks and compute local thresholds
        blocks = np.array([self.gray[r:r + self.block_size, c:c + self.block_size] for r, c in zip(rows.flatten(), cols.flatten())])
        threshold_values = np.mean(blocks, axis=(1, 2))  # Compute local thresholds for each block

        # Apply local thresholding using vectorized operations
        local_threshold = np.zeros_like(self.gray)
        for (r, c), block, threshold_value in zip(zip(rows.flatten(), cols.flatten()), blocks, threshold_values):
            local_threshold[r:r + self.block_size, c:c + self.block_size] = np.where(block > threshold_value, 255, 0)  # Threshold each block

        return local_threshold.astype(np.uint8)
