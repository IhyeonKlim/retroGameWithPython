import pygame  # pygame 모듈 임포트
import sys  # 시스템 종료용 모듈 임포트
from pygame.locals import QUIT  # pygame의 QUIT 상수 임포트

# 화면 설정 상수
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)  # 배경색 (흰색)
FPS = 30  # 초당 프레임 수

# 무지개 색상 정의 (문자별로 순환)
RAINBOW_COLORS = [
    (255, 0, 0),    # 빨강
    (255, 127, 0),  # 주황
    (255, 255, 0),  # 노랑
    (0, 255, 0),    # 초록
    (0, 0, 255),    # 파랑
    (75, 0, 130),   # 남색
    (148, 0, 211)   # 보라
]

# Pygame 초기화
pygame.init()
pygame.display.set_caption('Hello, world!')  # 창의 제목 설정
canvas = pygame.display.set_mode((WIDTH, HEIGHT))  # 메인 디스플레이 설정
clock = pygame.time.Clock()  # FPS 설정을 위한 Clock 객체

# 폰트 및 텍스트 설정
font = pygame.font.SysFont('굴림', 70)
message = "Hello, world!"
texts = []  # 문자별 서피스 및 위치 정보 저장
total_width = 0  # 전체 너비 계산용 변수

# 텍스트 서피스 생성 및 위치 설정
for i, char in enumerate(message):
    color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]  # 순환 색상 적용
    text_surface = font.render(char, True, color)  # 문자 렌더링
    text_rect = text_surface.get_rect()
    total_width += text_rect.width  # 전체 너비 누적
    texts.append((text_surface, text_rect))

# 시작 위치 중앙 정렬
offset = (WIDTH - total_width) // 2
for _, text_rect in texts:
    text_rect.topleft = (offset, HEIGHT / 2 - text_rect.height / 2)
    offset += text_rect.width

# 색상 인덱스 초기화
color_index = 0

# 메인 루프
while True:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 화면 갱신
    canvas.fill(WHITE)
    for i, (text_surface, text_rect) in enumerate(texts):
        color = RAINBOW_COLORS[(color_index + i) % len(RAINBOW_COLORS)]
        text_surface = font.render(message[i], True, color)  # 문자 렌더링
        canvas.blit(text_surface, text_rect)

    pygame.display.update()
    clock.tick(FPS)

    # 색상 인덱스 순환
    color_index = (color_index + 1) % len(RAINBOW_COLORS)
