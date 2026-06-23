import pygame
import random
import math
import json
import os

# --- 1. KONFIGURASI UTAMA ---
pygame.init()
pygame.mixer.init() 
monitor_info = pygame.display.Info()
WIDTH = int(monitor_info.current_w * 0.85)
HEIGHT = int(monitor_info.current_h * 0.85)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZMATH: GALACTIC TARGET - ADVANCED COCKPIT")
clock = pygame.time.Clock()

# Warna
CYAN, GREEN, RED = (0, 255, 255), (50, 255, 50), (255, 50, 50)
ORANGE, YELLOW, WHITE, BLACK = (255, 100, 0), (255, 255, 0), (255, 255, 255), (2, 2, 8)
GRAY = (100, 100, 100)
HUD_CYAN = (0, 120, 140)
HUD_DARK = (10, 15, 25)

# Font
font_math = pygame.font.SysFont("Consolas", int(HEIGHT * 0.025), bold=True)
font_ui = pygame.font.SysFont("Courier New", int(HEIGHT * 0.02), bold=True)
font_big = pygame.font.SysFont("Arial", int(HEIGHT * 0.08), bold=True)

# --- 2. SISTEM AUDIO (SAFE LOAD) ---
def play_backsound():
    try:
        pygame.mixer.music.load("space_backsound.mp3") 
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(0.4)
    except:
        pass 

def play_sfx(sound_type):
    try:
        if sound_type == "laser":
            snd = pygame.mixer.Sound("laser.wav")
            snd.set_volume(0.3)
            snd.play()
        elif sound_type == "explosion":
            snd = pygame.mixer.Sound("explosion.wav")
            snd.set_volume(0.5)
            snd.play()
    except:
        pass

# --- 3. SISTEM DATA LEADERBOARD ---
LEADERBOARD_FILE = "leaderboard_v2.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_leaderboard(name, score, level):
    data = load_leaderboard()
    data.append({"name": name, "score": score, "level": level})
    
    clean_dict = {}
    for item in data:
        n = item["name"]
        if n not in clean_dict or item["score"] > clean_dict[n]["score"]:
            clean_dict[n] = item
            
    cleaned_data = sorted(clean_dict.values(), key=lambda x: x["score"], reverse=True)
    
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(cleaned_data, f)
    return cleaned_data

def get_highest_score():
    data = load_leaderboard()
    if data:
        return data[0]["score"]
    return 0

def get_player_rank(name, score):
    data = load_leaderboard()
    clean_dict = {}
    for item in data:
        n = item["name"]
        if n not in clean_dict or item["score"] > clean_dict[n]["score"]:
            clean_dict[n] = item
            
    clean_dict[name] = {"name": name, "score": score}
    sorted_data = sorted(clean_dict.values(), key=lambda x: x["score"], reverse=True)
    
    for idx, item in enumerate(sorted_data):
        if item["name"] == name:
            return idx + 1
    return 1

# --- 4. SISTEM EFEK LINGKUNGAN ---
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.choice([1, 1, 1, 2]) 
        self.speed = random.uniform(0.2, 1.0) if self.size == 1 else random.uniform(1.0, 2.5)
        c_val = random.randint(150, 255)
        self.color = random.choice([(c_val, c_val, c_val), (c_val-50, c_val, c_val), (c_val, c_val, c_val-50)])

    def update(self, time_scale):
        self.y += self.speed * time_scale
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.size)

