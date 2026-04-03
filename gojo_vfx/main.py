import sys
import types
sys.modules['sounddevice'] = types.ModuleType('sounddevice')
sys.modules['sounddevice'].__path__ = []

import cv2
import time
import math
import random

from core.hand_tracking import HandTracker
from core.gesture_engine import GestureEngine
from core.state_manager import StateManager
from core.config import *

from effects.particles import ParticleSystem
from effects.blue_core import BlueEffect
from effects.red_projectile import RedProjectileEffect
from effects.purple_fusion import PurpleFusionEffect
from effects.domain import DomainExpansion
from effects.screen_fx import ScreenFX

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

    tracker = HandTracker(max_hands=2, detection_con=0.85, tracking_con=0.85, smoothing_factor=SMOOTHING_FACTOR)
    engine = GestureEngine()
    manager = StateManager()
    
    particle_sys = ParticleSystem(max_particles=MAX_PARTICLES)
    fx_screen = ScreenFX(w=CAM_WIDTH, h=CAM_HEIGHT)
    
    fx_blue = BlueEffect(color=COLOR_BLUE)
    fx_red = RedProjectileEffect(color=COLOR_RED)
    fx_purple = PurpleFusionEffect(color=COLOR_PURPLE)
    fx_domain = DomainExpansion()

    pTime = 0
    frame_count = 0

    while True:
        success, img = cap.read()
        if not success: break
        img = cv2.flip(img, 1)
        frame_count += 1

        tracker.find_hands(img, draw=False)
        hand_info = tracker.get_positions(img)
        
        gesture_data = engine.detect_gestures(hand_info)
        current_state = gesture_data['state']

        if current_state == "DOMAIN":
            manager.domain['active'] = True
        else:
            manager.domain['active'] = False
            manager.domain['frames'] = 0

        if current_state in ["BLUE", "BLUE_AND_RED"]:
            if gesture_data['blue_center']:
                manager.spawn_or_charge_blue(*gesture_data['blue_center'])
        else:
            manager.release_blue()

        if current_state in ["RED", "BLUE_AND_RED"]:
            if gesture_data['red_vel'] and engine.last_red:
                vx, vy = gesture_data['red_vel']
                speed = math.hypot(vx, vy)
                if speed > 12: 
                    manager.fire_red(engine.last_red[0], engine.last_red[1], vx * 1.5, vy * 1.5)

        shake_req = False
        tick_physics = True
        if manager.domain['active'] and frame_count % 2 == 1:
            tick_physics = False
            
        if tick_physics:
            shake_req = manager.update_physics()
            if shake_req: fx_screen.trigger_shake(5, 20)
            
        if manager.fusion_event:
            f = manager.fusion_event['frames']
            if f < 20:
                fx_screen.trigger_zoom(duration=2)
            elif f == 30:
                fx_screen.add_fracture(manager.fusion_event['x'], manager.fusion_event['y'])
                if manager.fusion_event.get('is_nuke'):
                    for _ in range(6):
                        fx_screen.add_fracture(
                            manager.fusion_event['x'] + random.randint(-200, 200),
                            manager.fusion_event['y'] + random.randint(-200, 200)
                        )

        if manager.domain['active']:
            img, shake = fx_domain.draw(img, fx_screen)
            if shake: fx_screen.trigger_shake(5, 10)

        img = fx_blue.draw(img, manager.blue_entity, particle_sys, fx_screen)
        
        for r in manager.red_projectiles:
            img = fx_red.draw(img, r, particle_sys, fx_screen)
            
        img = fx_purple.draw(img, manager.fusion_event, fx_screen)

        if not manager.domain['active']:
            img = particle_sys.update_and_draw(img)

        img = fx_screen.apply_fx(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        
        cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Reds: {len(manager.red_projectiles)}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        charge = manager.blue_entity['charge'] if manager.blue_entity else 0
        cv2.putText(img, f"Blue.C: {int(charge)}%", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 100), 2)

        cv2.imshow(WINDOW_NAME, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
