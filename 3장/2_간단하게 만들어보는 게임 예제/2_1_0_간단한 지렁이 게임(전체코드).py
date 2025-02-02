import pygame
import random

# 1️⃣ **게임 초기화**
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 500, 500
TILE_SIZE = 40  # 지렁이와 먹이 크기
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("지렁이 게임")

# 색상 설정
WHITE = (255, 255, 255)  # 배경색
GREEN = (0, 200, 0)  # 지렁이 머리 색상
LIGHT_GREEN = (150, 255, 150)  # 지렁이 몸통 색상
RED = (255, 0, 0)  # 먹이 색상

# 게임 속도 조절을 위한 시계
clock = pygame.time.Clock()

# 2️⃣ **지렁이 생성**
snake = [(240, 240)]  # 지렁이 시작 위치
snake_dx, snake_dy = 0, 0  # 초기 이동 방향 (정지 상태)

# 4️⃣ **먹이 생성 (랜덤 위치)**
def spawn_food():
    return (random.randint(0, (WIDTH // TILE_SIZE) - 1) * TILE_SIZE,
            random.randint(0, (HEIGHT // TILE_SIZE) - 1) * TILE_SIZE)

food_x, food_y = spawn_food()

# 5️⃣ **충돌 처리 함수**
def check_collision(new_head):
    # 벽에 닿았거나 자기 몸과 부딪혔을 경우
    if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        return True
    return False

# 6️⃣ **먹이를 먹었을 때 처리**
def check_food_eaten(new_head):
    global food_x, food_y
    if new_head == (food_x, food_y):  # 먹이 위치와 일치하면
        food_x, food_y = spawn_food()  # 새로운 먹이 생성
        return True
    return False

# 게임 루프 실행 여부
running = True

# 🎮 **게임 루프 시작**
while running:
    screen.fill(WHITE)  # 화면 초기화

    # 3️⃣ **키 입력을 통한 지렁이 컨트롤**
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창 닫기 버튼 클릭 시 게임 종료
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_dx == 0:
                snake_dx, snake_dy = -TILE_SIZE, 0
            elif event.key == pygame.K_RIGHT and snake_dx == 0:
                snake_dx, snake_dy = TILE_SIZE, 0
            elif event.key == pygame.K_UP and snake_dy == 0:
                snake_dx, snake_dy = 0, -TILE_SIZE
            elif event.key == pygame.K_DOWN and snake_dy == 0:
                snake_dx, snake_dy = 0, TILE_SIZE

    # 5️⃣ **지렁이 이동 및 충돌 검사**
    if snake_dx or snake_dy:
        head_x, head_y = snake[0]  # 현재 머리 위치
        new_head = (head_x + snake_dx, head_y + snake_dy)  # 새로운 머리 위치

        if check_collision(new_head):  # 충돌 검사
            print("game over")
            running = False  # 게임 종료

        snake.insert(0, new_head)  # 머리를 리스트 맨 앞에 추가

        # 6️⃣ **먹이를 먹었을 때 길이 증가**
        if not check_food_eaten(new_head):
            snake.pop()  # 안 먹었으면 꼬리를 삭제 (길이 유지)

    # 🐍 **지렁이 그리기**
    for i, part in enumerate(snake):
        color = GREEN if i == 0 else LIGHT_GREEN  # 머리는 초록색, 몸통은 연두색
        pygame.draw.rect(screen, color, (*part, TILE_SIZE, TILE_SIZE))

    # 🍎 **먹이 그리기**
    pygame.draw.rect(screen, RED, (food_x, food_y, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()  # 화면 업데이트
    clock.tick(10)  # 게임 속도 조절

# 게임 종료
pygame.quit()
