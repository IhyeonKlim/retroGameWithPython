import pygame
import random
import math
import sys
import os

# Pygame 초기화
pygame.init()

# 색상 정의 (RGB)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 화면 설정 (가로, 세로 크기 설정)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge Game")

# FPS 설정 (게임 속도 조절)
FPS = 60
clock = pygame.time.Clock()

# 폰트 설정 (게임 화면에 사용할 텍스트 스타일)
font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Arial", 60)

# 하이스코어 파일 경로 설정
HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.txt")

# 최고 점수 불러오기
# 텍스트 파일에서 최고 점수와 이름을 읽어옴
def load_high_scores():
    """텍스트 파일에서 최고 점수와 이름을 불러온다."""
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as f:
            scores = []
            for line in f:
                try:
                    name, score = line.strip().split(',')
                    scores.append((name, int(score)))
                except ValueError:
                    continue  # 잘못된 형식은 무시
            return sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    return []

# 최고 점수 저장하기
# 점수와 이름을 텍스트 파일에 저장

def save_high_scores(scores):
    """최고 점수와 이름들을 텍스트 파일에 저장한다."""
    with open(HIGHSCORE_FILE, 'w') as f:
        for name, score in scores:
            f.write(f"{name},{score}\n")
    return scores

# 새로운 점수를 기록하고 상위 5개의 점수를 유지
# 만약 새로운 점수가 기존 최고 점수보다 높으면 업데이트

