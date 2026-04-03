import cv2
import numpy as np
import random
import math

class PurpleFusionEffect:
    def __init__(self, color=(255, 50, 255)):
        self.color = color
        
    def draw(self, img, fx_event, fx_screen):
        if not fx_event: return img
        
        cx, cy = int(fx_event['x']), int(fx_event['y'])
        stage = fx_event['stage']
        f = fx_event['frames']
        is_nuke = fx_event.get('is_nuke', False)
        
        overlay = np.zeros_like(img, dtype=np.uint8)

        if stage == 'TENSION':
            b_r = int(20 + fx_event['b_charge']*0.4)
            cv2.circle(overlay, (cx, cy), b_r, (255, 100, 50), -1)
            rx, ry = int(fx_event['r_x']), int(fx_event['r_y'])
            rx = int(rx + (cx - rx) * (f / 20.0))
            ry = int(ry + (cy - ry) * (f / 20.0))
            cv2.circle(overlay, (rx, ry), 15, (50, 50, 255), -1)

            for _ in range(20):
                angle = random.uniform(0, 2*math.pi)
                dist = random.uniform(50, 300)
                p1 = (int(cx + dist*math.cos(angle)), int(cy + dist*math.sin(angle)))
                p2 = (int(cx + (dist-40)*math.cos(angle)), int(cy + (dist-40)*math.sin(angle)))
                cv2.line(overlay, p1, p2, (255, 100, 255), 2)
                
            radius = int(10 + random.uniform(0, 20 + f))
            cv2.circle(overlay, (cx, cy), radius, (255, 255, 255), -1)
            cv2.addWeighted(img, 1.0, overlay, 1.0, 0, img)
            alpha_dark = max(0.2, 1.0 - (f/20.0))
            img = cv2.addWeighted(img, alpha_dark, np.zeros_like(img), 0, 0)
            
        elif stage == 'FUSION':
            overlay[:] = (255, 255, 255)
            alpha = max(0, 1.0 - ((f-20)/10.0))
            cv2.addWeighted(img, 1.0, overlay, alpha, 0, img)
            cv2.circle(img, (cx, cy), int((f-20)*5), (255, 0, 255), 10)
            
        elif stage == 'RELEASE':
            blast_radius = int((f - 30) * (30 if is_nuke else 15))
            
            cv2.circle(overlay, (cx, cy), blast_radius, self.color, -1)
            cv2.circle(overlay, (cx, cy), int(blast_radius * 0.7), (255, 200, 255), -1)
            cv2.circle(overlay, (cx, cy), int(blast_radius * 1.2), (255, 100, 255), 10)

            num_arcs = 30 if is_nuke else 12
            for _ in range(num_arcs):
                start_angle = random.uniform(0, 2*math.pi)
                r = blast_radius
                curr_pt = (cx + int(r*math.cos(start_angle)), cy + int(r*math.sin(start_angle)))
                path = [curr_pt]
                
                for _step in range(6):
                    da = random.uniform(-0.8, 0.8)
                    dr = random.uniform(40, 150 if is_nuke else 80)
                    nx = curr_pt[0] + int(dr*math.cos(start_angle + da))
                    ny = curr_pt[1] + int(dr*math.sin(start_angle + da))
                    curr_pt = (nx, ny)
                    path.append(curr_pt)
                    
                for i in range(len(path)-1):
                    cv2.line(overlay, path[i], path[i+1], (255, 255, 255), random.randint(3, 10))

            img = fx_screen.apply_bloom(img, intensity=1.5 if is_nuke else 1.0)
            
            if is_nuke:
                overlay = cv2.bitwise_not(overlay)

            cv2.addWeighted(img, 1.0, overlay, max(0, 1.0 - (f-30)/50.0), 0, img)
            
        return img
