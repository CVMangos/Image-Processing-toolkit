import numpy as np
from Filters import Filter

class Hybrid:
    def __init__(self):
        self.filtered_img_one = None
        self.filtered_img_two = None

    def low_pass(self, image, freq_response):
        filtered = Filter(image, 3)
        filtered.gaussian_filter(freq_response)
        self.filtered_img_one = filtered.filtered_img
        return self.filtered_img_one
    
    def high_pass(self, image, freq_response):
        filtered = Filter(image, 3)
        filtered.gaussian_filter(freq_response)   
        self.filtered_img_two = filtered.original_img - filtered.filtered_img
        return self.filtered_img_two
