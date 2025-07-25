import cv2
from ultralytics import YOLO
import numpy as np
import torch

class CustomerSegmentationWithYolo():
    def __init__(self, erode_size=5, erode_intensity=2):
        self.model = YOLO("yolov8n-seg.pt")
        self.erode_size = erode_size
        self.erode_intensity = erode_intensity
        self.background_image = cv2.imread("static/DEFAULT-PNG.jpg")

    def generate_mask_from_result(self, results):
        for result in results:
            if result.masks:
                masks = result.masks.data
                boxes = result.boxes.data

                clss = boxes[:, 5]

                people_indices = torch.where(clss == 0)

                people_masks = masks[people_indices]

                if len(people_masks) > 0:
                    return None

                people_mask = torch.any(people_masks, dim=0).to(torch.uint8) * 255

                kernel = np.ones((self.erode_size, self.erode_size), np.uint8)
                eroded_mask = cv2.erode(people_mask.cpu().numpy(), kernel, iterations=self.erode_intensity)

                return eroded_mask
            else:
                return None
            
    def apply_blur_with_mask(self, frame, mask, blur_strength=21):
        blur_strength = (blur_strength, blur_strength)
        blurred_frame = cv2.GaussianBlur(frame, blur_strength, 0)

        #ensure mask is binary
        mask = (mask > 0).astype(np.uint8)

        # expand mask to three channels
        mask_3d = cv2.merge([mask, mask, mask])

        # combine the blurred frame and the original frame
        result_frame = np.where(mask_3d == 1, blurred_frame, frame) 

        return result_frame
    
    def apply_black_background(self, frame, mask):
        # create a black background
        black_background = np.zeros_like(frame)

        #apply the mask
        result_frame = np.where(mask[:, :, np.newaxis] == 255, black_background, frame)
        return result_frame
