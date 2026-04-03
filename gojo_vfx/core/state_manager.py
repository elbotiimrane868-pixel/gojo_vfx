import math
import threading
import platform

def play_sound(freq, duration):
    if platform.system() == 'Windows':
        import winsound
        threading.Thread(target=winsound.Beep, args=(int(abs(freq)), int(max(duration, 10))), daemon=True).start()

class StateManager:
    def __init__(self):
        self.blue_entity = None   # { 'x', 'y', 'charge', 'max_charge' }
        self.red_projectiles = []
        self.fusion_event = None # { 'x', 'y', 'stage', 'frames' }
        self.domain = {'active': False, 'frames': 0}
        
    def spawn_or_charge_blue(self, x, y):
        if not self.blue_entity:
            self.blue_entity = {'x': x, 'y': y, 'charge': 0.0, 'max_charge': 100.0}
            play_sound(70, 250)
        else:
            charge_spd = 2.0 if self.domain['active'] else 1.0
            self.blue_entity['charge'] = min(self.blue_entity['max_charge'], self.blue_entity['charge'] + charge_spd)
            if int(self.blue_entity['charge']) % 15 == 0:
                play_sound(55 + self.blue_entity['charge']*0.5, 80)
            
    def release_blue(self):
        if self.blue_entity:
            self.blue_entity['charge'] -= 0.2
            if self.blue_entity['charge'] <= 0:
                self.blue_entity = None

    def fire_red(self, x, y, vx, vy):
        play_sound(2000, 100)
        self.red_projectiles.append({
            'x': x, 'y': y,
            'vx': vx, 'vy': vy,
            'life': 50,
            'speed_norm': math.hypot(vx, vy)
        })

    def update_physics(self):
        # Update Reds
        alive_reds = []
        for r in self.red_projectiles:
            r['x'] += r['vx']
            r['y'] += r['vy']
            r['life'] -= 1
            
            if r['x'] < -100 or r['x'] > 800 or r['y'] < -100 or r['y'] > 600:
                if self.blue_entity:
                    vec_x = (self.blue_entity['x'] - r['x'])
                    vec_y = (self.blue_entity['y'] - r['y'])
                    mag = math.hypot(vec_x, vec_y)
                    if mag > 0:
                        r['vx'] = (vec_x / mag) * 35.0
                        r['vy'] = (vec_y / mag) * 35.0
                    r['life'] -= 10
                    play_sound(800, 50)
                else:
                    r['life'] = 0
            
            # Check Collision with Blue
            hit_blue = False
            if self.blue_entity and not self.fusion_event:
                dist = math.hypot(r['x'] - self.blue_entity['x'], r['y'] - self.blue_entity['y'])
                
                if dist < 300:
                    pull_force = (self.blue_entity['charge'] * 0.05) / max(1, dist)
                    vec_x = (self.blue_entity['x'] - r['x']) / max(1, dist)
                    vec_y = (self.blue_entity['y'] - r['y']) / max(1, dist)
                    r['vx'] += vec_x * pull_force * 20.0
                    r['vy'] += vec_y * pull_force * 20.0

                hit_dist = 140 if self.domain['active'] else 80
                
                if dist < hit_dist + (self.blue_entity['charge'] * 0.5):
                    hit_blue = True
                    nuke_thresh = 40 if self.domain['active'] else 80
                    speed_thresh = 15 if self.domain['active'] else 25
                    is_nuke = self.blue_entity['charge'] > nuke_thresh and r['speed_norm'] > speed_thresh
                    if self.domain['active']:
                        is_nuke = True
                        
                    self.fusion_event = {
                        'x': self.blue_entity['x'],
                        'y': self.blue_entity['y'],
                        'frames': 0,
                        'stage': 'TENSION',
                        'is_nuke': is_nuke,
                        'b_charge': self.blue_entity['charge'],
                        'r_x': r['x'], 'r_y': r['y']
                    }
                    self.blue_entity = None

            if not hit_blue and r['life'] > 0:
                alive_reds.append(r)
                
        self.red_projectiles = alive_reds
        
        # Update Fusion
        shake_request = False
        if self.fusion_event:
            self.fusion_event['frames'] += 1
            f = self.fusion_event['frames']
            if f < 20:
                self.fusion_event['stage'] = 'TENSION'
                shake_request = True
            elif f < 30:
                self.fusion_event['stage'] = 'FUSION'
            elif f < 80:
                self.fusion_event['stage'] = 'RELEASE'
                if f == 30: 
                    shake_request = True
                    play_sound(200, 800)
                    if self.fusion_event.get('is_nuke'):
                        play_sound(120, 1500)
            else:
                self.fusion_event = None
                
        return shake_request
