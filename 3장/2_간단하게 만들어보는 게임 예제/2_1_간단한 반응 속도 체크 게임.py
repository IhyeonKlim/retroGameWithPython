import pygame
import random
import time

# Pygame 초기화
pygame.init()

# 화면 설정 (600x800 해상도)
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reaction Time Game")

# 색상 정의
BLACK = (0, 0, 0)  # 배경색 (검정)
RED = (255, 0, 0)  # 준비 상태의 원 색상 (빨강)
YELLOW = (255, 255, 0)  # 클릭 전 반응 상태 원 색상 (노랑)
BLUE = (0, 0, 255)  # 클릭 후 원 색상 (파랑)
WHITE = (255, 255, 255)  # 텍스트 색상

# 폰트 설정
font = pygame.font.SysFont(None, 50)  # 안내 텍스트용 폰트, 크기 50
large_font = pygame.font.SysFont(None, 80)  # "Stop", "Go!", "Wrong!" 텍스트용 큰 폰트

# 원 위치와 속성 설정
circle_x, circle_y = WIDTH // 2, HEIGHT // 2  # 화면 중앙에 위치 고정
circle_radius = 50  # 원의 반지름
circle_color = RED  # 초기 원 색상 (빨강)

# 반응 시간과 상태 변수 초기화
reaction_time = None  # 반응 시간 저장 변수
show_reaction_time = False  # 반응 시간 표시 여부
ready_to_click = False  # 클릭 가능 여부
show_wrong_message = False  # 잘못 클릭 메시지 표시 여부

# 랜덤한 시간 후 노란색으로 변경
change_time = time.time() + random.uniform(1, 3)  # 1~3초 내에 색상 변경 예정

# 메인 루프
running = True
while running:
    for event in pygame.event.get():  # 이벤트 처리
        if event.type == pygame.QUIT:  # 창 닫기 이벤트
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트
            if ready_to_click and not show_reaction_time:  # 노란색일 때 클릭하면 반응 시간 기록
                reaction_time = time.time() - change_time
                circle_color = BLUE  # 클릭 후 파란색으로 변경
                show_reaction_time = True  # 반응 시간 표시 플래그 설정
                reaction_display_start = time.time()  # 반응 시간 표시 시작 시간 기록
            elif not ready_to_click:  # 노란색이 아니었을 때 클릭하면 "Wrong!" 표시
                show_wrong_message = True
                wrong_display_start = time.time()  # 잘못 클릭 메시지 표시 시작 시간 기록

    # 랜덤 시간 후 노란색으로 변경
    if not ready_to_click and time.time() >= change_time:
        circle_color = YELLOW  # 원 색상을 노란색으로 변경
        ready_to_click = True  # 클릭 가능 상태로 변경

    # 화면 그리기
    screen.fill(BLACK)  # 배경색 설정

    # 고정된 안내 문구
    tap_text = font.render("Tap the Yellow Circle!", True, WHITE)
    screen.blit(tap_text, (WIDTH // 2 - tap_text.get_width() // 2, 50))  # 화면 상단에 표시

    # 상태에 따른 "Stop" 또는 "Go!" 문구
    if not show_wrong_message and not show_reaction_time:
        if circle_color == RED:
            state_text = large_font.render("Stop", True, WHITE)
        elif circle_color == YELLOW:
            state_text = large_font.render("Go!", True, WHITE)
        screen.blit(state_text, (WIDTH // 2 - state_text.get_width() // 2, circle_y - circle_radius - 60))  # 원 위쪽에 표시

    # 원 그리기
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # 반응 속도 표시
    if show_reaction_time:  # 반응 시간 표시
        reaction_text = font.render(f"Your reaction time = {reaction_time:.2f} seconds", True, WHITE)
        screen.blit(reaction_text, (WIDTH // 2 - reaction_text.get_width() // 2, circle_y + circle_radius + 50))  # 원 아래쪽에 표시

        # 반응 시간 표시 후 2초 경과 시 게임 초기화
        if time.time() - reaction_display_start > 2:
            # 게임 상태 초기화
            circle_color = RED  # 원 색상을 빨간색으로 초기화
            ready_to_click = False  # 클릭 불가 상태로 초기화
            show_reaction_time = False  # 반응 시간 표시 플래그 초기화
            change_time = time.time() + random.uniform(1, 3)  # 다음 노란색 전환 시간 설정

    # 잘못 클릭했을 때 "Wrong!" 메시지 표시
    if show_wrong_message:
        wrong_text = large_font.render("Wrong!", True, WHITE)
        screen.blit(wrong_text, (WIDTH // 2 - wrong_text.get_width() // 2, circle_y - circle_radius - 60))  # 원 위쪽에 표시

        # "Wrong!" 메시지를 2초 동안 표시한 후 게임 초기화
        if time.time() - wrong_display_start > 2:
            circle_color = RED  # 원 색상을 빨간색으로 초기화
            ready_to_click = False  # 클릭 가능 상태 초기화
            show_wrong_message = False  # "Wrong!" 메시지 표시 플래그 초기화
            change_time = time.time() + random.uniform(1, 3)  # 다음 노란색 전환 시간 설정

    pygame.display.flip()  # 화면 업데이트

# Pygame 종료
pygame.quit()
