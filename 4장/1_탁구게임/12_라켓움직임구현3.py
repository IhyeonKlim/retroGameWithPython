import sys
import pygame
from pygame import QUIT, KEYDOWN, Rect

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
RED = (255, 0, 0)  # 빨간색 (꼭지점 및 라켓 표시용)

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

# 꼭지점 좌표 계산
top_left = (play_area_x, play_area_y)
top_right = (play_area_x + play_area_width, play_area_y)
bottom_left = (play_area_x, play_area_y + play_area_height)
bottom_right = (play_area_x + play_area_width, play_area_y + play_area_height)

#keyboard를 계속 입력받도록 하는 코드
pygame.key.set_repeat(5, 5)


print("Top Left:", top_left)
print("Top Right:", top_right)
print("Bottom Left:", bottom_left)
print("Bottom Right:", bottom_right)

def draw_center_dashed_line(surface, color, start_x, start_y, height, dash_height, gap_height, line_width):
    """ 중앙에 수직 점선을 쉽게 그리는 함수 """
    for y in range(start_y, start_y + height, dash_height + gap_height):
        pygame.draw.line(surface, color, (start_x, y), (start_x, y + dash_height), line_width)

# 플레이어(라켓)
class Player:
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 10, 60)  # 라켓의 크기와 위치
        self.rect.centerx = x
        self.rect.centery = y
        self.top = self.rect.top  # 초기 top 값 설정
        self.bottom = self.rect.bottom  # 초기 bottom 값 설정
        self.print_position()

    def update_position(self):
        """현재 rect의 top과 bottom 값을 업데이트"""
        self.top = self.rect.top
        self.bottom = self.rect.bottom

    def print_position(self):
        self.update_position()  # 위치 값 업데이트
        print(f"Player Position - Top: {self.top}, Bottom: {self.bottom}, Centery: {self.rect.centery}")

    def move_up(self):
        self.rect.centery -= 5  # Y축 중심 위로 이동
        self.update_position()  # 이동 후 위치 업데이트
        self.print_position()

    def move_down(self):
        self.rect.centery += 5  # Y축 중심 아래로 이동
        self.update_position()  # 이동 후 위치 업데이트
        self.print_position()

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
            elif event.key == pygame.K_w:
                if player1.top > play_area_y:
                    player1.move_up()
            elif event.key == pygame.K_s:
                if player1.bottom < play_area_y + play_area_height :
                    player1.move_down()
            elif event.key == pygame.K_UP:
                if player2.top > play_area_y:
                    player2.move_up()
            elif event.key == pygame.K_DOWN:
                if player2.bottom < play_area_y + play_area_height :
                    player2.move_down()

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

    # 각 꼭지점에 빨간색 점 찍기
    pygame.draw.circle(screen, RED, top_left, 5)
    pygame.draw.circle(screen, RED, top_right, 5)
    pygame.draw.circle(screen, RED, bottom_left, 5)
    pygame.draw.circle(screen, RED, bottom_right, 5)

    # 플레이어 1의 top, bottom, centery 위치에 빨간색 점 표시
    pygame.draw.circle(screen, RED, (player1.rect.centerx, player1.rect.top), 5)
    pygame.draw.circle(screen, RED, (player1.rect.centerx, player1.rect.bottom), 5)
    pygame.draw.circle(screen, RED, (player1.rect.centerx, player1.rect.centery), 5)

    pygame.display.update()
    clock.tick(fps_value)

pygame.quit()
sys.exit()
