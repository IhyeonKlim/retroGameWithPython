import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("벽돌 부수기 게임")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
YELLOW = (255, 255, 0)
FONT_COLOR = WHITE

# 폰트 설정
font = pygame.font.Font(None, 36)

# 프레임 설정
FPS = 60


class Paddle:
    """ 플래이어(패들)를 정의하는 클래스 """

    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = (SCREEN_WIDTH - self.width) / 2
        self.y = SCREEN_HEIGHT - 40
        self.speed = 7
        self.original_width = self.width
        self.extended_end_time = 0  # 패들 확장 종료 시간

    def move(self, keys):
        """ 키 입력을 받아 패들 이동 """
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def extend(self, duration, current_time):
        """ 패들 크기 증가 효과 적용 """
        self.width = self.original_width * 1.5
        self.extended_end_time = current_time + duration

    def update(self, current_time):
        """ 패들 확장 효과가 끝나면 원래 크기로 복귀 """
        if current_time > self.extended_end_time:
            self.width = self.original_width

    def draw(self):
        """ 패들을 화면에 그림 """
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))


class Ball:
    """ 공을 정의하는 클래스 """

    def __init__(self):
        self.radius = 10
        self.speed_x = 4
        self.speed_y = -4
        self.reset_position()

    def reset_position(self):
        """ 공을 패들 위에 위치시키고 초기 속도를 부여 """
        self.x = paddle.x + paddle.width / 2
        self.y = paddle.y - self.radius - 1
        self.speed_x = 4
        self.speed_y = -4

    def move(self):
        """ 공의 위치 업데이트 """
        self.x += self.speed_x
        self.y += self.speed_y

    def check_wall_collision(self):
        """ 벽과의 충돌 처리 """
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y

    def draw(self):
        """ 공을 화면에 그림 """
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

class Block:
    """ 블록을 정의하는 클래스 """

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        """ 블록을 화면에 그림 """
        pygame.draw.rect(screen, RED, self.rect)


class Item:
    """ 아이템을 정의하는 클래스 """

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 2
        self.effect = random.choice(["speed_up", "slow_down"])

    def move(self):
        """ 아이템을 아래로 이동 """
        self.rect.y += self.speed

    def draw(self):
        """ 무지개 색상 적용하여 아이템 그리기 """
        color_offset = (pygame.time.get_ticks() // 5) % 255
        rainbow_color = (color_offset, (color_offset + 85) % 255, (color_offset + 170) % 255)
        pygame.draw.rect(screen, rainbow_color, self.rect)


class Game:
    """ 게임 전체를 관리하는 클래스 """

    def __init__(self):
        self.running = True
        self.score = 0
        self.lives = 3
        self.speed_multiplier = 1  # 속도 배율
        self.speed_effect_end_time = 0  # 아이템 속도 효과 종료 시간(ms)
        self.speed_effect_duration = 5000  # 아이템 속도 효과 지속 시간(ms)
        self.blocks = self.create_blocks()
        self.items = []
        self.clock = pygame.time.Clock()

    def create_blocks(self):
        """ 블록을 생성하여 리스트로 반환 """
        blocks = []
        rows, cols = 5, 10
        margin = 5
        block_width = (SCREEN_WIDTH - margin * (cols + 1)) / cols
        block_height = 30

        for row in range(rows):
            for col in range(cols):
                x = col * (block_width + margin) + margin
                y = row * (block_height + margin) + margin
                blocks.append(Block(x, y, block_width, block_height))  # ⬅ Block 인스턴스를 생성해서 리스트에 추가
        return blocks

    def handle_collisions(self):
        """ 공과 블록 및 패들 간 충돌 처리 """
        global paddle, ball

        # 블록 충돌 검사
        for block in self.blocks[:]:
            if block.rect.colliderect(
                    pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)):
                ball.speed_y = -ball.speed_y
                self.blocks.remove(block)
                self.score += 10

                # 아이템 생성 확률 적용
                if random.random() < 1:  # 100% 확률로 아이템 생성
                    self.items.append(Item(block.rect.centerx, block.rect.centery))
                break

        # 패들과의 충돌 검사
        paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
        if paddle_rect.colliderect(
                pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)):
            ball.speed_y = -ball.speed_y

        # 아이템 충돌 검사
        current_time = pygame.time.get_ticks()
        for item in self.items[:]:
            item.move()
            if paddle_rect.colliderect(item.rect):
                self.score += 50
                paddle.extend(5000, current_time)  # 5초간 패들 확장
                if item.effect == "speed_up":
                    self.speed_multiplier = 1.5
                elif item.effect == "slow_down":
                    self.speed_multiplier = 0.5

                self.speed_effect_end_time = current_time + self.speed_effect_duration  # 15초 후 속도 원상 복구
                self.items.remove(item)

            elif item.rect.y > SCREEN_HEIGHT:
                self.items.remove(item)

    def update_speed_effect(self):
        """ 속도 효과가 15초가 지나면 원래 속도로 복구 """
        current_time = pygame.time.get_ticks()
        if current_time > self.speed_effect_end_time:
            self.speed_multiplier = 1  # 원래 속도로 복귀

    def draw_status(self):
        """ 점수, 생명, 속도 상태를 화면에 표시 """
        score_text = font.render(f"Score: {self.score}", True, FONT_COLOR)
        lives_text = font.render(f"Lives: {self.lives}", True, FONT_COLOR)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 20))

        # 속도 효과 상태 표시 (속도가 1이 아닐 때만 표시)
        if self.speed_multiplier > 1:
            speed_text = font.render("Speed: FAST", True, FONT_COLOR)
            screen.blit(speed_text, (SCREEN_WIDTH // 2 - 60, 200))
        elif self.speed_multiplier < 1:
            speed_text = font.render("Speed: SLOW", True, FONT_COLOR)
            screen.blit(speed_text, (SCREEN_WIDTH // 2 - 60, 200))

    def run(self):
        """ 게임 루프 실행 """
        while self.running:
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            paddle.move(keys)
            paddle.update(current_time)
            ball.move()
            ball.check_wall_collision()

            # 공이 바닥에 닿았을 때 처리
            if ball.y + ball.radius >= SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    print("Game Over")
                    self.running = False
                else:
                    ball.reset_position()

            self.handle_collisions()
            self.update_speed_effect()  # ⬅ 속도 효과 유지 시간 체크

            # 화면 그리기
            screen.fill(BLACK)
            paddle.draw()
            ball.draw()
            for block in self.blocks:
                block.draw()
            for item in self.items:
                item.draw()

            # 점수, 생명, 속도 상태 표시
            self.draw_status()

            pygame.display.flip()
            self.clock.tick(FPS * self.speed_multiplier)

        pygame.quit()
        sys.exit()


# 게임 실행
paddle = Paddle()
ball = Ball()
game = Game()
game.run()
