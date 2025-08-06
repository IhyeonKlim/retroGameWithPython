import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color and Time Example")

# 색상 정의
colors = [(255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0)]  # 흰색, 빨강, 파랑, 초록
color_index = 0

# 시간 설정
CHANGE_INTERVAL = 1000  # 1초 간격
last_change_time = pygame.time.get_ticks()

# 폰트 설정
font = pygame.font.SysFont('Arial', 24)  # 글꼴 및 크기 설정

# 게임 루프
running = True
while running:
    # 현재 시간 가져오기
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - last_change_time) / 1000  # 초 단위 경과 시간 계산

    # 배경색 변경 조건 확인
    if current_time - last_change_time > CHANGE_INTERVAL:
        color_index += 1
        if color_index >= len(colors):
            color_index = 0  # 색상 순환
        last_change_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경색 설정
    screen.fill(colors[color_index])

    # 경과 시간 텍스트 생성
    time_text = font.render(f"Elapsed Time: {elapsed_time:.2f} sec", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))  # 좌상단에 텍스트 표시

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
