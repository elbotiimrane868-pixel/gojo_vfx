# 🌌 Gojo VFX: Cinematic Real-Time Combat Physics Engine

A high-fidelity, highly optimized, real-time interactive VFX physics system inspired by Satoru Gojo from *Jujutsu Kaisen*. Built entirely in pure Python using MediaPipe Computer Vision tracking and deeply mathematics-focused OpenCV rendering.

This is not a simple "hand-drawing" filter. This is a fully orchestrated physics engine simulating gravity anchors, kinetic projectile momentum, and catastrophic fusion interactions directly from your webcam.

---

## 🎮 The Mechanics & Controls

### 🔵 Blue (The Gravity Anchor)
**Gesture:** `Left Hand Open` (Palm visible to camera)
- Unlike a standard attachment, Blue acts as a **Persistent Spatial Anchor**. Once deployed, if you drop your hand, it stays anchored in 3D space, heavily distorting the light behind it (using spherical Fisheye warps). 
- It naturally gathers theoretical mass. While your hand is held open near it, it charges up, vibrating with intense sub-bass frequency audio.

### 🔴 Red (The Kinetic Projectile)
**Gesture:** `Right Hand, 1 Finger` (Index finger pointing)
- A highly unstable, chaotic core tracks perfectly to the tip of your index finger. 
- **Shooting it:** Thrust your hand forward and break the gesture (close your finger). The engine captures your wrist's escape velocity, decoupling the projectile and firing it away from you into space.
- The faster you flick your wrist, the faster it flies, and the more "Intent Detection" scales the particle chaos, dragging massive shattered geometric streaks behind it.

### 🟣 Hollow Purple (Collision Tension Fusion)
**Trigger:** `Fire a Red Blast into a Blue Anchor`
- **Inevitable Tension:** The moment Red and Blue mathematically cross thresholds, time locks. The projectiles freeze, vibrate, and physically pull themselves into the exact same spatial coordinate for half a second.
- **Cinematic Zoom:** The physical camera micro-zooms into the tension.
- **Release:** The collision breaks. A massive, screen-tearing explosion of purple energy erupts, accompanied by deep-frequency audio tearing.

### ☢️ Hollow Nuke (Auto-Trigger inside Domain)
**Trigger:** `Charge an Anchor to >80% and Fire a High-Velocity Blast into it`
- Calculates the mass difference. Triggers a shattered-reality event where extreme spatial fractures rip across the screen, and the background environment undergoes intense monochromatic scaling and chromatic aberration (RGB tearing).

### 🤞 Domain Expansion (Infinite Void)
**Gesture:** `Right Hand, Index + Middle Fingers Crossed` (The Gojo Sign)
- **Environment Hacking:** Replaces the room behind you with a cinematic, cold-blue, high-contrast endless void layered with geometric boundaries and floating physical debris.
- **Rule Breaking:** The physics engine drops 50% of its ticks (Time Dilation). Inside the Domain, Red projectiles act as instant auto-nukes if they hit an anchor, and Blue charges twice as rapidly.

---

## ⚙️ Installation

1. Clone the repository.
2. Install the Vision libraries:
   ```bash
   pip install opencv-python mediapipe numpy
   ```
3. Run the application:
   - On Windows: Simply double-click `run_gojo.bat`
   - Via Terminal: `python `

---

### 🔥 Technical Architecture Breakdown
- `core/gesture_engine.py`: Maps vector magnitude mathematics and rotation-invariant thresholds to Google MediaPipe's underlying 3D bone mapping AI.
- `core/state_manager.py`: The physics orchestrator. Tracks boundary boomerangs, force application, decay tracking, and triggers collision interactions.
- `effects/*`: Segmented, highly-optimized frame rendering matrices using arrays and Gaussian caching.
