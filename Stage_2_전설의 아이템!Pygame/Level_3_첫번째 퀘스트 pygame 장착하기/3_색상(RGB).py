import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Example")

# 색상 정의
colors = [(255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0)]  # 흰색, 빨강, 파랑, 초록
color_index = 0

# 시간 설정
CHANGE_INTERVAL = 1000  # 1초 간격
last_change_time = pygame.time.get_ticks()

# 게임 루프
running = True
while running:
    current_time = pygame.time.get_ticks()
    if current_time - last_change_time > CHANGE_INTERVAL:
        color_index += 1
        if color_index >= len(colors):
            color_index = 0  # 리스트의 마지막 색상 이후에는 처음 색상으로 돌아갑니다.
        last_change_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경색 설정
    screen.fill(colors[color_index])
    pygame.display.flip()

# Pygame 종료
pygame.quit()
