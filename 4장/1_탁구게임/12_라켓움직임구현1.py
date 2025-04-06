import sys
import pygame
from pygame import QUIT, KEYDOWN, K_LEFT, K_RIGHT, KEYUP, Rect

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 타이틀 설정
pygame.display.set_caption("ping pong game")

# 색상 정의
BLACK = (0, 0, 0)  # 배경색 (검정)
WHITE = (255, 255, 255)  # 테두리 및 점선 (하얀색)

# FPS 설정
fps_value = 60
clock = pygame.time.Clock()

# 테두리 및 여백 설정
border_thickness = 10  # 테두리 두께
horizontal_padding = 60  # 좌우 패딩
vertical_padding = 40  # 위아래 패딩

# 플레이 구역 설정
play_area_x = border_thickness + horizontal_padding  # 구역의 X 좌표 시작점
play_area_y = border_thickness + vertical_padding  # 구역의 Y 좌표 시작점
play_area_width = screen_width - 2 * (border_thickness + horizontal_padding)  # 구역의 너비
play_area_height = screen_height - 2 * (border_thickness + vertical_padding)  # 구역의 높이

# 점선 설정
dashed_line_width = 10  # 점선의 두께
dash_height = 20  # 점선의 한 개 길이
gap_between_dashes = 20  # 점선 사이의 간격

def draw_center_dashed_line(surface, color, start_x, start_y, height, dash_height, gap_height, line_width):
    """ 중앙에 수직 점선을 쉽게 그리는 함수 """
    for y in range(start_y, start_y + height, dash_height + gap_height):
        pygame.draw.line(surface, color, (start_x, y), (start_x, y + dash_height), line_width)

# 플레이어(라켓)
class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 60)  # 라켓 크기 설정 (폭 10, 높이 60)
        self.rect.centerx = x  # X 좌표 설정
        self.rect.centery = y  # Y 좌표 설정
    def move_up(self): # 위로가기
        self.rect.centery -= 5 #최초 설정된 중아값에서 5씩 빼주기
        return True

    def move_down(self): # 아래로가기
        self.rect.centery += 5 #아래로 움직이는 것은 위와 반대.
        return True

# 플레이어 1 (왼쪽)
# 라켓의 Y 위치를 play_area의 중앙에 맞춤
player1 = Player(play_area_x + 20, play_area_y + play_area_height // 2)

# 플레이어 2 (오른쪽)
# 라켓의 X 위치를 play_area의 가로길이 만큼 이동
# 라켓의 Y 위치를 play_area의 중앙에 맞춤
player2 = Player(play_area_x + play_area_width - 20, play_area_y + play_area_height // 2)

# 공 클래스 정의
class Ball:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 50, 50)  # 공의 크기 설정 (0.0 위치에 가로 50, 세로 50)
        self.rect.centerx = x  # 사각형 중심의 X 좌표 설정
        self.rect.centery = y  # 사각형 중심의 Y 좌표 설정
# 공 객체 생성
ball = Ball(play_area_x + play_area_width // 2, play_area_y + play_area_height // 2)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #키보드의 자판을 누르는 이벤트가 발생할 때
        elif event.type == KEYDOWN:
            # ESC 키를 누르면 게임이 종료
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 화살표 위를 누르면 위로 올라가는 메서드를 호출
            elif event.key == pygame.K_UP:
                player1.move_up() #player1 class의 instance인 move_up()메서드
            # 화살표 아래를 누르면 아래로 내려가는 메서드를 호출
            elif event.key == pygame.K_DOWN:
                player1.move_down()
    # 화면을 검정색으로 채움 (전체 배경)
    screen.fill(BLACK)

    # 플레이 구역 바깥에 테두리 그리기 (테두리가 안쪽으로 침범되지 않도록)
    outer_rect_x = play_area_x - border_thickness
    outer_rect_y = play_area_y - border_thickness
    outer_rect_width = play_area_width + 2 * border_thickness
    outer_rect_height = play_area_height + 2 * border_thickness
    pygame.draw.rect(screen, WHITE, (outer_rect_x, outer_rect_y, outer_rect_width, outer_rect_height), border_thickness)

    # 중앙에 점선을 그림
    mid_x = play_area_x + play_area_width // 2  # 중앙선 X 좌표 계산
    draw_center_dashed_line(screen, WHITE, mid_x, play_area_y, play_area_height, dash_height, gap_between_dashes, dashed_line_width)

    # 플레이어1 라켓 그리기
    pygame.draw.rect(screen, WHITE, player1.rect)
    # 플레이어2 라켓 그리기
    pygame.draw.rect(screen, WHITE, player2.rect)
    # 공 그리기
    pygame.draw.rect(screen, WHITE, ball.rect)
    # 화면 업데이트
    pygame.display.update()

    # 초당 프레임 설정
    clock.tick(fps_value)

# Pygame 종료
pygame.quit()
sys.exit()
