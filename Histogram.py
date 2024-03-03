import numpy as np
import cv2
class Histogram:
    def __init__(self, original_img):
        self.image = cv2.convertScaleAbs(original_img)

    def get_histograms(self):
        # Separate the R, G, and B channels
        R = self.image[..., 0]
        G = self.image[..., 1]
        B = self.image[..., 2]

        # Calculate the histograms for R, G, and B channels
        hist_R, bins_R = np.histogram(R.flatten(), bins=256, range=(0, 256))
        hist_G, bins_G = np.histogram(G.flatten(), bins=256, range=(0, 256))
        hist_B, bins_B = np.histogram(B.flatten(), bins=256, range=(0, 256))

        # Calculate the cumulative distribution functions (CDFs) for R, G, and B channels
        cdf_R = hist_R.cumsum()
        cdf_G = hist_G.cumsum()
        cdf_B = hist_B.cumsum()

        return {"R": [hist_R, cdf_R], "G": [hist_G, cdf_G], "B": [hist_B, cdf_B]}