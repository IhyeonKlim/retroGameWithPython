import pygame
import sys
import random

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
font_color = (255, 255, 255)  # 흰색 텍스트

# 패들 설정
paddle_width = 100
paddle_height = 15
paddle_x = (screen_width - paddle_width) / 2
paddle_y = screen_height - 40
paddle_speed = 7
original_paddle_width = paddle_width  # 기본 패들 너비
paddle_extended_duration = 5000  # 패들 길이 증가 지속 시간 (밀리초)
paddle_extended_end_time = 0  # 패들 길이 증가 종료 시간

# 블록 설정
block_rows = 5
block_columns = 10
block_margin = 5  # 블록 사이의 간격

# 블록 크기 계산
total_margin = block_margin * (block_columns + 1)
block_width = (screen_width - total_margin) / block_columns
block_height = 30  # 고정된 블록 높이

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

# 점수 및 생명 설정
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# 아이템 설정
item_chance = 1  # 아이템 생성 확률 (100%)
items = []  # 화면에 생성된 아이템 리스트
item_speed = 2  # 아이템의 낙하 속도
color_change_speed = 5  # 색상 변화 속도

# 프레임 레이트 설정
clock = pygame.time.Clock()
fps = 60


# 색상 변화 함수
def get_rainbow_color(offset):
    """offset에 따라 무지개 색상을 반환"""
    r = (offset % 255)
    g = (offset + 85) % 255
    b = (offset + 170) % 255
    return (r, g, b)


# 게임 루프
running = True
while running:
    # 현재 시간 계산
    current_time = pygame.time.get_ticks()

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

    # 패들 길이 증가 효과 해제
    if current_time > paddle_extended_end_time:
        paddle_width = original_paddle_width

    # 공 움직임 업데이트
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # 공이 화면 경계에 부딪힐 때 반사
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_speed_x = -ball_speed_x  # X축 반사
    if ball_y - ball_radius <= 0:
        ball_speed_y = -ball_speed_y  # Y축 반사 (상단 벽)

    # 바닥에 닿을 때 생명 감소 처리
    if ball_y + ball_radius >= screen_height:
        lives -= 1
        if lives <= 0:
            print("Game Over")
            running = False
        else:
            # 공과 패들 위치 초기화
            ball_x = paddle_x + paddle_width / 2
            ball_y = paddle_y - ball_radius - 1
            ball_speed_y = -ball_speed_y  # Y축 방향 초기화

    # 블록과 충돌 감지 및 처리
    block_collision = False
    for row in blocks:
        for block in row:
            if block.colliderect(
                    pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                # 좌우 및 상하 충돌 처리
                if ball_x < block.left or ball_x > block.right:
                    ball_speed_x = -ball_speed_x
                if ball_y < block.top or ball_y > block.bottom:
                    ball_speed_y = -ball_speed_y
                row.remove(block)  # 블록 제거
                score += 10  # 점수 추가

                # 아이템 생성 확률 적용
                if random.random() < item_chance:
                    item_rect = pygame.Rect(block.x + block.width / 2 - 10, block.y + block.height / 2, 20, 20)
                    items.append(item_rect)

                block_collision = True
                break
        if block_collision:
            break

    # 패들과 공의 충돌 감지 및 처리
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    if paddle_rect.colliderect(
            pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
        if ball_x < paddle_rect.left or ball_x > paddle_rect.right:
            ball_speed_x = -ball_speed_x
        ball_speed_y = -ball_speed_y

    # 아이템 이동 및 패들과의 충돌 감지
    for item in items[:]:
        item.y += item_speed  # 아이템 낙하
        if paddle_rect.colliderect(item):  # 패들과 충돌 시
            score += 50  # 점수 추가 (아이템 효과)
            paddle_width = original_paddle_width * 1.5  # 패들 길이 증가
            paddle_extended_end_time = current_time + paddle_extended_duration  # 효과 종료 시간 설정
            items.remove(item)  # 아이템 제거
        elif item.y > screen_height:  # 화면 아래로 떨어진 아이템 제거
            items.remove(item)

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

    # 아이템 그리기 - 무지개 색상 적용
    color_offset = (current_time // color_change_speed) % 255
    for item in items:
        rainbow_color = get_rainbow_color(color_offset)
        pygame.draw.rect(screen, rainbow_color, item)

    # 점수 및 생명 표시
    score_text = font.render(f"Score: {score}", True, font_color)
    lives_text = font.render(f"Lives: {lives}", True, font_color)
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (screen_width - 120, 20))

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 제한
    clock.tick(fps)

# 게임 종료
pygame.quit()
sys.exit()
