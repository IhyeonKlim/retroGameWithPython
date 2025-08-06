import pygame  # pygame 모듈 임포트
import sys  # 외장 모듈
from pygame.locals import *  # QUIT 등의 pygame 상수를 로드

pygame.init()  # 초기화

WIDTH = 600  # 화면의 가로 크기 설정
HEIGHT = 400  # 화면의 세로 크기 설정
WHITE = (255, 255, 255)  # 흰색 RGB
BLACK = (0, 0, 0)  # 검정색 RGB
FPS = 30  # 초당 프레임 수 설정 (Frame Per Second)

pygame.display.set_caption('Hello, world!')  # 창 제목 설정
canvas = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)  # 메인 디스플레이 설정
clock = pygame.time.Clock()  # 시간 설정 (추후 FPS 관련 설명 예정)

guilim_font = pygame.font.SysFont('굴림', 70)  # 서체 설정
hello_world_text = guilim_font.render('Hello, world!', 1, BLACK)
# .render() 함수에 내용, 안티앨리어싱(1), 색을 전달하여 텍스트 이미지 생성
text_rect = hello_world_text.get_rect()  # 생성된 텍스트의 rect 객체를 가져옴
text_rect.center = (WIDTH / 2, HEIGHT / 2)  # rect 중앙을 화면 중앙에 맞춤

# 게임이 종료되기 전까지 반복해서 동작하도록 설정
# while문을 사용하며, True 조건 대신 변수를 이용해 제어 가능
while True:  # 아래 코드를 무한 반복
    for event in pygame.event.get():  # 발생한 입력 event를 하나씩 검사
        if event.type == QUIT:  # event type이 QUIT일 경우
            pygame.quit()  # pygame을 종료
            sys.exit()  # 창을 닫음

    # 메인 디스플레이를 제어
    canvas.fill(WHITE)  # canvas를 흰색으로 채움
    canvas.blit(hello_world_text, text_rect)
    # canvas의 text_rect 위치에 hello_world_text 텍스트를 그림

    pygame.display.update()  # 화면 업데이트
    # FPS 설정은 추후 더 자세히 설명할 예정
    clock.tick(FPS)  # 설정된 FPS에 따라 루프 간격을 둠
