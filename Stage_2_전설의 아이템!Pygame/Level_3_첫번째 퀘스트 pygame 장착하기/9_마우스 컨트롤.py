import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click to Create Rectangle")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 사각형의 크기
rect_width = 50
rect_height = 50

# 사각형의 위치 리스트
rectangles = []  # 생성된 사각형의 위치를 저장할 리스트

# 게임 루프 설정
running = True

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 마우스 클릭 이벤트 처리
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos  # 클릭한 위치 가져오기
            print(f"Clicked at: ({mouse_x}, {mouse_y})")  # 클릭한 좌표 출력

            # 클릭한 위치에 사각형 추가
            rect_x = mouse_x - rect_width // 2
            rect_y = mouse_y - rect_height // 2
            rectangles.append((rect_x, rect_y))  # 사각형 위치를 리스트에 추가

    # 화면 초기화
    screen.fill(WHITE)

    # 모든 사각형 그리기
    for (x, y) in rectangles:
        pygame.draw.rect(screen, RED, (x, y, rect_width, rect_height))

    # 화면 업데이트
    pygame.display.flip()

# 게임 종료
pygame.quit()
