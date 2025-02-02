import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("벽돌 부수기 게임")

# 색상 정의
background_color = (0, 0, 0)  # 검정색 배경
paddle_color = (255, 255, 255)  # 흰색 패들
block_color = (200, 50, 50)  # 붉은색 블록
ball_color = (255, 255, 0)  # 노란색 공

# 패들 설정
paddle_width = 100
paddle_height = 15
paddle_x = (screen_width - paddle_width) / 2
paddle_y = screen_height - 40
paddle_speed = 7

# 블록 설정
block_width = 75
block_height = 20
block_rows = 5
block_columns = 10
block_margin = 10  # 블록 사이의 간격

# 블록 리스트 생성
blocks = []
for row in range(block_rows):
    block_row = []
    for col in range(block_columns):
        block_x = col * (block_width + block_margin) + block_margin
        block_y = row * (block_height + block_margin) + block_margin
        block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
        block_row.append(block_rect)
    blocks.append(block_row)

# 공 설정
ball_radius = 10
ball_x = paddle_x + paddle_width / 2  # 패들 위 중앙에 위치
ball_y = paddle_y - ball_radius - 1
ball_speed_x = 4  # 공의 X축 속도
ball_speed_y = -4  # 공의 Y축 속도

# 프레임 레이트 설정
clock = pygame.time.Clock()
fps = 60

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    # 공 움직임 업데이트
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # 공이 화면 경계에 부딪힐 때 반사
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_speed_x = -ball_speed_x  # X축 반사
    if ball_y - ball_radius <= 0:
        ball_speed_y = -ball_speed_y  # Y축 반사 (상단 벽)

    # 바닥에 닿을 때 게임 종료 조건
    if ball_y + ball_radius >= screen_height:
        print("Game Over")
        running = False

    # 화면 채우기
    screen.fill(background_color)

    # 패들 그리기
    pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))

    # 블록 그리기
    for row in blocks:
        for block in row:
            pygame.draw.rect(screen, block_color, block)

    # 공 그리기
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 제한
    clock.tick(fps)

# 게임 종료
pygame.quit()
sys.exit()
