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

# 게임 루프 실행 여부
running = True

# 게임 루프 (게임이 실행되는 동안 계속 반복됨)
while running:
    screen.fill(WHITE)  # 화면을 흰색으로 채워서 이전 프레임을 지움

    # 2️⃣ **지렁이 그리기**
    for part in snake:  # 지렁이의 각 부분을 그리기 (현재는 머리만 있음)
        pygame.draw.rect(screen, GREEN, (part[0], part[1], TILE_SIZE, TILE_SIZE))

    # 이벤트 처리 (사용자의 입력을 감지)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 사용자가 창을 닫으면
            running = False  # 루프 종료

    pygame.display.flip()  # 화면을 업데이트하여 변경 사항을 적용

# 게임 종료
pygame.quit()  # pygame을 종료하여 리소스를 정리합니다.

