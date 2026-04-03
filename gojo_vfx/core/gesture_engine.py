import math

class GestureEngine:
    def __init__(self):
        self.state = "IDLE"
        self.last_blue = None
        self.last_red = None
        self.vel_blue = (0, 0)
        self.vel_red = (0, 0)
        
    def fingers_up(self, lm_list):
        fingers = []
        if not lm_list: return [0,0,0,0,0]
        
        wrist = lm_list[0]
        pinky_mcp = lm_list[17]
        thumb_tip = lm_list[4]
        thumb_mcp = lm_list[2]
        
        d_tip = math.hypot(thumb_tip[1]-pinky_mcp[1], thumb_tip[2]-pinky_mcp[2])
        d_mcp = math.hypot(thumb_mcp[1]-pinky_mcp[1], thumb_mcp[2]-pinky_mcp[2])
        fingers.append(1 if d_tip > d_mcp * 1.5 else 0)

        for id in [8, 12, 16, 20]:
            tip = lm_list[id]
            pip = lm_list[id-2]
            d_tip = math.hypot(tip[1]-wrist[1], tip[2]-wrist[2])
            d_pip = math.hypot(pip[1]-wrist[1], pip[2]-wrist[2])
            fingers.append(1 if d_tip > d_pip * 1.25 else 0)
            
        return fingers

    def detect_gestures(self, hand_info):
        blue_active = False
        red_active = False
        domain_active = False
        
        blue_center = None
        red_center = None

        for hand in hand_info:
            fingers = self.fingers_up(hand['lmList'])
            
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                blue_active = True
                blue_center = hand['center']
                
            elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                red_active = True
                red_center = (hand['lmList'][8][1], hand['lmList'][8][2])
                
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                idx_tip = hand['lmList'][8]
                mid_tip = hand['lmList'][12]
                wrist = hand['lmList'][0]
                idx_mcp = hand['lmList'][5]
                scale = math.hypot(idx_mcp[1]-wrist[1], idx_mcp[2]-wrist[2])
                dist = math.hypot(idx_tip[1]-mid_tip[1], idx_tip[2]-mid_tip[2])
                
                if dist < scale * 0.4:
                    domain_active = True

        current_state = "IDLE"
        if domain_active: current_state = "DOMAIN"
        elif blue_active and red_active:
            dist = math.hypot(blue_center[0] - red_center[0], blue_center[1] - red_center[1])
            if dist < 150: current_state = "PURPLE"
            else: current_state = "BLUE_AND_RED"
        elif blue_active: current_state = "BLUE"
        elif red_active: current_state = "RED"
        
        if blue_center and self.last_blue:
            self.vel_blue = (blue_center[0] - self.last_blue[0], blue_center[1] - self.last_blue[1])
        if red_center and self.last_red:
            self.vel_red = (red_center[0] - self.last_red[0], red_center[1] - self.last_red[1])
            
        self.last_blue = blue_center
        self.last_red = red_center
            
        return {
            'state': current_state,
            'blue_center': blue_center,
            'red_center': red_center,
            'blue_vel': self.vel_blue,
            'red_vel': self.vel_red
        }
