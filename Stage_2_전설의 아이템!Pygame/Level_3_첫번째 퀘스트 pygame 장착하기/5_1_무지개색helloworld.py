import pygame  # pygame 모듈을 임포트합니다.
import sys  # 외장 모듈을 임포트합니다.
from pygame.locals import *  # QUIT 등의 pygame 상수들을 불러옵니다.

pygame.init()  # Pygame을 초기화합니다.

WIDTH = 600  # 화면의 가로 크기를 설정합니다.
HEIGHT = 400  # 화면의 세로 크기를 설정합니다.
WHITE = (255, 255, 255)  # 흰색을 RGB 값으로 정의합니다.

# 무지개 색상 정의 (문자별로 색을 반복 적용합니다)
RAINBOW_COLORS = [
    (255, 0, 0),    # 빨강
    (255, 127, 0),  # 주황
    (255, 255, 0),  # 노랑
    (0, 255, 0),    # 초록
    (0, 0, 255),    # 파랑
    (75, 0, 130),   # 남색
    (148, 0, 211)   # 보라
]

FPS = 30  # 초당 프레임 수(FPS)를 설정합니다.

pygame.display.set_caption('Hello, world!')  # 창 제목을 설정합니다.
canvas = pygame.display.set_mode((WIDTH, HEIGHT))  # 메인 디스플레이를 설정합니다.
clock = pygame.time.Clock()  # 초당 프레임 설정에 사용할 시계를 생성합니다.

guilimFont = pygame.font.SysFont('굴림', 70)  # 폰트를 설정합니다.

# 텍스트 렌더링 및 위치 설정합니다.
texts = []  # 각 문자를 렌더링한 서피스를 저장할 리스트를 선언합니다.
total_width = 0  # 텍스트의 전체 너비를 계산하기 위한 변수를 선언합니다.
message = "Hello, world!"  # 화면에 출력할 메시지를 정의합니다.

# 각 문자에 대해 색상을 할당하고 텍스트 서피스를 생성합니다.
for i, char in enumerate(message):
    color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]  # 무지개 색상을 순환적으로 적용합니다.
    text_surface = guilimFont.render(char, True, color)  # 문자 렌더링합니다.
    text_rect = text_surface.get_rect()  # 텍스트의 위치를 위한 Rect 객체를 생성합니다.
    total_width += text_rect.width  # 전체 텍스트의 너비를 누적합니다.
    texts.append((text_surface, text_rect))  # 서피스와 Rect를 튜플로 리스트에 저장합니다.

# 전체 텍스트의 너비를 기준으로 텍스트의 시작 위치를 조정합니다.
offset = (WIDTH - total_width) // 2  # 화면 가로 중앙을 기준으로 시작 지점을 계산합니다.

# 각 텍스트의 위치를 설정합니다.
for text_surface, text_rect in texts:
    text_rect.topleft = (offset, HEIGHT / 2 - text_rect.height / 2)  # 수직 중앙에 배치합니다.
    offset += text_rect.width  # 다음 텍스트의 위치를 조정합니다.

# 게임 루프를 시작합니다.
while True:
    for event in pygame.event.get():  # 발생한 이벤트를 순회합니다.
        if event.type == QUIT:  # 창을 닫는 이벤트가 발생하면
            pygame.quit()  # Pygame을 종료합니다.
            sys.exit()  # 프로그램을 종료합니다.

    canvas.fill(WHITE)  # 화면을 흰색으로 채웁니다.

    # 각 문자 서피스를 화면에 그립니다.
    for text_surface, text_rect in texts:
        canvas.blit(text_surface, text_rect)  # 텍스트를 화면에 그립니다.

    pygame.display.update()  # 화면을 업데이트합니다.
    clock.tick(FPS)  # 설정된 FPS로 루프를 제어합니다.
