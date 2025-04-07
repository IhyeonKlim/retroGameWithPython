import sys
import pygame
from pygame.locals import QUIT

# 게임 화면 크기
screen_size = {
    'width': 640,
    'height': 480
}

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((screen_size['width'], screen_size['height']))
pygame.display.set_caption("우주 침략자 게임")
clock = pygame.time.Clock()
fps = 300

# 게임 루프
def update_game():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 화면 초기화 및 업데이트
    screen.fill(black)
    pygame.display.update()

# 메인 루프
while True:
    update_game()
    clock.tick(fps)