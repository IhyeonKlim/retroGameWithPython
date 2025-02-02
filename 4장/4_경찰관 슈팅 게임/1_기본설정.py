import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cop Shooting Game")

# 색상 정의
BLACK = (0, 0, 0)

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 기본 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임 종료 이벤트
            running = False

    # 화면 검은색으로 채우기
    screen.fill(BLACK)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