# --- ADVANCED FUTURISTIC COCKPIT BACKGROUND RENDERER ---
def draw_spaceship_cockpit(surf):
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    # 1. Holographic HUD Lines (Perspektif Target)
    pygame.draw.line(surf, (0, 50, 60), (0, 0), (WIDTH, HEIGHT), 1)
    pygame.draw.line(surf, (0, 50, 60), (WIDTH, 0), (0, HEIGHT), 1)
    for r in [int(HEIGHT * 0.25), int(HEIGHT * 0.5), int(HEIGHT * 0.75)]:
        pygame.draw.circle(surf, (0, 40, 50), (center_x, center_y), r, 1)

    # 2. Struktur Frame Kaca Depan Pesawat
    # Pilar Samping Kiri
    pygame.draw.polygon(surf, HUD_DARK, [(0, 0), (100, 0), (220, HEIGHT - 150), (0, HEIGHT - 150)])
    pygame.draw.polygon(surf, HUD_CYAN, [(0, 0), (100, 0), (220, HEIGHT - 150), (0, HEIGHT - 150)], 2)
    # Pilar Samping Kanan
    pygame.draw.polygon(surf, HUD_DARK, [(WIDTH, 0), (WIDTH - 100, 0), (WIDTH - 220, HEIGHT - 150), (WIDTH, HEIGHT - 150)])
    pygame.draw.polygon(surf, HUD_CYAN, [(WIDTH, 0), (WIDTH - 100, 0), (WIDTH - 220, HEIGHT - 150), (WIDTH, HEIGHT - 150)], 2)
    
    # Konsol Atap Cockpit
    pygame.draw.polygon(surf, HUD_DARK, [(center_x - 200, 0), (center_x + 200, 0), (center_x + 140, 45), (center_x - 140, 45)])
    pygame.draw.polygon(surf, HUD_CYAN, [(center_x - 200, 0), (center_x + 200, 0), (center_x + 140, 45), (center_x - 140, 45)], 2)

    # 3. Dashboard / Meja Kendali Utama (Bagian Bawah)
    pygame.draw.polygon(surf, (15, 20, 30), [(0, HEIGHT), (WIDTH, HEIGHT), (WIDTH - 200, HEIGHT - 150), (200, HEIGHT - 150)])
    pygame.draw.polygon(surf, HUD_CYAN, [(0, HEIGHT), (WIDTH, HEIGHT), (WIDTH - 200, HEIGHT - 150), (200, HEIGHT - 150)], 3)
    
    # Sub-Panel Monitor Tengah Dashboard
    pygame.draw.rect(surf, (22, 28, 40), (center_x - 300, HEIGHT - 110, 600, 90), border_radius=10)
    pygame.draw.rect(surf, (0, 160, 180), (center_x - 300, HEIGHT - 110, 600, 90), 2, border_radius=10)

    # Lampu Dekorasi Kerlip Konsol Elektronik
    ticks = pygame.time.get_ticks()
    g_light = GREEN if ticks % 1000 < 500 else (10, 60, 10)
    r_light = RED if ticks % 700 < 350 else (60, 10, 10)
    pygame.draw.circle(surf, g_light, (center_x - 260, HEIGHT - 65), 5)
    pygame.draw.circle(surf, r_light, (center_x - 240, HEIGHT - 65), 5)
    pygame.draw.circle(surf, g_light, (center_x + 260, HEIGHT - 65), 5)

    # 4. LAPISAN FILTER BLUR/DIM (Kunci utama agar tulisan menu terbaca super jelas!)
    dim_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim_layer.fill((6, 10, 22, 195)) # Warna navy gelap transparan dengan opasitas tinggi (195/255)
    surf.blit(dim_layer, (0, 0))


class Particle:
    def __init__(self, x, y, color, speed_range=(1, 4), size_range=(2, 4)):
        self.x, self.y = x, y; self.color = color; self.size = random.uniform(*size_range)
        angle = random.uniform(0, math.pi * 2); speed = random.uniform(*speed_range)
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed; self.alpha = 255

    def update(self, time_scale):
        self.x += self.vx * time_scale; self.y += self.vy * time_scale; self.alpha -= 6 * time_scale
        if self.size > 0.1: self.size -= 0.1 * time_scale

    def draw(self, surf):
        if self.alpha > 0:
            s = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (int(self.size), int(self.size)), int(self.size))
            surf.blit(s, (self.x - self.size, self.y - self.size))

class Shockwave:
    def __init__(self, x, y, color, speed=5):
        self.x, self.y = x, y; self.color = color; self.radius = 5; self.speed = speed; self.alpha = 255

    def update(self, time_scale):
        self.radius += self.speed * time_scale; self.alpha -= 8 * time_scale

    def draw(self, surf):
        if self.alpha > 0:
            s = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (int(self.radius), int(self.radius)), int(self.radius), 3)
            surf.blit(s, (self.x - self.radius, self.y - self.radius))

