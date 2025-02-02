import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 공의 초기 위치와 속도
ball_x = 200  # 공의 X 좌표
ball_y = 200  # 공의 Y 좌표
ball_speed_x = 2  # X 축 속도
ball_speed_y = 3  # Y 축 속도
ball_radius = 20  # 공의 반지름

# 게임 루프
running = True
clock = pygame.time.Clock()  # 속도 조절을 위한 시계 객체

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 공의 위치 업데이트
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # 경계 체크 (화면의 가장자리에서 튕기기)
    if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
        ball_speed_x = -ball_speed_x  # X 방향 반전
    if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
        ball_speed_y = -ball_speed_y  # Y 방향 반전

    # 화면 지우기 및 공 그리기
    screen.fill(WHITE)  # 화면을 흰색으로 초기화
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)  # 공 그리기

    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 설정
    clock.tick(60)

# Pygame 종료
pygame.quit()
