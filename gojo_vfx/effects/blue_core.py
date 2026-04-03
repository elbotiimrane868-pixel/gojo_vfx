import cv2
import numpy as np
import math
import random

class BlueEffect:
    def __init__(self, color=(255, 100, 50)):
        self.color = color
        self.time = 0
        
    def draw(self, img, entity, particle_sys, fx_screen):
        if not entity: return img
        cx, cy = int(entity['x']), int(entity['y'])
        charge = entity['charge']
        
        radius = 20 + int(charge * 0.4)
        
        self.time += 0.1
        img = fx_screen.apply_gravity_warp(img, (cx, cy))

        overlay = np.zeros_like(img, dtype=np.uint8)
        pulse = math.sin(self.time * 2) * (5 + charge * 0.1)
        cv2.circle(overlay, (cx, cy), int(radius + pulse), self.color, -1)
        
        rotation = self.time * 1.5
        for i in range(4):
            angle_offset = rotation + i * (math.pi / 2)
            pts = []
            for t in range(0, int(30 + charge*0.3), 2):
                r = radius * 0.2 + t * 1.5
                theta = angle_offset + t * 0.1
                px = cx + r * math.cos(theta)
                py = cy + r * math.sin(theta)
                pts.append([int(px), int(py)])
            if pts:
                pts = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(overlay, [pts], isClosed=False, color=(255, 200, 100), thickness=int(2 + math.sin(self.time)*2))

        particle_sys.emit_attract(cx, cy, self.color, radius=radius*5, life=15, size=2)
        cv2.circle(overlay, (cx, cy), int(radius * 0.3), (255, 255, 255), -1)

        cv2.addWeighted(img, 1.0, overlay, 1.0, 0, img)
        return img
