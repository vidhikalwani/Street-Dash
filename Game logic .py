import random
import time

# ==========================================
# 1. CONSTANTS & INITIAL CONFIGURATION
# ==========================================
LANE_X = [-2.2, 0.0, 2.2]  # Left, Center, Right lane positions
GROUND_Y = 0.0
INITIAL_SPEED = 15.0
MAX_SPEED = 35.0
GRAVITY = 22.0
JUMP_IMPULSE = 9.0
SLIDE_DURATION = 0.55


# ==========================================
# 2. PLAYER OBJECT & STATE
# ==========================================
class Player:
    def __init__(self):
        self.lane_idx = 1  # Start in center lane (0=Left, 1=Center, 2=Right)
        self.x = 0.0
        self.target_x = 0.0
        self.y = GROUND_Y
        self.z = 2.0  # Player stays glued at Z = 2.0
        self.vy = 0.0  # Vertical velocity for jumping
        self.is_jumping = False
        self.is_sliding = False
        self.slide_timer = 0.0

    def move_left(self):
        """Shift destination lane to the left."""
        if self.lane_idx > 0:
            self.lane_idx -= 1
            self.target_x = LANE_X[self.lane_idx]

    def move_right(self):
        """Shift destination lane to the right."""
        if self.lane_idx < 2:
            self.lane_idx += 1
            self.target_x = LANE_X[self.lane_idx]

    def jump(self):
        """Trigger jump action if on ground."""
        if not self.is_jumping and not self.is_sliding:
            self.is_jumping = True
            self.vy = JUMP_IMPULSE

    def slide(self):
        """Trigger slide action if on ground."""
        if not self.is_jumping:
            self.is_sliding = True
            self.slide_timer = SLIDE_DURATION

    def get_hitbox(self):
        """Dynamic 3D bounding box that shrinks during slides."""
        height = 0.45 if self.is_sliding else 1.2
        min_y = self.y - 0.2 if self.is_sliding else self.y
        return {
            "min_x": self.x - 0.28, "max_x": self.x + 0.28,
            "min_y": min_y,        "max_y": min_y + height,
            "min_z": self.z - 0.4,  "max_z": self.z + 0.4
        }


# ==========================================
# 3. OBSTACLE & COIN ENTITIES
# ==========================================
class Obstacle:
    def __init__(self, obs_type, lane):
        self.type = obs_type
        self.lane = lane
        self.x = LANE_X[lane]
        self.z = -80.0  # Spawns far ahead in distance

        # Define height profiles based on type
        if obs_type == "hurdle":      # Jump over
            self.min_y, self.max_y = 0.0, 0.55
        elif obs_type == "overhead":  # Slide under
            self.min_y, self.max_y = 0.8, 2.2
        else:                         # Standard roadblock / car
            self.min_y, self.max_y = 0.0, 1.1

    def get_hitbox(self):
        width = 1.0 if self.type == "car" else 0.75
        depth = 2.2 if self.type == "car" else 0.75
        return {
            "min_x": self.x - width / 2, "max_x": self.x + width / 2,
            "min_y": self.min_y,         "max_y": self.max_y,
            "min_z": self.z - depth / 2, "max_z": self.z + depth / 2
        }


class Coin:
    def __init__(self, lane, z_pos):
        self.x = LANE_X[lane]
        self.y = 0.5
        self.z = z_pos
        self.collected = False


# ==========================================
# 4. COLLISION MATH & GAME STATE
# ==========================================
def check_aabb_collision(box_a, box_b):
    """Axis-Aligned Bounding Box (AABB) 3D Overlap Detection."""
    return (
        box_a["max_x"] > box_b["min_x"] and box_a["min_x"] < box_b["max_x"] and
        box_a["max_y"] > box_b["min_y"] and box_a["min_y"] < box_b["max_y"] and
        box_a["max_z"] > box_b["min_z"] and box_a["min_z"] < box_b["max_z"]
    )