# --- 5. LOGIKA GAMEPLAY ALIEN ---
class Alien:
    def __init__(self, target_pos, level, prefix):
        self.target_pos = target_pos; self.prefix = prefix; self.generate_mission(level)

    def generate_mission(self, level):
        op = '+'; self.spawn_delay_modifier = 0; speed_grade = 1.0 
        if level == 1:
            op = '+'; ans = random.randint(2, 20); self.a = random.randint(1, ans - 1); self.b = ans - self.a
        elif level == 2:
            op = '-'; self.a = random.randint(10, 20); self.b = random.randint(1, 9); ans = self.a - self.b
        elif level == 3:
            op = '+'; ans = random.randint(2, 20); self.a = random.randint(1, ans - 1); self.b = ans - self.a; speed_grade = 1.3 
        elif level == 4:
            op = '-'; self.a = random.randint(10, 20); self.b = random.randint(1, 9); ans = self.a - self.b; speed_grade = 1.3
        elif level == 5:
            op = random.choice(['+', '-'])
            if op == '+': ans = random.randint(2, 20); self.a = random.randint(1, ans - 1); self.b = ans - self.a
            else: self.a = random.randint(10, 20); self.b = random.randint(1, 9); ans = self.a - self.b
            speed_grade = 1.1 
        elif level == 6:
            op = '+'; ans = random.randint(10, 50); self.a = random.randint(5, ans - 5); self.b = ans - self.a; self.spawn_delay_modifier = 800
        elif level == 7:
            op = '+'; ans = random.randint(10, 50); self.a = random.randint(5, ans - 5); self.b = ans - self.a; speed_grade = 1.3; self.spawn_delay_modifier = 500
        elif level == 8:
            op = '-'; self.a = random.randint(20, 50); self.b = random.randint(5, 19); ans = self.a - self.b; self.spawn_delay_modifier = 800
        elif level == 9:
            op = '-'; self.a = random.randint(20, 50); self.b = random.randint(5, 19); ans = self.a - self.b; speed_grade = 1.3; self.spawn_delay_modifier = 500
        elif level == 10:
            op = '-'; self.a = random.randint(2, 10); self.b = random.randint(11, 20); ans = self.a - self.b; speed_grade = 0.8; self.spawn_delay_modifier = 1200
        elif level == 11:
            op = '+'; ans = random.randint(40, 100); self.a = random.randint(10, ans - 10); self.b = ans - self.a; speed_grade = 0.9; self.spawn_delay_modifier = 1500
        elif level == 12:
            op = '-'; self.a = random.randint(50, 100); self.b = random.randint(10, 40); ans = self.a - self.b; speed_grade = 0.9; self.spawn_delay_modifier = 1500
        elif level == 13:
            op = random.choice(['+', '-'])
            if op == '+': ans = random.randint(40, 100); self.a = random.randint(10, ans - 10); self.b = ans - self.a
            else: self.a = random.randint(50, 100); self.b = random.randint(10, 40); ans = self.a - self.b
            speed_grade = 1.2; self.spawn_delay_modifier = 1000
        elif level == 14:
            op = random.choice(['+', '-'])
            if op == '+': ans = random.randint(20, 80); self.a = random.randint(5, ans - 5); self.b = ans - self.a
            else: self.a = random.randint(5, 15); self.b = random.randint(16, 30); ans = self.a - self.b
            speed_grade = 1.1; self.spawn_delay_modifier = 1200
        elif level == 15:
            op = 'x'; self.a = random.randint(2, 9); self.b = random.randint(2, 9); ans = self.a * self.b; speed_grade = 0.8; self.spawn_delay_modifier = 1800
        elif level == 16:
            op = 'x'; self.a = random.randint(2, 9); self.b = random.randint(2, 9); ans = self.a * self.b; speed_grade = 1.1; self.spawn_delay_modifier = 1400
        elif level == 17:
            op = ':'; ans = random.randint(2, 20); self.b = random.randint(2, 9); self.a = ans * self.b; speed_grade = 0.8; self.spawn_delay_modifier = 2000
        elif level == 18:
            op = ':'; ans = random.randint(2, 20); self.b = random.randint(2, 9); self.a = ans * self.b; speed_grade = 1.1; self.spawn_delay_modifier = 1500
        elif 19 <= level <= 22:
            op = random.choice(['+', '-', 'x', ':'])
            if op == '+': ans = random.randint(10, 80); self.a = random.randint(1, ans - 1); self.b = ans - self.a
            elif op == '-': self.a = random.randint(20, 70); self.b = random.randint(1, 19); ans = self.a - self.b
            elif op == 'x': self.a = random.randint(2, 9); self.b = random.randint(2, 9); ans = self.a * self.b
            elif op == ':': ans = random.randint(2, 15); self.b = random.randint(2, 7); self.a = ans * self.b
            speed_grade = 1.1; self.spawn_delay_modifier = 1200
        else:
            op = random.choice(['+', '-', 'x', ':'])
            if op == '+': ans = random.randint(50, 150); self.a = random.randint(10, ans - 10); self.b = ans - self.a
            elif op == '-': self.a = random.randint(10, 30); self.b = random.randint(40, 70); ans = self.a - self.b 
            elif op == 'x': self.a = random.randint(3, 12); self.b = random.randint(3, 9); ans = self.a * self.b
            elif op == ':': ans = random.randint(5, 25); self.b = random.randint(3, 11); self.a = ans * self.b
            speed_grade = 1.4; self.spawn_delay_modifier = 800

        self.answer = str(ans); self.question = f"{self.a}{op}{self.b}"
        self.x, self.y = random.randint(100, WIDTH - 100), -50
        dx, dy = self.target_pos[0] - self.x, self.target_pos[1] - self.y; self.angle = math.atan2(dy, dx)
        actual_speed = (HEIGHT * 0.0005) * speed_grade
        self.vx, self.vy = math.cos(self.angle) * actual_speed, math.sin(self.angle) * actual_speed; self.input = ""

    def update(self, time_scale):
        self.x += self.vx * time_scale; self.y += self.vy * time_scale

    def draw(self, surf, is_active):
        color = GREEN if is_active else RED
        thrust_angle = self.angle + math.pi
        thrust_x = self.x + math.cos(thrust_angle) * 18; thrust_y = self.y + math.sin(thrust_angle) * 18
        flicker = random.randint(6, 12)
        pygame.draw.circle(surf, ORANGE, (int(thrust_x), int(thrust_y)), flicker)
        pygame.draw.circle(surf, YELLOW, (int(thrust_x), int(thrust_y)), flicker - 3)
        pygame.draw.ellipse(surf, (40, 40, 60), (self.x - 35, self.y - 12, 70, 24))
        pygame.draw.ellipse(surf, color, (self.x - 35, self.y - 12, 70, 24), 2) 
        
        if pygame.time.get_ticks() % 600 < 300:
            pygame.draw.circle(surf, RED, (int(self.x - 28), int(self.y)), 3)
            pygame.draw.circle(surf, RED, (int(self.x + 28), int(self.y)), 3)

        pygame.draw.ellipse(surf, (30, 100, 150), (self.x - 18, self.y - 18, 36, 20))
        pygame.draw.ellipse(surf, CYAN, (self.x - 18, self.y - 18, 36, 20), 1)

        if is_active:
            p = 45 + math.sin(pygame.time.get_ticks()*0.01) * 5
            pygame.draw.circle(surf, GREEN, (int(self.x), int(self.y)), int(p), 1)

        txt_str = f"[{self.prefix}] {self.question}"
        if is_active: txt_str += f"={self.input}"
        
        txt = font_math.render(txt_str, True, WHITE)
        rect = txt.get_rect(center=(self.x, self.y - 45))
        frame_rect = rect.inflate(16, 10) 
        frame_surf = pygame.Surface((frame_rect.width, frame_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(frame_surf, (0, 0, 0, 180), frame_surf.get_rect(), border_radius=6)
        pygame.draw.rect(frame_surf, color, frame_surf.get_rect(), 2, border_radius=6) 
        surf.blit(frame_surf, frame_rect.topleft); surf.blit(txt, rect)

def draw_dashed_target_line(surf, color, start_pos, end_pos, dash_length=12, space_length=8, width=2):
    x1, y1 = start_pos; x2, y2 = end_pos; dx, dy = x2 - x1, y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0: return
    ux, uy = dx / distance, dy / distance
    total_segment = dash_length + space_length; num_dashes = int(distance / total_segment)
    for i in range(num_dashes + 1):
        start_d = i * total_segment; end_d = start_d + dash_length
        if end_d > distance: end_d = distance
        if start_d > distance: break
        p1 = (int(x1 + ux * start_d), int(y1 + uy * start_d))
        p2 = (int(x1 + ux * end_d), int(y1 + uy * end_d))
        pygame.draw.line(surf, color, p1, p2, width)

def draw_massive_carrier(surf, center_pos, target_alien):
    if target_alien:
        angle_laser = math.atan2(target_alien.y - center_pos[1], target_alien.x - center_pos[0])
        barrel_tip_x = center_pos[0] + math.cos(angle_laser) * 50; barrel_tip_y = center_pos[1] + math.sin(angle_laser) * 50
        target_radius = 45 
        end_target_x = target_alien.x - math.cos(angle_laser) * target_radius; end_target_y = target_alien.y - math.sin(angle_laser) * target_radius
        draw_dashed_target_line(surf, GREEN, (barrel_tip_x, barrel_tip_y), (end_target_x, end_target_y), dash_length=10, space_length=8, width=2)

    base_points = [(0, HEIGHT - 50), (WIDTH, HEIGHT - 50), (WIDTH - 150, HEIGHT + 150), (150, HEIGHT + 150)]
    pygame.draw.polygon(surf, (15, 25, 45), base_points)
    deck_points = [(WIDTH // 2 - 200, HEIGHT - 40), (WIDTH // 2 + 200, HEIGHT - 40), (WIDTH // 2 + 150, HEIGHT), (WIDTH // 2 - 150, HEIGHT)]
    pygame.draw.polygon(surf, GRAY, deck_points)
    pygame.draw.line(surf, WHITE, (WIDTH // 2, HEIGHT - 40), (WIDTH // 2, HEIGHT), 2)

    if target_alien: angle = math.atan2(target_alien.y - center_pos[1], target_alien.x - center_pos[0])
    else: angle = -math.pi / 2

    def rotate_point(pt, ang):
        x, y = pt; rx = x * math.cos(ang) - y * math.sin(ang); ry = x * math.sin(ang) + y * math.cos(ang)
        return (int(rx + center_pos[0]), int(ry + center_pos[1]))

    barrel_points = [rotate_point((50, -6), angle), rotate_point((50, 6), angle), rotate_point((-5, 6), angle), rotate_point((-5, -6), angle)]
    base_t_points = [rotate_point((30, -22), angle), rotate_point((30, 22), angle), rotate_point((-30, 22), angle), rotate_point((-30, -22), angle)]
    mount_points = [(center_pos[0] - 40, center_pos[1] + 15), (center_pos[0] + 40, center_pos[1] + 15), (center_pos[0] + 55, center_pos[1] + 45), (center_pos[0] - 55, center_pos[1] + 45)]
    
    pygame.draw.polygon(surf, (20, 20, 30), mount_points); pygame.draw.polygon(surf, WHITE, mount_points, 1)
    pygame.draw.polygon(surf, (30, 30, 50), base_t_points); pygame.draw.polygon(surf, WHITE, base_t_points, 2)
    pygame.draw.polygon(surf, CYAN, barrel_points); pygame.draw.polygon(surf, WHITE, barrel_points, 1)

# --- 6. ALUR UTAMA CORE STATE MACHINE ---
def main():
    play_backsound()
    stars = [Star() for _ in range(150)]
    
    username = ""
    current_state = "INPUT_NAME" 
    
    final_score = 0
    final_level = 1
    game_over_reason = "BASE DESTROYED"
    menu_selection = 0 

    while True:
        dt = clock.tick(60)
        screen.fill(BLACK)
        
        for star in stars:
            star.update(1.0); star.draw(screen)

        # ----------------------------------------------------
        # STATE A: MASUKKAN NICKNAME (ADVANCED COCKPIT VIEW)
        # ----------------------------------------------------
        if current_state == "INPUT_NAME":
            draw_spaceship_cockpit(screen)
            
            txt_title = font_big.render("ZMATH: GALACTIC", True, CYAN)
            txt_sub = font_math.render("INITIALIZE PILOT ID (NAME):", True, WHITE)
            txt_user = font_big.render(username + ("_" if pygame.time.get_ticks() % 1000 < 500 else ""), True, YELLOW)
            txt_start = font_ui.render("Press ENTER to Link Interface", True, GRAY)

            screen.blit(txt_title, txt_title.get_rect(center=(WIDTH//2, HEIGHT//2 - 140)))
            screen.blit(txt_sub, txt_sub.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
            screen.blit(txt_user, txt_user.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
            screen.blit(txt_start, txt_start.get_rect(center=(WIDTH//2, HEIGHT//2 + 150)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(username) > 0:
                        current_state = "MAIN_MENU"
                        menu_selection = 0
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif len(username) < 10 and event.unicode.isalnum():
                        username += event.unicode.upper()

        # ----------------------------------------------------
        # STATE B: MENU UTAMA PESAWAT (ADVANCED COCKPIT VIEW)
        # ----------------------------------------------------
        elif current_state == "MAIN_MENU":
            draw_spaceship_cockpit(screen)
            
            txt_welcome = font_math.render(f"WELCOME TO FLIGHT DECK, PILOT: {username}", True, GREEN)
            screen.blit(txt_welcome, txt_welcome.get_rect(center=(WIDTH//2, HEIGHT//2 - 150)))

            options = ["LAUNCH MISSION", "CHANGE PILOT ID", "QUIT GAME"]
            for idx, opt in enumerate(options):
                color = YELLOW if idx == menu_selection else WHITE
                prefix = "=> " if idx == menu_selection else "   "
                txt_opt = font_math.render(prefix + opt + prefix[::-1], True, color)
                screen.blit(txt_opt, txt_opt.get_rect(center=(WIDTH//2, HEIGHT//2 - 20 + (idx * 50))))

            txt_nav = font_ui.render("[W/S or UP/DOWN] Navigate  |  [ENTER] Confirm", True, GRAY)
            screen.blit(txt_nav, txt_nav.get_rect(center=(WIDTH//2, HEIGHT//2 + 160)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); return
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        menu_selection = (menu_selection - 1) % len(options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selection = (menu_selection + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if menu_selection == 0:
                            current_state = "GAMEPLAY"
                        elif menu_selection == 1:
                            username = ""
                            current_state = "INPUT_NAME"
                        elif menu_selection == 2:
                            pygame.quit(); return

        # ----------------------------------------------------
        # STATE C: GAMEPLAY & PAUSE ENGINE
        # ----------------------------------------------------
        elif current_state == "GAMEPLAY":
            global_highscore = get_highest_score()
            turret_pos = [WIDTH // 2, HEIGHT - 85] 
            aliens, particles, shockwaves = [], [], []
            active_alien = None
            
            score = 0
            questions_solved = 0
            level = 1
            
            base_spawn_delay = 2500
            spawn_timer = 0
            death_sequence, death_timer, screen_offset = False, 0, [0, 0]

            is_paused = False
            pause_selection = 0 
            blurred_surf = None
            resume_boost_timer = 0 

            gameplay_running = True
            while gameplay_running:
                inner_dt = clock.tick(60)

                # --- SUB-STATE: PAUSE MODE ---
                if is_paused:
                    screen.blit(blurred_surf, (0, 0)) 
                    m_width, m_height = 420, 240
                    m_rect = pygame.Rect((WIDTH//2 - m_width//2, HEIGHT//2 - m_height//2), (m_width, m_height))
                    pygame.draw.rect(screen, (10, 15, 30), m_rect, border_radius=12)
                    pygame.draw.rect(screen, CYAN, m_rect, 3, border_radius=12)

                    txt_pause_title = font_math.render("COMMAND INTERFACE", True, CYAN)
                    screen.blit(txt_pause_title, txt_pause_title.get_rect(center=(WIDTH//2, HEIGHT//2 - 70)))

                    res_color = YELLOW if pause_selection == 0 else WHITE
                    abort_color = YELLOW if pause_selection == 1 else WHITE

                    txt_res = font_math.render("> RESUME MISSION <" if pause_selection == 0 else "  RESUME MISSION  ", True, res_color)
                    txt_abort = font_math.render("> ABORT MISSION <" if pause_selection == 1 else "  ABORT MISSION  ", True, abort_color)

                    screen.blit(txt_res, txt_res.get_rect(center=(WIDTH//2, HEIGHT//2 - 5)))
                    screen.blit(txt_abort, txt_abort.get_rect(center=(WIDTH//2, HEIGHT//2 + 45)))

                    txt_nav_hint = font_ui.render("[W/S] Nav | [ENTER] Select | [ESC] Close", True, GRAY)
                    screen.blit(txt_nav_hint, txt_nav_hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 95)))

                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: pygame.quit(); return
                        if event.type == pygame.KEYDOWN:
                            if event.key in (pygame.K_UP, pygame.K_w): pause_selection = 0
                            elif event.key in (pygame.K_DOWN, pygame.K_s): pause_selection = 1
                            elif event.key == pygame.K_ESCAPE:
                                is_paused = False
                                resume_boost_timer = 1000 
                            elif event.key == pygame.K_RETURN:
                                if pause_selection == 0:
                                    is_paused = False
                                    resume_boost_timer = 1000
                                elif pause_selection == 1:
                                    final_score = score
                                    final_level = level
                                    game_over_reason = "MISSION ABORTED"
                                    save_leaderboard(username, final_score, final_level)
                                    gameplay_running = False
                                    current_state = "GAME_OVER"
                                    menu_selection = 0
                    continue

                # --- NORMAL PERTEMBURAN GAMEPLAY ---
                if death_sequence: 
                    screen_offset = [random.randint(-15, 15), random.randint(-15, 15)]
                    time_scale = 0.2
                else: 
                    screen_offset = [0, 0]
                    time_scale = 1.0

                if resume_boost_timer > 0:
                    resume_boost_timer -= inner_dt
                    time_scale *= 2.2 

                screen.fill(BLACK)
                for star in stars:
                    star.update(time_scale); star.draw(screen)

                if not death_sequence:
                    current_modifier = aliens[0].spawn_delay_modifier if aliens else 0
                    adapted_delay = max(1200, base_spawn_delay + current_modifier)
                    
                    spawn_timer += inner_dt
                    if spawn_timer > adapted_delay and len(aliens) < 5:
                        used_prefixes = [a.prefix for a in aliens]
                        available_prefixes = [c for c in "abcdefghijklmnopqrstuvwxyz" if c not in used_prefixes]
                        if available_prefixes:
                            chosen_prefix = random.choice(available_prefixes)
                            aliens.append(Alien(turret_pos, level, chosen_prefix))
                        spawn_timer = 0

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: pygame.quit(); return
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                is_paused = True
                                pause_selection = 0
                                raw_capture = screen.copy()
                                low_res = pygame.transform.smoothscale(raw_capture, (WIDTH // 28, HEIGHT // 28))
                                blurred_surf = pygame.transform.smoothscale(low_res, (WIDTH, HEIGHT))
                                dark_dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                                dark_dim.fill((5, 5, 15, 180))
                                blurred_surf.blit(dark_dim, (0, 0))
                                break

                            char = event.unicode.lower()
                            if not active_alien:
                                for a in aliens:
                                    if char == a.prefix: 
                                        active_alien = a; play_sfx("laser"); break
                            else:
                                if char.isdigit() or char == "-":
                                    active_alien.input += char
                                    if active_alien.input == active_alien.answer:
                                        play_sfx("explosion")
                                        score += 100 + (level * 10)
                                        questions_solved += 1
                                        level = min(25, 1 + (questions_solved // 15))
                                        
                                        shockwaves.append(Shockwave(active_alien.x, active_alien.y, GREEN, speed=3))
                                        for _ in range(12): particles.append(Particle(active_alien.x, active_alien.y, GREEN, speed_range=(1, 5)))
                                        aliens.remove(active_alien)
                                        active_alien = None
                                elif event.key == pygame.K_BACKSPACE: active_alien.input = ""
                else:
                    pygame.event.pump()
                    death_timer += 1
                    if death_timer > 120: 
                        final_score = score
                        final_level = level
                        game_over_reason = "BASE DESTROYED"
                        save_leaderboard(username, final_score, final_level)
                        gameplay_running = False
                        current_state = "GAME_OVER"
                        menu_selection = 0

                aliens.sort(key=lambda x: x.y)
                for a in aliens[:]:
                    a.update(time_scale); a.draw(screen, a == active_alien)
                    if a.y > HEIGHT - 70 and not death_sequence:
                        play_sfx("explosion")
                        death_sequence = True
                        active_alien = None
                        shockwaves.append(Shockwave(turret_pos[0], turret_pos[1], CYAN, speed=15))
                        for _ in range(100): particles.append(Particle(turret_pos[0], turret_pos[1], random.choice([CYAN, WHITE, ORANGE]), speed_range=(5, 15)))

                for p in particles[:]:
                    p.update(time_scale); p.draw(screen)
                    if p.alpha <= 0: particles.remove(p)
                for s in shockwaves[:]:
                    s.update(time_scale); s.draw(screen)
                    if s.alpha <= 0: shockwaves.remove(s)

                if not death_sequence: draw_massive_carrier(screen, turret_pos, active_alien)
                
                ui_text = f"PILOT: {username}   |   SCORE: {score:05d}   |   HIGHSCORE: {global_highscore:05d}"
                ui_text_2 = f"LEVEL: {level}/25   |   PROGRESS: {(questions_solved % 15)}/15"
                screen.blit(font_ui.render(ui_text, True, CYAN), (30, 25))
                screen.blit(font_ui.render(ui_text_2, True, YELLOW), (30, 55))
                
                if screen_offset != [0, 0]:
                    screen_copy = screen.copy(); screen.fill(BLACK); screen.blit(screen_copy, screen_offset)

                pygame.display.flip()

        # ----------------------------------------------------
        # STATE D: HALAMAN SUMMARY DATABASE (GAME OVER)
        # ----------------------------------------------------
        elif current_state == "GAME_OVER":
            s_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s_overlay.fill((10, 16, 30, 220)) 
            screen.blit(s_overlay, (0,0))
            
            pygame.draw.line(screen, CYAN, (0, 80), (WIDTH, 80), 2)
            pygame.draw.line(screen, CYAN, (0, HEIGHT - 130), (WIDTH, HEIGHT - 130), 2)

            real_rank = get_player_rank(username, final_score)

            txt_reason = font_big.render(game_over_reason, True, RED if game_over_reason == "BASE DESTROYED" else ORANGE)
            txt_p_score = font_math.render(f"FINAL SCORE: {final_score}", True, YELLOW)
            txt_p_lvl = font_math.render(f"FINAL LEVEL: {final_level}", True, WHITE)
            txt_p_rank = font_math.render(f"RANKING    : #{real_rank}", True, GREEN)
            
            screen.blit(txt_reason, (50, HEIGHT // 2 - 140))
            screen.blit(txt_p_score, (50, HEIGHT // 2 - 40))
            screen.blit(txt_p_lvl, (50, HEIGHT // 2))
            screen.blit(txt_p_rank, (50, HEIGHT // 2 + 40))

            # Render Ranking 5 Besar Dunia
            txt_board_title = font_math.render("GLOBAL LEADERBOARD (TOP 5)", True, CYAN)
            screen.blit(txt_board_title, (WIDTH // 2 + 40, HEIGHT // 2 - 140))
            
            top_scores = load_leaderboard()[:5]
            start_y = HEIGHT // 2 - 90
            for idx, data in enumerate(top_scores):
                is_current = (data["name"] == username and data["score"] == final_score)
                color_rank = GREEN if is_current else WHITE
                rank_str = f"{idx+1}. {data['name'].ljust(10)} - {str(data['score']).zfill(5)} (LVL {data['level']})"
                screen.blit(font_math.render(rank_str, True, color_rank), (WIDTH // 2 + 40, start_y + (idx * 35)))

            # Opsi Navigasi Pasca Pertempuran selesai
            end_options = ["RESTART MISSION", "CHANGE PILOT ID", "QUIT GAME"]
            for idx, opt in enumerate(end_options):
                color = YELLOW if idx == menu_selection else WHITE
                prefix = "> " if idx == menu_selection else "  "
                txt_opt = font_math.render(prefix + opt, True, color)
                screen.blit(txt_opt, (50, HEIGHT // 2 + 110 + (idx * 35)))

            txt_hint = font_ui.render("[W/S] Navigate Selection   |   [ENTER] Execute Choice", True, GRAY)
            screen.blit(txt_hint, txt_hint.get_rect(center=(WIDTH//2, HEIGHT - 50)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); return
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        menu_selection = (menu_selection - 1) % len(end_options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selection = (menu_selection + 1) % len(end_options)
                    elif event.key == pygame.K_RETURN:
                        if menu_selection == 0:
                            current_state = "GAMEPLAY"
                        elif menu_selection == 1:
                            username = ""
                            current_state = "INPUT_NAME"
                        elif menu_selection == 2:
                            pygame.quit(); return

        pygame.display.flip()

if __name__ == "__main__": 
    main()
