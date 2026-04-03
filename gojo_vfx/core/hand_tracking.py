import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_con=0.7, tracking_con=0.7, smoothing_factor=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.smoothing_factor = smoothing_factor

        base_options = python.BaseOptions(model_asset_path='core/hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=self.max_hands,
            min_hand_detection_confidence=detection_con,
            min_tracking_confidence=tracking_con
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        # Previous positions for smoothing (EMA)
        self.prev_landmarks = {}
        self.results = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        self.results = self.detector.detect(mp_image)
        # Tracking drawing is disabled for cinematic feel.
        return img

    def get_positions(self, img):
        hand_info = []
        if self.results and self.results.hand_landmarks:
            for i, hand_lms in enumerate(self.results.hand_landmarks):
                label = self.results.handedness[i][0].category_name
                
                lm_list = []
                h, w, c = img.shape
                
                cx_sum, cy_sum = 0, 0

                for id, lm in enumerate(hand_lms):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    key = f"{label}_{id}"
                    if key in self.prev_landmarks:
                        px, py = self.prev_landmarks[key]
                        cx = int(self.smoothing_factor * px + (1 - self.smoothing_factor) * cx)
                        cy = int(self.smoothing_factor * py + (1 - self.smoothing_factor) * cy)
                    
                    self.prev_landmarks[key] = (cx, cy)
                    lm_list.append([id, cx, cy])

                    if id in [0, 5, 9, 13, 17]:
                        cx_sum += cx
                        cy_sum += cy
                
                center_x = cx_sum // 5
                center_y = cy_sum // 5

                hand_info.append({
                    'label': label,
                    'lmList': lm_list,
                    'center': (center_x, center_y)
                })

        return hand_info
