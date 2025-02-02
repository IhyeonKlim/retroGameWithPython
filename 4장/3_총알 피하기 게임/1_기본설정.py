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

# 게임 루프 (초기 화면)
if __name__ == "__main__":
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 화면에 종료 방법 메시지 표시 (테스트용)
        text = font.render("Press the 'X' button on the window to close.", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)
