import pygame
import sys

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Background")

# 배경 이미지 로드
background_image = pygame.image.load("background.png")  # 이미지 경로 수정
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 배경 위치 초기화
bg_y1 = 0
bg_y2 = -SCREEN_HEIGHT  # 첫 번째 이미지 바로 위에 두 번째 이미지를 배치

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

#스피드 설정
speed =5

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경 위치 업데이트
    bg_y1 += speed  # 배경이 위로 스크롤되도록 양수로 설정
    bg_y2 += speed

    # 화면 밖으로 나간 배경을 재배치
    if bg_y1 >= SCREEN_HEIGHT:
        bg_y1 = -SCREEN_HEIGHT
    if bg_y2 >= SCREEN_HEIGHT:
        bg_y2 = -SCREEN_HEIGHT

    # 화면에 배경 이미지 그리기
    screen.blit(background_image, (0, bg_y1))
    screen.blit(background_image, (0, bg_y2))

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(FPS)

# 종료
pygame.quit()
sys.exit()