def update_high_scores(name, score):
    """새로운 점수를 추가하고, 상위 5개 점수를 저장한다."""
    scores = load_high_scores()
    # 새로운 점수를 삽입하고 순위를 재정리
    scores.append((name, score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # 최고 점수 목록을 최대 5개로 유지
    if len(scores) > 5:
        scores = scores[:5]
    new_high_scores = save_high_scores(scores)
    return new_high_scores

# 최고 점수의 이름 목록 불러오기

def load_name_log():
    """목록 파일에서 모든 이름을 불러온다."""
    return [name for name, _ in load_high_scores()]

# 플레이어 클래스 정의
# 플레이어 캐릭터의 이동과 그리기를 담당

class Player:
    """플레이어 클래스"""
    def __init__(self):
        self.size = 20  # 플레이어 크기 설정
        self.speed = 4  # 플레이어 속도 설정
        # 플레이어 위치 초기화 (화면 중앙에서 시작)
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.size, self.size)

    def move(self, keys):
        # 키보드 입력에 따라 플레이어의 위치 이동
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        # 플레이어 그리기 (파란색 사각형)
        pygame.draw.rect(screen, BLUE, self.rect)

# 일반 총알 클래스 정의
# 플레이어를 향해 이동하며 충돌을 감지하는 역할

class Bullet:
    """일반 총알 클래스"""
    def __init__(self, player, bullets):
        # 총알을 화면 가장자리에서 생성
        self.x, self.y = self._spawn_on_border(bullets)
        self.radius = 3  # 총알 크기 설정
        self.speed = random.uniform(1, 2)  # 총알 속도 설정 (임의 속도)

        # 플레이어를 목표로 각도 계산
        self.target_x = player.rect.centerx
        self.target_y = player.rect.centery
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

    def _spawn_on_border(self, bullets):
        """기존 총알과 최소 거리가 필요한 위치에 총알 생성"""
        while True:
            side = random.choice(['left', 'right', 'top', 'bottom'])
            if side == 'left':
                x, y = 0, random.randint(0, SCREEN_HEIGHT)
            elif side == 'right':
                x, y = SCREEN_WIDTH - 1, random.randint(0, SCREEN_HEIGHT)
            elif side == 'top':
                x, y = random.randint(0, SCREEN_WIDTH), 0
            else:
                x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT - 1

            # 기존 총알과 최소 거리(30픽셀)를 확보한 위치에서 생성
            if all(math.hypot(b.x - x, b.y - y) > 30 for b in bullets):
                return x, y

    def move(self):
        # 각도에 따라 총알 이동
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        # 총알 그리기 (노란색 원)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def is_on_border(self):
        # 총알이 화면 밖으로 나갔는지 확인
        return self.x <= 0 or self.x >= SCREEN_WIDTH - 1 or self.y <= 0 or self.y >= SCREEN_HEIGHT - 1

    def check_collision(self, player):
        # 총알과 플레이어 사이의 충돌 여부 확인
        return check_collision_with_player(self, player)

# 특별 총알 (Comet) 클래스 정의
# 일반 총알보다 크고 빠른 속도로 이동

class Comet(Bullet):
    """특별 총알 (Comet) 클래스"""
    def __init__(self, player, bullets):
        super().__init__(player, bullets)
        self.radius = 6  # 일반 총알보다 큰 반지름
        self.speed *= 1.5  # 일반 총알보다 빠른 속도

    def draw(self):
        # 특별 총알 그리기 (빨간색 원)
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# 게임 클래스 정의
# 게임의 전체적인 흐름을 제어

class Game:
    """게임 클래스"""
    def __init__(self):
        self.high_scores = load_high_scores()  # 기존 하이스코어 로드
        self.reset_game()  # 게임 초기화
        self.current_state = "intro"  # 게임의 상태 (intro, playing, game_over, name_input)
        self.high_score_achieved = False  # 새로운 하이스코어 달성 여부
        self.high_score_saved = False  # 하이스코어 저장 여부

    def reset_game(self, immediate_start=False):
        # 게임 초기화 (플레이어와 총알 생성, 초기 점수 설정 등)
        self.player = Player()
        self.bullets = [Bullet(self.player, []) for _ in range(60)]  # 초기 총알 생성
        self.score = 0  # 점수 초기화
        self.game_started = immediate_start
        self.game_over = False
        self.name_input_active = False
        self.high_score_achieved = False
        self.high_score_saved = False
        # 게임 상태 설정 (즉시 시작 여부에 따라)
        self.current_state = "intro" if not immediate_start else "playing"

    def run(self):
        # 메인 게임 루프 (게임을 실행하는 동안 지속)
        running = True
        while running:
            screen.fill(BLACK)  # 화면 배경을 검정색으로 채우기

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 창 닫기 버튼 클릭 시 게임 종료
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.current_state == "intro" and event.key == pygame.K_RETURN:
                        # Enter 키 입력 시 게임 시작
                        self.current_state = "playing"
                    elif self.current_state == "game_over" and event.key == pygame.K_r:
                        # R 키 입력 시 게임 재시작
                        self.reset_game(immediate_start=True)

            # 현재 상태에 따라 화면 업데이트
            if self.current_state == "intro":
                self.wait_screen()
            elif self.current_state == "playing":
                self.play_game()
            elif self.current_state == "game_over":
                self.display_game_over_screen()
            elif self.current_state == "name_input" and self.high_score_achieved and not self.high_score_saved:
                self.high_score_input()

            # 화면 갱신
            pygame.display.flip()
            clock.tick(FPS)

    def wait_screen(self):
        """멈춘 화면 - 게임 시작 전 또는 재시작 대기 상태"""
        self.display_start_message()  # 게임 시작 메시지 표시
        self.display_name_log()  # 저장된 하이스코어 목록 표시

    def play_game(self):
        """게임 실행 화면"""
        keys = pygame.key.get_pressed()
        self.player.move(keys)  # 플레이어 이동

        for bullet in self.bullets:
            bullet.move()  # 총알 이동
            bullet.draw()  # 총알 그리기

            if bullet.check_collision(self.player):
                # 플레이어와 총알 충돌 시 게임 종료
                self.end_game()

            if bullet.is_on_border():
                # 총알이 화면 밖으로 나갔을 때 새로 생성
                self.bullets.remove(bullet)
                self.bullets.append(Bullet(self.player, self.bullets))

        self.player.draw()  # 플레이어 그리기
        # self.draw_border()  # 화면 경계선 그리기 (주석 처리됨)

        # 점수 증가 및 화면에 표시
        self.score += 1
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 현재 총알 수 화면에 표시
        bullet_count_text = font.render(f"Bullets: {len(self.bullets)}", True, WHITE)
        screen.blit(bullet_count_text, (SCREEN_WIDTH // 2 - bullet_count_text.get_width() // 2, 10))

        self.spawn_comet()  # 특정 조건에서 특별 총알 생성

    def display_game_over_screen(self):
        """게임 오버 화면"""
        if len(self.high_scores) > 0:
            # 하이스코어와 비교하여 새로운 기록인지 확인
            for i, (_, high_score) in enumerate(self.high_scores):
                if self.score > high_score and not self.high_score_saved:
                    self.high_score_achieved = True
                    self.current_state = "name_input"
                else:
                    self.display_game_over()  # 게임 오버 메시지 표시
                    self.display_name_log()  # 하이스코어 목록 표시
        else:
            self.high_score_achieved = True
            self.current_state = "name_input"

    def high_score_input(self):
        """새로운 최고 점수일 때 이름을 입력받는 화면"""
        name = ""
        while self.current_state == "name_input":
            screen.fill(BLACK)

            # 이름 입력 메시지 표시
            prompt = font.render(f"New High Score! Enter your name: {name}", True, WHITE)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2))

            pygame.display.flip()

            # 키 입력 확인
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Enter 키가 눌린 경우 이름 저장 및 종료
                        if name.strip():  # 공백이 아닌 경우에만 저장
                            new_high_score = update_high_scores(name, self.score)
                            self.high_scores = new_high_score
                            self.high_score_saved = True
                            self.current_state = "game_over"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]  # 백스페이스 키로 이름 삭제
                    else:
                        if len(name) < 10:  # 이름의 최대 길이를 제한
                            name += event.unicode

    def spawn_comet(self):
        """특별 총알 생성"""
        if self.score > 0 and self.score % 100 == 0:
            self.bullets.append(Comet(self.player, self.bullets))

    def end_game(self):
        # 게임 종료 시 상태를 게임 오버로 전환
        self.current_state = "game_over"

    # def draw_border(self):
    #     # 화면 경계선 그리기 (주석 처리됨)
    #     pygame.draw.rect(screen, RED, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)

    def display_start_message(self):
        # 게임 시작 메시지 표시
        start_text = font.render("Press Enter to Start", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

    def display_game_over(self):
        # 게임 오버 메시지 표시
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    def display_name_log(self):
        """저장된 이름 목록을 화면에 표시한다."""
        x_offset = 50
        y_offset = 20
        title = font.render("Previous High Scores:", True, WHITE)
        screen.blit(title, (x_offset, y_offset))
        y_offset += 30
        for i, (name, score) in enumerate(self.high_scores):  # 최고 점수와 점수 표시
            name_text = font.render(f"{i + 1}. {name} - {score}", True, WHITE)
            screen.blit(name_text, (x_offset, y_offset))
            y_offset += 30

# 총알과 플레이어의 충돌 여부를 계산하는 함수

def check_collision_with_player(bullet, player):
    """총알과 플레이어 사이의 충돌 여부를 반환하는 함수."""
    distance = math.hypot(player.rect.centerx - bullet.x, player.rect.centery - bullet.y)
    return distance < bullet.radius + player.size / 2

# 게임 실행
if __name__ == "__main__":
    game = Game()
    game.run()
