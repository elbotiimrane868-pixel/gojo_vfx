import cv2
import numpy as np
import random
import math

class BlueEffect:
    def __init__(self, color=(255, 100, 50)):
        self.color = color
        self.radius = 5
        self.max_radius = 60
        self.rotation = 0
        self.time = 0
        
    def draw(self, img, center, particle_system, fx_screen):
        if not center: return img
        cx, cy = int(center[0]), int(center[1])
        self.time += 0.1
        
        if self.radius < self.max_radius:
            self.radius += 5

        img = fx_screen.apply_gravity_warp(img, (cx, cy))

        self.rotation += 0.15
        overlay = np.zeros_like(img, dtype=np.uint8)

        pulse = math.sin(self.time * 2) * 10
        cv2.circle(overlay, (cx, cy), int(self.radius + pulse), self.color, -1)
        
        for i in range(4):
            angle_offset = self.rotation + i * (math.pi / 2)
            pts = []
            for t in range(0, 50, 2):
                r = self.radius * 0.2 + t * 1.5
                theta = angle_offset + t * 0.1
                px = cx + r * math.cos(theta)
                py = cy + r * math.sin(theta)
                pts.append([int(px), int(py)])
            pts = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(overlay, [pts], isClosed=False, color=(255, 200, 100), thickness=int(3 + math.sin(self.time)*2))

        particle_system.emit_attract(cx, cy, self.color, radius=self.radius*5, life=15, size=2)
        cv2.circle(overlay, (cx, cy), int(self.radius * 0.3), (255, 255, 255), -1)

        cv2.add(img, overlay, img)
        return img

    def reset(self):
        self.radius = 5
