import pygame
import random  # 랜덤한 위치에 먹이를 생성하기 위해 추가

# 1️⃣ **게임 초기화**
pygame.init()

# 화면 설정
WIDTH = 500  # 게임 창 너비
HEIGHT = 500  # 게임 창 높이
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("지렁이 게임")

# 색상 설정
WHITE = (255, 255, 255)  # 배경색
GREEN = (0, 200, 0)  # 지렁이 색상
RED = (255, 0, 0)  # 먹이 색상

# 2️⃣ **지렁이 생성**
TILE_SIZE = 40
snake = [(240, 240)]

# 3️⃣ **지렁이 이동 관련 변수**
dx, dy = 0, 0

# 4️⃣ **먹이 생성 함수**
def spawn_food():
    """먹이를 랜덤한 위치에 생성하는 함수"""
    return (
        random.randint(0, (WIDTH // TILE_SIZE) - 1) * TILE_SIZE,
        random.randint(0, (HEIGHT // TILE_SIZE) - 1) * TILE_SIZE
    )

# 4️⃣ **초기 먹이 위치 설정**
food_x, food_y = spawn_food()

# 게임 속도 조절을 위한 시계
clock = pygame.time.Clock()

# 게임 루프 실행 여부
running = True

# 🎮 게임 루프 시작
while running:
    screen.fill(WHITE)

    # 3️⃣ **키 입력을 통한 지렁이 이동 방향 설정**
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -TILE_SIZE, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = TILE_SIZE, 0
            elif event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -TILE_SIZE
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, TILE_SIZE

    # 3️⃣ **지렁이 이동**
    if dx != 0 or dy != 0:
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)
        snake.insert(0, new_head)
        snake.pop()

    # 2️⃣ **지렁이 그리기**
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], TILE_SIZE, TILE_SIZE))

    # 4️⃣ **먹이 그리기**
    pygame.draw.rect(screen, RED, (food_x, food_y, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()
    clock.tick(10)

# 게임 종료
pygame.quit()

