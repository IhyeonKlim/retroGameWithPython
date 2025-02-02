import pygame
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

# 폰트 설정
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

# 게임 루프 추가 (플레이어 표시 및 이동 구현)
if __name__ == "__main__":
    player = Player()
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

        pygame.display.flip()
        clock.tick(FPS)
