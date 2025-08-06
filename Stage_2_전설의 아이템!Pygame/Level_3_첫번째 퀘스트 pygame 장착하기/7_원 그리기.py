import pygame  # pygame 모듈 임포트

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Circle Example")  # 창 제목 설정

# 색상 정의
WHITE = (255, 255, 255)  # 배경색 (흰색)
BLUE = (0, 0, 255)  # 사각형 색상 (파랑)

# 원 설정
circle_radius = 50  # 원의 반지름
circle_x = WIDTH // 2  # 화면 중앙에 위치하도록 X 좌표 설정
circle_y = HEIGHT // 2  # 화면 중앙에 위치하도록 Y 좌표 설정

# 메인 루프
running = True
while running:
    for event in pygame.event.get():  # 이벤트 처리
        if event.type == pygame.QUIT:  # 창 닫기 이벤트가 발생하면
            running = False

    # 배경색을 흰색으로 채우기
    screen.fill(WHITE)

    # 원 그리기
    pygame.draw.circle(screen, BLUE, (circle_x, circle_y), circle_radius)

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
