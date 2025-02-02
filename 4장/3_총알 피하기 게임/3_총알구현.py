import pygame
import random
import math
import sys
import os

# Pygame 초기화
pygame.init()

# 색상 정의
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge Game")

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Arial", 60)

# 플레이어 클래스 정의
class Player:
    """플레이어 클래스"""
    def __init__(self):
        self.size = 20
        self.speed = 4
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.size, self.size)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# 총알 클래스 정의
class Bullet:
    """일반 총알 클래스"""
    def __init__(self, player, bullets):
        self.x, self.y = self._spawn_on_border(bullets)
        self.radius = 3
        self.speed = random.uniform(1, 2)

        self.target_x = player.rect.centerx
        self.target_y = player.rect.centery
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

    def _spawn_on_border(self, bullets):
        """기존 총알과 최소 거리가 필요한 위치에 총알 생성"""
        while True:
            side = random.choice(['left', 'right', 'top', 'bottom'])
            if side == 'left':
                x, y = 0, random.randint(0, SCREEN_HEIGHT)
            elif side == 'right':
                x, y = SCREEN_WIDTH - 1, random.randint(0, SCREEN_HEIGHT)
            elif side == 'top':
                x, y = random.randint(0, SCREEN_WIDTH), 0
            else:
                x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT - 1

            if all(math.hypot(b.x - x, b.y - y) > 30 for b in bullets):
                return x, y

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)



# 게임 루프 (플레이어 및 총알 표시)
if __name__ == "__main__":
    player = Player()
    bullets = [Bullet(player, []) for _ in range(10)]  # 10개의 총알 생성
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw()

        # 총알 이동 및 그리기
        for bullet in bullets:
            bullet.move()
            bullet.draw()

        pygame.display.flip()
        clock.tick(FPS)
