import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter 🚀")

# Clock
clock = pygame.time.Clock()

# Load spaceship image
SPACESHIP_IMG = pygame.image.load(r"C:\Users\LENOVO\Desktop\Python program\Game\Spaceship.png")
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (50, 50))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = SPACESHIP_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -8
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 7)
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - 50)

# Groups
player = Player()
player_group = pygame.sprite.GroupSingle(player)
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

for _ in range(5):
    asteroid = Asteroid()
    asteroids.add(asteroid)

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)
    
    player.move(keys)
    bullets.update()
    asteroids.update()
    
    # Collision detection
    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, asteroids, True)
        for hit in hits:
            asteroid = Asteroid()
            asteroids.add(asteroid)
            bullet.kill()
            score += 10
    
    if pygame.sprite.spritecollide(player, asteroids, False):
        running = False
    
    # Draw elements
    player_group.draw(screen)
    bullets.draw(screen)
    asteroids.draw(screen)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)

# Game Over Screen
screen.fill(BLACK)
game_over_text = font.render("GAME OVER! Final Score: " + str(score), True, RED)
screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
