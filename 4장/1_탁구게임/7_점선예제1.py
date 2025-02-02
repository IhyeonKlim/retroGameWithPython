import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS 설정
clock = pygame.time.Clock()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면을 검정색으로 채움
    screen.fill(BLACK)

    # 하얀색 선을 (50, 50)에서 (350, 50)까지 그림, 선의 두께는 5
    pygame.draw.line(screen, WHITE, (50, 50), (350, 50), 5)

    # 화면 업데이트
    pygame.display.update()

    # 초당 프레임 설정
    clock.tick(60)

# Pygame 종료
pygame.quit()
sys.exit()
