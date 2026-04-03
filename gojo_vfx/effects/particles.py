import cv2
import numpy as np
import random

class ParticleSystem:
    def __init__(self, max_particles=600):
        self.max_particles = max_particles
        self.particles = []

    def emit(self, x, y, color, velocity=(0, 0), speed=1.0, life=30, size=3):
        if len(self.particles) < self.max_particles:
            vx = velocity[0] * speed + random.uniform(-1, 1)
            vy = velocity[1] * speed + random.uniform(-1, 1)
            self.particles.append({
                'x': x, 'y': y, 'px': x, 'py': y,
                'vx': vx, 'vy': vy, 'color': color,
                'life': life, 'max_life': life, 'size': size
            })

    def emit_attract(self, center_x, center_y, color, radius=150, life=20, size=3):
        if len(self.particles) < self.max_particles:
            angle = random.uniform(0, 2 * np.pi)
            r = random.uniform(radius*0.5, radius)
            px = center_x + r * np.cos(angle)
            py = center_y + r * np.sin(angle)
            
            vx = (center_x - px) / life + np.sin(angle)*3
            vy = (center_y - py) / life + np.cos(angle)*3
            
            self.particles.append({
                'x': px, 'y': py, 'px': px, 'py': py,
                'vx': vx, 'vy': vy, 'color': tuple(min(255, c+50) for c in color),
                'life': life, 'max_life': life, 'size': size
            })

    def emit_repel(self, center_x, center_y, color, speed=10.0, life=15, size=3):
        if len(self.particles) < self.max_particles:
            angle = random.uniform(0, 2 * np.pi)
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle)
            self.particles.append({
                'x': center_x, 'y': center_y, 'px': center_x, 'py': center_y,
                'vx': vx, 'vy': vy, 'color': color,
                'life': life, 'max_life': life, 'size': size
            })

    def update_and_draw(self, img):
        overlay = np.zeros_like(img, dtype=np.uint8)
        alive = []
        for p in self.particles:
            p['px'], p['py'] = p['x'], p['y']
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1

            if p['life'] > 0:
                alive.append(p)
                alpha = p['life'] / p['max_life']
                color = tuple(int(c * alpha) for c in p['color'])
                
                # Draw motion streak
                thickness = max(1, p['size'])
                cv2.line(overlay, (int(p['px']), int(p['py'])), (int(p['x']), int(p['y'])), color, thickness)
                if alpha > 0.5:
                    cv2.circle(overlay, (int(p['x']), int(p['y'])), thickness, (255,255,255), -1)

        self.particles = alive
        cv2.add(img, overlay, img)
        return img
