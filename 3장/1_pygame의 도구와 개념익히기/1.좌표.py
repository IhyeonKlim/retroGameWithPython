import pygame
import sys
from pygame.locals import QUIT

# 초기 설정
WIDTH, HEIGHT = 800, 600  # 화면 크기
GRID_SIZE = 100  # 격자의 크기 (100 x 100 픽셀)
WHITE = (255, 255, 255)  # 흰색 RGB
BLACK = (0, 0, 0)  # 검은색 RGB
GRAY = (200, 200, 200)  # 회색 (격자 색상)
RED = (255, 0, 0)  # 빨간색 RGB

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 화면 설정
pygame.display.set_caption("Pygame 좌표평면 예제")  # 창 제목 설정
font = pygame.font.SysFont(None, 24)  # 폰트 설정

# 메인 루프
while True:
    for event in pygame.event.get():  # 이벤트 처리
        if event.type == QUIT:  # 창 닫기 이벤트 처리
            pygame.quit()
            sys.exit()

    # 화면 그리기
    screen.fill(WHITE)  # 화면을 흰색으로 채움

    # 모눈종이 격자 그리기
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))  # 세로선 그리기
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))  # 가로선 그리기

    # 좌표 표시
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            coord_text = font.render(f"({x},{y})", True, BLACK)  # 좌표 텍스트 생성
            screen.blit(coord_text, (x + 5, y + 5))  # 좌표를 약간 안쪽에 배치

    # (0, 0)과 (800, 600)에 빨간 점 그리기
    pygame.draw.circle(screen, RED, (0, 0), 10)  # (0, 0) 근처에 빨간 원 표시
    pygame.draw.circle(screen, RED, (800, 0), 10)  # (800, 0) 근처에 빨간 원 표시 WIDTH
    pygame.draw.circle(screen, RED, (0, 600), 10)  # (0, 600) 근처에 빨간 원 표시 HEIGHT
    pygame.draw.circle(screen, RED, (WIDTH, HEIGHT), 10)  # (800, 600) 근처에 빨간 원 표시

    pygame.display.update()  # 화면 갱신
