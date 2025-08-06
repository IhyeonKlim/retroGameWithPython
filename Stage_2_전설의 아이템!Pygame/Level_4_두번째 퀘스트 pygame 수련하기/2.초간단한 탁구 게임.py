import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Ping Pong Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 패들1 설정
paddle1_x = 10
paddle1_y = HEIGHT // 2 - 30
paddle1_width = 10
paddle1_height = 60

# 패들2 설정
paddle2_x = WIDTH - 20
paddle2_y = HEIGHT // 2 - 30
paddle2_width = 10
paddle2_height = 60

# 공 설정 (pygame.Rect 사용)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_speed_x = 3
ball_speed_y = 3

# 키 상태 추적 변수
paddle1_up = False
paddle1_down = False
paddle2_up = False
paddle2_down = False

# 게임 루프 설정
clock = pygame.time.Clock()
running = True

# 게임 루프 시작
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키가 눌렸을 때
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1_up = True
            elif event.key == pygame.K_s:
                paddle1_down = True
            elif event.key == pygame.K_UP:
                paddle2_up = True
            elif event.key == pygame.K_DOWN:
                paddle2_down = True

        # 키가 떼어졌을 때
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                paddle1_up = False
            elif event.key == pygame.K_s:
                paddle1_down = False
            elif event.key == pygame.K_UP:
                paddle2_up = False
            elif event.key == pygame.K_DOWN:
                paddle2_down = False

    # 패들1 이동 처리
    if paddle1_up and paddle1_y > 0:
        paddle1_y = paddle1_y - 5
    if paddle1_down and paddle1_y + paddle1_height < HEIGHT:
        paddle1_y = paddle1_y + 5

    # 패들2 이동 처리
    if paddle2_up and paddle2_y > 0:
        paddle2_y = paddle2_y - 5
    if paddle2_down and paddle2_y + paddle2_height < HEIGHT:
        paddle2_y = paddle2_y + 5

    # 공 이동 처리
    ball.x = ball.x + ball_speed_x
    ball.y = ball.y + ball_speed_y

    # 공 경계 체크 (화면 위/아래 충돌)
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # 공과 패들1 충돌 처리
    if (ball.left <= paddle1_x + paddle1_width and
        paddle1_y < ball.bottom and
        paddle1_y + paddle1_height > ball.top):
        ball_speed_x = -ball_speed_x

    # 공과 패들2 충돌 처리
    if (ball.right >= paddle2_x and
        paddle2_y < ball.bottom and
        paddle2_y + paddle2_height > ball.top):
        ball_speed_x = -ball_speed_x

    # 공이 왼쪽 또는 오른쪽 경계를 벗어나면 종료
    if ball.left <= 0 or ball.right >= WIDTH:
        print("Game Over! Ball exited the boundary.")
        running = False

    # 화면 초기화
    screen.fill(BLACK)

    # 패들1 그리기
    pygame.draw.rect(screen, WHITE,
                     (paddle1_x, paddle1_y, paddle1_width, paddle1_height))

    # 패들2 그리기
    pygame.draw.rect(screen, WHITE,
                     (paddle2_x, paddle2_y, paddle2_width, paddle2_height))

    # 공 그리기 (사각형으로 그리기)
    pygame.draw.rect(screen, WHITE, ball)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)  # 초당 60프레임 설정

pygame.quit()