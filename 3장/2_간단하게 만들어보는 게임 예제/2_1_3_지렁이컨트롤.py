import pygame  # Pygame 라이브러리를 불러옵니다.

# 1️⃣ **게임 초기화**
pygame.init()  # Pygame을 초기화하여 게임을 실행할 준비를 합니다.

# 화면 설정
WIDTH = 500  # 게임 창의 너비
HEIGHT = 500  # 게임 창의 높이
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 설정한 크기로 게임 창을 생성
pygame.display.set_caption("지렁이 게임")  # 창 제목 설정

# 색상 설정
WHITE = (255, 255, 255)  # 배경색
GREEN = (0, 200, 0)  # 지렁이 색상

# 2️⃣ **지렁이 생성**
TILE_SIZE = 40  # 지렁이의 크기 (한 칸 크기)
snake = [(240, 240)]  # 지렁이의 초기 위치 (가운데에 가깝게 설정)

# 3️⃣ **지렁이 이동 관련 변수 설정**
dx, dy = 0, 0  # 초기 이동 방향 (멈춘 상태)

# 게임 속도 조절을 위한 시계 생성
clock = pygame.time.Clock()

# 게임 루프 실행 여부
running = True

# 🎮 게임 루프 (게임이 실행되는 동안 계속 반복됨)
while running:
    screen.fill(WHITE)  # 화면을 흰색으로 채워서 이전 프레임을 지움

    # 3️⃣ **키 입력을 통한 지렁이 이동 방향 설정**
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 사용자가 창을 닫으면
            running = False  # 루프 종료
        elif event.type == pygame.KEYDOWN:  # 키보드 입력 감지
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -TILE_SIZE, 0  # 왼쪽으로 이동
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = TILE_SIZE, 0  # 오른쪽으로 이동
            elif event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -TILE_SIZE  # 위쪽으로 이동
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, TILE_SIZE  # 아래쪽으로 이동

    # 3️⃣ **지렁이 이동**
    if dx != 0 or dy != 0:  # 이동 방향이 설정된 경우에만 실행
        head_x, head_y = snake[0]  # 현재 머리 위치 가져오기
        new_head = (head_x + dx, head_y + dy)  # 새로운 머리 위치 계산
        snake.insert(0, new_head)  # 새로운 머리를 리스트 앞에 추가
        snake.pop()  # 꼬리를 제거하여 길이를 유지

    # 2️⃣ **지렁이 그리기**
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], TILE_SIZE, TILE_SIZE))

    pygame.display.flip()  # 화면을 업데이트하여 변경 사항을 적용

    clock.tick(10)  # 게임 속도를 조절 (1초에 10번 이동)

# 게임 종료
pygame.quit()  # pygame을 종료하여 리소스를 정리합니다.

