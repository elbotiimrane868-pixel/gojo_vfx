import cv2
import numpy as np
import random
import math

class RedEffect:
    def __init__(self, color=(50, 50, 255)):
        self.color = color
        self.noise_offset = random.random() * 100
        
    def draw(self, img, center, particle_system, fx_screen):
        if not center: return img
        cx, cy = int(center[0]), int(center[1])
        self.noise_offset += 0.4

        overlay = np.zeros_like(img, dtype=np.uint8)
        
        # Concentrated Red Dot Base 
        cv2.circle(overlay, (cx, cy), 20, (50, 50, 150), -1)
        cv2.circle(overlay, (cx, cy), 12, (50, 50, 255), -1)
        cv2.circle(overlay, (cx, cy), 6, (255, 255, 255), -1)
        
        # Tiny subtle erratic sparks hovering directly around the fingertip point
        for i in range(5):
            angle = random.uniform(0, 2*math.pi)
            length = random.uniform(15, 30 + 10 * math.sin(self.noise_offset))
            pt2 = (int(cx + length * math.cos(angle)), int(cy + length * math.sin(angle)))
            cv2.line(overlay, (cx, cy), pt2, (200, 200, 255), random.randint(1, 2))

        cv2.add(img, overlay, img)
        return img

    def reset(self):
        pass