class GameState:
    def __init__(self):
        self.is_running = True
        self.is_game_over = False
        self.score = 0
        self.coins = 0
        self.speed = INITIAL_SPEED
        self.frame = 0


# ==========================================
# 5. CORE GAME LOOP LOGIC
# ==========================================
def update_game_logic(player, game_state, obstacles, coins, dt):
    if not game_state.is_running or game_state.is_game_over:
        return

    game_state.frame += 1

    # 1. Progressive Speed Acceleration
    if game_state.frame % 300 == 0:
        game_state.speed = min(game_state.speed + 0.6, MAX_SPEED)

    # 2. Score Progression
    game_state.score += int(game_state.speed * 0.12)

    # 3. Smooth Lane Movement (Linear Interpolation)
    player.x += (player.target_x - player.x) * 0.18

    # 4. Jump & Slide Physics
    if player.is_jumping:
        player.vy -= GRAVITY * dt
        player.y += player.vy * dt
        if player.y <= GROUND_Y:
            player.y = GROUND_Y
            player.is_jumping = False
            player.vy = 0.0

    if player.is_sliding:
        player.slide_timer -= dt
        if player.slide_timer <= 0:
            player.is_sliding = False

    # 5. Obstacle Movement & Collision Checks
    player_box = player.get_hitbox()
    for obs in obstacles[:]:
        obs.z += game_state.speed * dt  # Scroll toward player

        # Clean up off-screen obstacles
        if obs.z > player.z + 5:
            obstacles.remove(obs)
            continue

        # Check collision
        if check_aabb_collision(player_box, obs.get_hitbox()):
            game_state.is_game_over = True
            game_state.is_running = False
            print(f"\n💥 CRASH! Hit a {obs.type} in Lane {obs.lane}!")
            return

    # 6. Coin Collection Logic
    for coin in coins[:]:
        coin.z += game_state.speed * dt

        if coin.z > player.z + 3:
            coins.remove(coin)
            continue

        # Pick up detection
        dx = abs(player.x - coin.x)
        dz = abs(player.z - coin.z)
        if not coin.collected and dx < 0.7 and dz < 1.2:
            coin.collected = True
            game_state.coins += 1
            coins.remove(coin)


def spawn_random_obstacle(obstacles):
    """Spawns an obstacle in a random lane."""
    types = ["hurdle", "overhead", "barrier", "cone", "car"]
    lane = random.randint(0, 2)
    obs_type = random.choice(types)
    obstacles.append(Obstacle(obs_type, lane))


# ==========================================
# 6. RUNNABLE SIMULATION
# ==========================================
if __name__ == "__main__":
    player = Player()
    game_state = GameState()
    obstacles = []
    coins = []

    dt = 0.016  # Simulating ~60 FPS update delta (16ms)
    print("🏃 Starting Street Dash 3D Engine Simulation...")

    for step in range(1, 201):
        # Periodically spawn obstacles
        if step % 30 == 0:
            spawn_random_obstacle(obstacles)

        # Simulate random player choices
        if step == 40:
            print("🕹️ Player switched LEFT")
            player.move_left()
        elif step == 80:
            print("🕹️ Player JUMPED")
            player.jump()
        elif step == 120:
            print("🕹️ Player SLID")
            player.slide()

        # Update core game tick
        update_game_logic(player, game_state, obstacles, coins, dt)

        # Print stats every 20 ticks
        if step % 20 == 0:
            print(
                f"Tick {step:03d} | Speed: {game_state.speed:.1f} | "
                f"Score: {game_state.score:04d} | Coins: {game_state.coins} | "
                f"Player Pos: (X={player.x:.2f}, Y={player.y:.2f}, Z={player.z:.1f})"
            )

        if game_state.is_game_over:
            break

        time.sleep(0.02)  # Pause briefly for visual CLI playback

    print(
        f"\n🎮 Game Ended! Final Score: {game_state.score} | Coins: {game_state.coins}"
    )
