import pygame  # Pygame 라이브러리를 불러옵니다.

# 1️⃣ **게임 초기화**
pygame.init()  # Pygame을 초기화하여 게임을 실행할 준비를 합니다.

# 화면 설정
WIDTH = 500  # 게임 창의 너비를 500 픽셀로 설정합니다.
HEIGHT = 500  # 게임 창의 높이를 500 픽셀로 설정합니다.
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 설정한 크기로 게임 창을 생성합니다.
pygame.display.set_caption("지렁이 게임")  # 창의 제목을 "지렁이 게임"으로 지정합니다.

# 색상 설정
WHITE = (255, 255, 255)  # 화면 배경색으로 사용할 흰색 (RGB 값)을 정의합니다.

# 게임 루프 실행 여부
running = True  # 게임이 실행되는 동안 반복문을 유지하기 위해 `running` 변수를 `True`로 설정합니다.

# 게임 루프 (게임이 실행되는 동안 계속 반복됨)
while running:
    screen.fill(WHITE)  # 화면을 흰색으로 채워서 이전 프레임을 지웁니다.

    # 이벤트 처리 (사용자의 입력을 감지)
    for event in pygame.event.get():  # pygame의 이벤트 목록을 가져와 하나씩 확인합니다.
        if event.type == pygame.QUIT:  # 사용자가 창을 닫으려고 하면
            running = False  # `running`을 `False`로 변경하여 루프를 종료합니다.

    pygame.display.flip()  # 화면을 업데이트하여 변경 사항을 적용합니다.

# 게임 종료
pygame.quit()  # 게임을 종료하고 pygame에서 사용한 리소스를 정리합니다.

