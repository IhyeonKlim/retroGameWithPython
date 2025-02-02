import pygame
import sys

# 초기화 및 화면 설정
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 객체 생성
rect = pygame.Rect(0, 0, 50, 50)  # (x, y, width, height)
rect.center = (400, 300)  # 객체를 화면 중앙에 배치

# 색상
color = (0, 128, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키보드 입력에 따라 객체 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect.centerx -= 5  # 중심을 기준으로 왼쪽 이동
    if keys[pygame.K_RIGHT]:
        rect.centerx += 5  # 중심을 기준으로 오른쪽 이동
    if keys[pygame.K_UP]:
        rect.centery -= 5  # 중심을 기준으로 위로 이동
    if keys[pygame.K_DOWN]:
        rect.centery += 5  # 중심을 기준으로 아래로 이동

    # 화면 그리기
    screen.fill((0, 0, 0))  # 배경 검정색
    pygame.draw.rect(screen, color, rect)  # 객체 그리기
    pygame.display.flip()

    # 초당 60프레임으로 설정
    clock.tick(60)

