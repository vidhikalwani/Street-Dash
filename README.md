# Street-Dash
Street Dash is a browser-based, retro-inspired, plain-style endless runner prompted by the me to Claude AI and generated with Claude AI. It features a blocky child character, a 3-lane track system, jump and slide movement, simple 3D obstacles, and a camera-follow setup.

# The Key Features of Street Dash 
1. AI-Assisted Development: Designed through prompt engineering to generate complete, single-file HTML/JS game code powered by Three.js and the Web Audio API.
2. 3D Environment & Atmospheric Lighting: Features a vibrant, infinite 3D street route surrounded by colorful, glowing high-rise buildings, ambient fill lights, and directional sun casting real-time soft shadows.
3. 3-Lane Gameplay: Smoothly switch between three lanes (left, center, right) to navigate around obstacles and collect items.
4. Varied Jump & Slide Obstacle Mechanics: Test your reflexes against low hurdles and roadblocks, overhead signs and low-hanging barriers, traffic cones, trash cans, and colorful cars.
5. High-Tempo Progressive Speed & Difficulty Scaling: Game velocity starts at a high-tempo base pace (15) and automatically accelerates up to a fast-paced maximum speed (35) as your score rises, dramatically increasing the challenge over time.
6. Synthesized Web Audio Engine & BGM: Fully procedural audio system built with the Web Audio API that generates custom looping chiptune background music and synthesized retro sound effects for jumping, sliding, picking up coins, and crashing—requiring zero external audio files.
7. Coin Collection & Visual Effects: Gather spinning gold coins along the track accompanied by custom synth pickup audio, gold particle bursts upon collection, and on-screen coin tracking.
8. Camera Follow: Immersive trailing camera system that tilts smoothly into lane shifts and triggers impact camera shake on collisions.
9. Multi-Input Cross-Platform Controls: Full support for both desktop keyboard inputs and mobile touch swipe gestures.
10. Action Mechanics & Character Animations: Full jump and low-slide physics paired with character scale body deformations and leg/arm running movements

# Tech Stack & Implementation
1. 3D Graphics & Rendering Engine: Three.js (r128 WebGL renderer, PCF soft shadows, directional light maps, procedural geometry).
2. Audio Processing: Native HTML5 Web Audio API (AudioContext, OscillatorNode, GainNode sound synth pipeline).
3. Prompt Engineering: Directed AI to architect the logic, collision physics, synth sound synthesis, and rendering pipeline within a single self-contained HTML deliverable.

# Control Mechanics
1. Keyboard API: Captures keydown events for Arrow keys (← / → / ↑ / ↓), WASD, and Spacebar navigation.
2. Touch / Gesture API: Custom swipe detection (touchstart and touchend) calculating swipe vectors for mobile touch devices.

# Gameplay screenshot
![image_alt](https://github.com/vidhikalwani/Street-Dash/blob/4e2c679a06c85518c699e42f4515e4c3b2e57ec8/Game%20start%20page.jpeg)
[![image_alt](https://github.com/vidhikalwani/Street-Dash/blob/cc7ded38e9df445a7ae06cbe061f93e868b11291/Playing%20the%20game%20(1).jpeg)
![image_alt](https://github.com/vidhikalwani/Street-Dash/blob/cc7ded38e9df445a7ae06cbe061f93e868b11291/Playing%20the%20game%20(2).jpeg)
[![image_alt](https://github.com/vidhikalwani/Street-Dash/blob/cc7ded38e9df445a7ae06cbe061f93e868b11291/When%20we%20lose.jpeg)

# Action Demo
![video](https://github.com/vidhikalwani/Street-Dash/blob/cc7ded38e9df445a7ae06cbe061f93e868b11291/Playing%20the%20game.mp4)
