import cv2
import numpy as np
import random
import math

class ScreenFX:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.shake_duration = 0
        self.shake_intensity = 0
        self.zoom_duration = 0
        self.fractures = []
        
        # Precompute a displacement map for the Blue gravity well
        self.warp_size = 300
        self.map_x, self.map_y = self._create_gravity_map(self.warp_size)

    def _create_gravity_map(self, size):
        x = np.arange(0, size, 1, np.float32)
        y = np.arange(0, size, 1, np.float32)
        X, Y = np.meshgrid(x, y)
        
        center = size / 2.0
        X_shift = X - center
        Y_shift = Y - center
        
        R = np.sqrt(X_shift**2 + Y_shift**2) + 1 
        pull = 400.0 / (R + 10.0) 
        
        map_x = X + (X_shift / R) * pull
        map_y = Y + (Y_shift / R) * pull
        
        mask = np.clip((size/2.0 - R) / 20.0, 0, 1)
        map_x = map_x * mask + X * (1 - mask)
        map_y = map_y * mask + Y * (1 - mask)
        
        return map_x, map_y

    def trigger_shake(self, duration=10, intensity=15):
        self.shake_duration = duration
        self.shake_intensity = intensity
        
    def trigger_zoom(self, duration=10):
        self.zoom_duration = duration
        
    def add_fracture(self, x, y):
        pts = []
        for _ in range(8):
            pts.append([int(x + random.uniform(-40, 40)), int(y + random.uniform(-40, 40))])
        self.fractures.append({
            'pts': np.array(pts, dtype=np.int32).reshape((-1, 1, 2)),
            'life': 100
        })
        
    def apply_bloom(self, img, intensity=0.5):
        # Downsample for rapidly faster blur
        small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        blurred = cv2.GaussianBlur(small, (21, 21), 0)
        upscaled = cv2.resize(blurred, (img.shape[1], img.shape[0]))
        return cv2.addWeighted(img, 1.0, upscaled, intensity, 0)
        
    def apply_gravity_warp(self, img, center):
        cx, cy = int(center[0]), int(center[1])
        half = self.warp_size // 2
        
        x1, y1 = cx - half, cy - half
        x2, y2 = cx + half, cy + half
        
        if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
            return img 
            
        roi = img[y1:y2, x1:x2]
        warped = cv2.remap(roi, self.map_x, self.map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        img[y1:y2, x1:x2] = warped
        
        return img

    def apply_fx(self, img):
        if self.shake_duration > 0:
            ox = random.randint(-self.shake_intensity, self.shake_intensity)
            oy = random.randint(-self.shake_intensity, self.shake_intensity)
            
            M = np.float32([[1, 0, ox], [0, 1, oy]])
            img = cv2.warpAffine(img, M, (self.w, self.h), borderMode=cv2.BORDER_REFLECT)
            self.shake_duration -= 1
            
        if self.zoom_duration > 0:
            zoom = 1.05 + 0.05 * (self.zoom_duration / 10.0)
            M = cv2.getRotationMatrix2D((self.w/2, self.h/2), 0, zoom)
            img = cv2.warpAffine(img, M, (self.w, self.h), borderMode=cv2.BORDER_REFLECT)
            self.zoom_duration -= 1
            
        alive_fractures = []
        for f in self.fractures:
            f['life'] -= 1
            if f['life'] > 0:
                alive_fractures.append(f)
                cv2.polylines(img, [f['pts']], isClosed=True, color=(150, 0, 150), thickness=2)
                cv2.fillPoly(img, [f['pts']], (0, 0, 0))
        self.fractures = alive_fractures
            
        return img
