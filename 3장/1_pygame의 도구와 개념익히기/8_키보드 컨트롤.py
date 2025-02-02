import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT  # 필요한 키와 QUIT 상수 불러오기

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Square")

# 색상과 사각형 초기 설정
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
rect_x = 200 # 사각형의 x
rect_y = 200 #y 좌표를 개별 변수로 설정
rect_size = 30

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # 키보드 입력 처리 (방향키 이벤트 처리)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                rect_x -= 5
            elif event.key == K_RIGHT:
                rect_x += 5
            elif event.key == K_UP:
                rect_y -= 5
            elif event.key == K_DOWN:
                rect_y += 5

    pygame.draw.rect(screen, GREEN, (rect_x, rect_y, rect_size, rect_size))
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
