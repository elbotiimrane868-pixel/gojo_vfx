import cv2
import numpy as np
import random
import math

class DomainExpansion:
    def __init__(self):
        self.active_frames = 0
        self.w, self.h = None, None
        self.map_x, self.map_y = None, None
        self.debris = []
        self.lut = self._create_LUT()
        
    def _init_resolution(self, img):
        self.h, self.w = img.shape[:2]
        self.map_x, self.map_y = self._build_fisheye_maps(self.w, self.h)
        for _ in range(60):
            self.debris.append({
                'x': random.randint(0, self.w),
                'y': random.randint(0, self.h),
                'vy': random.uniform(-1.0, -3.0),
                'size': random.randint(2, 6),
                'ch': random.choice([0, 1])
            })
            
    def _create_LUT(self):
        lut = np.zeros((256, 1, 3), dtype=np.uint8)
        for i in range(256):
            v = i
            if v < 60:
                b, g, r = v*0.5, v*0.2, v*0.1
            else:
                b = np.clip(v * 1.2, 0, 255)
                g = np.clip(v * 0.7, 0, 255)
                r = np.clip(v * 0.4, 0, 255)
            lut[i, 0] = [int(b), int(g), int(r)]
        return lut

    def _build_fisheye_maps(self, w, h):
        x_mesh, y_mesh = np.meshgrid(np.arange(w), np.arange(h))
        x_c, y_c = w / 2.0, h / 2.0
        
        x_norm = (x_mesh - x_c) / x_c
        y_norm = (y_mesh - y_c) / y_c
        r = np.sqrt(x_norm**2 + y_norm**2)
        
        distortion = 1.0 + 0.3 * (r**2) + 0.1 * (r**4)
        x_distorted = x_norm * distortion * x_c + x_c
        y_distorted = y_norm * distortion * y_c + y_c
        
        return x_distorted.astype(np.float32), y_distorted.astype(np.float32)

    def draw(self, img, fx_screen):
        if self.map_x is None:
            self._init_resolution(img)
            
        self.active_frames += 1
        if self.active_frames < 5:
            return np.zeros_like(img), True
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        tone_mapped = cv2.LUT(img, self.lut)
        
        edges_colored = cv2.merge([edges]*3)
        edges_colored[:,:,0] = edges 
        edges_colored[:,:,1] = edges//2 
        edges_colored[:,:,2] = edges//4 
        
        bld = cv2.addWeighted(tone_mapped, 0.6, edges_colored, 0.4, 0)
        warped = cv2.remap(bld, self.map_x, self.map_y, cv2.INTER_LINEAR)
        
        overlay = np.zeros_like(warped, dtype=np.uint8)
        for d in self.debris:
            d['y'] += d['vy']
            if d['y'] < 0:
                d['y'] = self.h
                d['x'] = random.randint(0, self.w)
                
            color = (255, 200, 100) if d['ch'] == 0 else (255, 255, 255)
            cv2.rectangle(overlay, (int(d['x']), int(d['y'])), (int(d['x']+d['size']), int(d['y']+d['size'])), color, -1)

        final = cv2.add(warped, overlay)
        
        mask = np.zeros((self.h, self.w), dtype=np.float32)
        cv2.circle(mask, (self.w//2, self.h//2), int(min(self.w, self.h)*0.55), 1.0, -1)
        mask = cv2.GaussianBlur(mask, (151, 151), 0)
        mask = np.dstack([mask]*3)
        
        final = (final * mask).astype(np.uint8)
        return final, False

    def reset(self):
        self.active_frames = 0
