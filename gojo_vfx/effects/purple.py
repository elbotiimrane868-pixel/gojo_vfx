import cv2
import numpy as np
import random
import math

class PurpleEffect:
    def __init__(self, color=(255, 50, 255)):
        self.color = color
        self.beam_radius = 5
        self.max_beam_radius = 350
        self.active_frames = 0
        self.flash_alpha = 1.0
        
    def draw(self, img, b_center, r_center, fx_screen):
        if not b_center or not r_center: return img, False
        self.active_frames += 1
        
        cx = (b_center[0] + r_center[0]) // 2
        cy = (b_center[1] + r_center[1]) // 2

        if self.active_frames < 10:
            self.flash_alpha = max(0, 1.0 - (self.active_frames / 10.0))
            overlay = np.full_like(img, (255, 255, 255), dtype=np.uint8)
            cv2.addWeighted(img, 1.0, overlay, self.flash_alpha, 0, img)
            # Screen tear
            cv2.line(img, (0, cy), (img.shape[1], cy), (255, 50, 255), int(self.flash_alpha*30))
            cv2.line(img, (cx, 0), (cx, img.shape[0]), (255, 50, 255), int(self.flash_alpha*30))
            return img, True

        if self.beam_radius < self.max_beam_radius:
            self.beam_radius += 40

        overlay = np.zeros_like(img, dtype=np.uint8)
        
        cv2.circle(overlay, (cx, cy), self.beam_radius, self.color, -1)
        cv2.circle(overlay, (cx, cy), int(self.beam_radius * 0.8), (255, 200, 255), -1)

        cv2.circle(overlay, (cx, cy), int(self.beam_radius * 1.5), (255, 100, 255), 10)
        cv2.circle(overlay, (cx, cy), int(self.beam_radius * 2.0), (200, 50, 200), 4)

        for _ in range(15):
            start_angle = random.uniform(0, 2*math.pi)
            r = self.beam_radius
            pt1 = (cx + int(r*math.cos(start_angle)), cy + int(r*math.sin(start_angle)))
            
            path = [pt1]
            curr_pt = pt1
            for _step in range(5):
                da = random.uniform(-0.8, 0.8)
                dr = random.uniform(40, 100)
                nx = curr_pt[0] + int(dr*math.cos(start_angle + da))
                ny = curr_pt[1] + int(dr*math.sin(start_angle + da))
                curr_pt = (nx, ny)
                path.append(curr_pt)
                
            for i in range(len(path)-1):
                cv2.line(overlay, path[i], path[i+1], (255, 255, 255), random.randint(3, 8))

        img = fx_screen.apply_bloom(img, intensity=1.0)
        cv2.add(img, overlay, img)
        
        return img, True

    def reset(self):
        self.beam_radius = 5
        self.active_frames = 0
        self.flash_alpha = 1.0
