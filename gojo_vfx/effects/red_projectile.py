import cv2
import numpy as np
import random
import math

class RedProjectileFX:
    def __init__(self):
        pass

    def draw(self, img, reds, fx_screen):
        if not reds: return img
        
        overlay = np.zeros_like(img, dtype=np.uint8)
        
        for r in reds:
            x, y = int(r['x']), int(r['y'])
            vx, vy = r['vx'], r['vy']
            speed = r.get('speed_norm', 15.0)
            
            # Intention Metric (High speed = chaotic, low = controlled)
            chaos = int(speed / 10.0)
            
            # Scatter sparks based on chaos
            for _ in range(5 + chaos * 3):
                p_x = x - vx * random.uniform(0.1, 1.5) + random.randint(-15 - chaos*5, 15 + chaos*5)
                p_y = y - vy * random.uniform(0.1, 1.5) + random.randint(-15 - chaos*5, 15 + chaos*5)
                size = random.randint(2, 5 + chaos)
                cv2.circle(overlay, (int(p_x), int(p_y)), size, (50, 50, 255), -1)
                
            # Core
            core_r = int(8 + (speed / 10.0))
            cv2.circle(img, (x, y), core_r, (200, 200, 255), -1)
            cv2.circle(overlay, (x, y), core_r + 4, (0, 0, 255), 2)
            
            # Geometric shards if extremely high intention
            if chaos > 3:
                for _ in range(chaos):
                    dx = random.randint(-40, 40)
                    dy = random.randint(-40, 40)
                    cv2.line(overlay, (x, y), (x+dx, y+dy), (255, 255, 255), 1)

        cv2.addWeighted(img, 1.0, overlay, 1.0, 0, img)
        return img
