import sys
import pygame

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 타이틀 설정
pygame.display.set_caption("PONG")

# 색상 정의
BLACK = (0, 0, 0)       # 배경색 (검정)
WHITE = (255, 255, 255) # 테두리색 (하얀색)

# FPS 설정
fps_value = 60
clock = pygame.time.Clock()

# 테두리 및 여백 설정
border_thickness = 10    # 테두리 두께
border_padding = 10      # 테두리를 안쪽으로 더 옮길 여백

# 플레이 구역 설정
play_area_x = border_thickness + border_padding  # 구역의 X 좌표 시작점
play_area_y = border_thickness + border_padding  # 구역의 Y 좌표 시작점
play_area_width = screen_width - 2 * (border_thickness + border_padding)  # 구역의 너비
play_area_height = screen_height - 2 * (border_thickness + border_padding) # 구역의 높이

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면을 검정색으로 채움 (전체 배경)
    screen.fill(BLACK)

    # 하얀색 테두리가 있는 직사각형을 그림
    pygame.draw.rect(screen, WHITE, (play_area_x, play_area_y, play_area_width, play_area_height), border_thickness)

    # 화면 업데이트
    pygame.display.update()

    # 초당 프레임 설정
    clock.tick(fps_value)

# Pygame 종료
pygame.quit()
sys.exit()
