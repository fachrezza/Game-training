import pygame
import os
from spritesheet import SpriteSheet

# Inisialisasi pygame
pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turn-Based Battle Game")
clock = pygame.time.Clock()
FPS = 60

# Warna
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load sound
# attack_sound = pygame.mixer.Sound("assets/sounds/attack.wav")

# Load sprite sheet path
SPRITE_PATH = "assets/sprites"

class Player(pygame.sprite.Sprite):
    def __init__(self, folder, pos):
        super().__init__()
        self.spritesheet = SpriteSheet(os.path.join(SPRITE_PATH, folder))
        self.animations = {
            'idle': self.spritesheet.load_strip("Idle.png", 8),
            'attack': self.spritesheet.load_strip("Attack_1.png", 8),
            'hurt': self.spritesheet.load_strip("Hurt.png", 3),
        }
        self.state = 'idle'
        self.frame = 0
        self.image = self.animations[self.state][self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 100
        self.score = 0
        self.animation_timer = pygame.time.get_ticks()
        self.facing_right = True
        self.attacking = False

    def set_state(self, state):
        self.state = state
        self.frame = 0
        self.animation_timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.animation_timer > 150:
            self.frame = (self.frame + 1) % len(self.animations[self.state])
            self.animation_timer = now

        self.image = self.animations[self.state][self.frame]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw_health_bar(self):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, max(0, self.health), 5))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 100

    def update(self):
        pass

# Buat pemain dan musuh
player1 = Player("Musketeer", (100, 400))
player2 = Player("Enchantress", (300, 400))
enemy = Enemy((600, 400))

players = [player1, player2]
current_turn = 0
phase = "player"
waiting_for_input = True

font = pygame.font.SysFont(None, 24)

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update animasi pemain dan musuh
    for p in players:
        p.update()
    enemy.update()

    # Turn-based logic
    if phase == "player":
        active_player = players[current_turn]
        if waiting_for_input:
            if (current_turn == 0 and keys[pygame.K_w]) or (current_turn == 1 and keys[pygame.K_UP]):
                active_player.set_state('attack')
                # attack_sound.play()
                enemy.health -= 10
                waiting_for_input = False
        else:
            # Selesai animasi? ganti giliran
            if active_player.frame == len(active_player.animations['attack']) - 1:
                active_player.set_state('idle')
                current_turn += 1
                waiting_for_input = True
                if current_turn >= len(players):
                    current_turn = 0
                    phase = "enemy"

    elif phase == "enemy":
        for p in players:
            p.set_state('hurt')
            p.health -= 10
        phase = "player"

    # Gambar sprite
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)
    screen.blit(enemy.image, enemy.rect)

    for p in players:
        p.draw_health_bar()

    # Gambar teks
    turn_text = font.render(f"Turn: Player {current_turn + 1 if phase == 'player' else 'Enemy'}", True, (0, 0, 0))
    screen.blit(turn_text, (20, 20))
    score_text = font.render(f"Enemy HP: {enemy.health}", True, (0, 0, 0))
    screen.blit(score_text, (20, 50))

    pygame.display.flip()

pygame.quit()
