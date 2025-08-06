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
WHITE = (255, 255, 255) #RGB 값으로 표현합니다.

# FPS 설정
fps_value = 60
clock = pygame.time.Clock()

# Pygame 텍스트 렌더링 후 화면에 표시하는 예제
font = pygame.font.Font(None, 50)  # 폰트 객체 생성

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면을 흰색으로 채움

    text_surface = font.render("Hello, World!", True, (255, 255, 255))  # 텍스트 렌더링

    # 텍스트를 화면의 (100, 100) 좌표에 그리기
    screen.blit(text_surface, (100, 100))
    # 화면 업데이트
    pygame.display.update()

    # 초당 프레임 설정
    clock.tick(fps_value)

# Pygame 종료
pygame.quit()
sys.exit()


