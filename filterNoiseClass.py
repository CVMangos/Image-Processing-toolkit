import cv2


##################################################################################
# Basic implementation, will be contuined tomorrow 
##################################################################################
class FilterNoise:
    def __init__(self, original_img):
        self.original_img = original_img
        self.filtered_img = None

    def median_filter(self):
        self.filtered_img = cv2.medianBlur(self.original_img, 5)
        return self.filtered_img

    def gaussian_filter(self):
        self.noisy_img2 = cv2.GaussianBlur(self.original_img, (5, 5), 0)
        return self.noisy_img2
    
    def average_filter(self, kernel_size=5):
        self.filtered_img = cv2.blur(self.original_img, (kernel_size, kernel_size))
        return self.filtered_img