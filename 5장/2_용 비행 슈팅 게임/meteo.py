import pygame
import random

class Meteo:
    default_width = 150
    default_height = 150
    WARNING_COLOR = (255, 0, 0)  # 빨간색 경고 표시
    METEO_COLOR = (255, 0, 0)  # 회색 운석

    def __init__(self, x, y=-50, width=default_width, height=default_height, speed=10, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.state = "warning"  # 초기 상태: "warning" -> "falling"
        self.warning_start_time = pygame.time.get_ticks()  # 경고 시작 시간
        self.warning_duration = 2000  # 경고 시간 (2초)

        # 이미지 로드
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))  # 크기 조정
            except pygame.error as e:
                print(f"[ERROR] Could not load image: {e}")
                self.image = None  # 이미지 로드 실패 시 None으로 설정
        else:
            self.image = None  # 이미지가 없는 경우
    @property
    def rect(self):
        """운석의 충돌 영역 반환"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """운석 이동"""
        if self.state == "falling":
            self.y += self.speed

    def update_state(self):
        """운석 상태 업데이트: 경고 -> 낙하"""
        current_time = pygame.time.get_ticks()
        if self.state == "warning" and current_time - self.warning_start_time > self.warning_duration:
            self.state = "falling"
            self.y = -self.height  # 화면 상단 끝에서 시작

    def draw_warning(self, surface, font):
        """운석 출현 전 경고 표시"""
        if self.state == "warning":
            warning_text = font.render("!!!!!", True, self.WARNING_COLOR)
            text_rect = warning_text.get_rect(center=(self.x + self.width // 2, 200))
            surface.blit(warning_text, text_rect)

    def draw_guide_line(self, surface, screen_height):
        """운석 이동 경로 유도선 그리기"""
        if self.state == "warning":
            pygame.draw.line(surface, self.WARNING_COLOR, (self.x + self.width // 2, -self.height), (self.x + self.width // 2, screen_height), 1)

    def draw(self, surface):
        """운석 그리기"""
        if self.state == "falling":
            if self.image:  # 이미지가 있으면 이미지로 그리기
                surface.blit(self.image, (self.x, self.y))
            else:  # 이미지가 없으면 기본 색상으로 그리기
                pygame.draw.rect(surface, self.METEO_COLOR, self.rect)

    @staticmethod
    def create_random(screen_width, image_path=None):
        """화면의 랜덤 위치에 운석 생성"""
        x = random.randint(0, screen_width - Meteo.default_width)
        return Meteo(x=x, image_path=image_path)
