import pygame  # pygame 모듈을 임포트합니다.
import sys  # 시스템 종료를 위한 sys 모듈을 임포트합니다.
from pygame.locals import QUIT  # pygame의 QUIT 상수를 임포트합니다.
import time  # 시간 측정을 위한 time 모듈을 임포트합니다.

# 초기 설정
WIDTH, HEIGHT = 600, 400  # 화면 크기
WHITE = (255, 255, 255)  # 흰색 RGB
BLACK = (0, 0, 0)  # 검은색 RGB

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 화면 설정
pygame.display.set_caption('FPS & Time Demo')  # 창 제목 설정
clock = pygame.time.Clock()  # FPS 제어를 위한 Clock 객체 생성

# 폰트 설정 및 텍스트 준비
font = pygame.font.SysFont(None, 60)  # 기본 폰트 사용
info_font = pygame.font.SysFont(None, 30)  # 정보 표시용 작은 폰트

text = font.render("HELLO PYGAME", True, BLACK)  # 검은색 텍스트 생성
text_rect = text.get_rect()  # 텍스트 위치 정보 가져오기
text_rect.topleft = (0, HEIGHT // 2 - text_rect.height // 2)  # 시작 위치 설정

FPS = 5  # 초기 FPS 설정
speed = 5  # 텍스트 이동 속도
start_time = time.time()  # 프로그램 시작 시간 기록

# 메인 루프
while True:
    for event in pygame.event.get():  # 이벤트 처리
        if event.type == QUIT:  # 창 닫기 이벤트가 발생하면
            pygame.quit()  # pygame을 종료합니다.
            sys.exit()  # 프로그램을 종료합니다.

    # 1초마다 FPS 증가
    elapsed_time = int(time.time() - start_time)  # 경과 시간 계산
    FPS = min(5 + elapsed_time * 5, 60)  # FPS는 5씩 증가하며 최대 60까지

    # 텍스트 위치 업데이트 (오른쪽으로 이동)
    text_rect.x += speed
    if text_rect.left > WIDTH:  # 텍스트가 오른쪽 끝을 넘어가면 다시 왼쪽으로 이동
        text_rect.right = 0

    # 화면 그리기
    screen.fill(WHITE)  # 화면을 흰색으로 채웁니다.
    screen.blit(text, text_rect)  # 텍스트를 화면에 그립니다.

    # 경과 시간 및 FPS 정보 표시
    elapsed_text = info_font.render(f"Time: {elapsed_time}s", True, BLACK)
    fps_text = info_font.render(f"FPS: {FPS}", True, BLACK)
    screen.blit(elapsed_text, (10, 10))  # 화면 왼쪽 상단에 경과 시간 표시
    screen.blit(fps_text, (10, 40))  # 화면 왼쪽 상단에 FPS 표시

    pygame.display.update()  # 화면을 갱신합니다.

    # FPS 제어
    clock.tick(FPS)  # 현재 FPS에 맞춰 루프를 제어합니다.