import numpy as np
import cv2


class thresholding:
    def __init__(self, original_img):
        self.gray = cv2.convertScaleAbs(original_img)
        self.threshold = 120
        self.block_size = 11

    def global_thresholding(self):
        return np.where(self.gray > self.threshold, 255, 0).astype(np.uint8)
    
    def local_thresholding(self):
        # Create meshgrids for block indices with adjusted step size
        rows, cols = np.meshgrid(
            np.arange(0, self.gray.shape[0] - self.block_size + 1, self.block_size),
            np.arange(0, self.gray.shape[1] - self.block_size + 1, self.block_size),
            indexing='ij'
        )

        # Initialize the local thresholded image
        local_threshold = np.zeros_like(self.gray)

        # Iterate over each block
        for r, c in zip(rows.flatten(), cols.flatten()):
            # Extract the block
            block = self.gray[r:r + self.block_size, c:c + self.block_size]
            
            # Calculate the local threshold for the block using the mean
            threshold_value = np.mean(block) - 3
            
            # Apply binary thresholding to the block
            block_thresholded = np.where(block > threshold_value, 255, 0)
            
            # Update the local thresholded image with the thresholded block
            local_threshold[r:r + self.block_size, c:c + self.block_size] = block_thresholded

        return local_threshold.astype(np.uint8)

