import pygame
import os
from spritesheet import SpriteSheet

# Inisialisasi pygame
pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multichar Game")
clock = pygame.time.Clock()
FPS = 60

# Warna
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load sound (dummy)
# attack_sound = pygame.mixer.Sound("assets/sounds/attack.wav")

# Load sprite sheets
SPRITE_PATH = "assets/sprites"

class Player(pygame.sprite.Sprite):
    def __init__(self, folder, pos, controls):
        super().__init__()
        self.spritesheet = SpriteSheet(os.path.join(SPRITE_PATH, folder))
        self.animations = {
            'idle': self.spritesheet.load_strip("Idle.png", 8),
            'run': self.spritesheet.load_strip("Run.png", 8),
            'attack': self.spritesheet.load_strip("Attack_1.png", 8),
        }
        self.state = 'idle'
        self.frame = 0
        self.image = self.animations[self.state][self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 4
        self.controls = controls
        self.health = 100
        self.score = 0
        self.facing_right = True
        self.attacking = False
        self.animation_timer = pygame.time.get_ticks()


    def update(self, keys):
        dx = 0
        prev_state = self.state

        # Gerakan
        if keys[self.controls['left']]:
            dx = -self.speed
            self.facing_right = False
            self.state = 'run'
        elif keys[self.controls['right']]:
            dx = self.speed
            self.facing_right = True
            self.state = 'run'
        else:
            self.state = 'idle'

        # Serang
        if keys[self.controls['attack']]:
            self.state = 'attack'
            if not self.attacking:  # baru mulai serang
            #     attack_sound.play()
                self.attacking = True
        else:
            self.attacking = False

        # Reset frame jika animasi berubah
        if self.state != prev_state:
            self.frame = 0
            self.animation_timer = pygame.time.get_ticks()

        # Ganti frame hanya setiap 100ms
        now = pygame.time.get_ticks()
        if now - self.animation_timer > 1000:
            self.frame = (self.frame + 1) % len(self.animations[self.state])
            self.animation_timer = now

        # Ambil frame & flip jika perlu
        self.image = self.animations[self.state][self.frame]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += dx


    def draw_health_bar(self):
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 50

    def update(self):
        pass

# Kontrol dua pemain
controls1 = {'left': pygame.K_a, 'right': pygame.K_d, 'attack': pygame.K_w}
controls2 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'attack': pygame.K_UP}

# Buat objek
player1 = Player("Musketeer", (100, 400), controls1)
player2 = Player("Enchantress", (300, 400), controls2)
enemy = Enemy((600, 400))

players = pygame.sprite.Group(player1, player2)
enemies = pygame.sprite.Group(enemy)

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    players.update(keys)
    enemies.update()

    # Cek serangan
    for player in players:
        if player.attacking:
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    e.health -= 1
                    if e.health <= 0:
                        player.score += 1
                        enemies.remove(e)

    # Gambar
    players.draw(screen)
    enemies.draw(screen)
    for player in players:
        player.draw_health_bar()

    # Skor
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"P1 Score: {player1.score}  |  P2 Score: {player2.score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

pygame.quit()
