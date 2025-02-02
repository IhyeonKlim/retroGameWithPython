import pygame

class Boss:
    def __init__(self, x, y=0, width=400, height=400, speed=5, speed_x=3, color=(255, 0, 0), health=1, time_limit=30000, stage=1, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed  # 아래로 이동 속도
        self.speed_x = speed_x + stage * 0.5 # 좌우 이동 속도
        self.color = color
        self.health = health + stage * 500
        self.max_health = self.health
        self.time_limit = time_limit  # 제한 시간 (밀리초)
        self.spawn_time = pygame.time.get_ticks()  # 보스 등장 시간

        # 이미지 로드
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))  # 크기 조정
            except pygame.error as e:
                print(f"[ERROR] Could not load boss image: {e}")
                self.image = None  # 이미지 로드 실패 시 None으로 설정
        else:
            self.image = None  # 이미지가 없는 경우

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, screen_width):
        """보스의 좌우 이동 및 화면 경계 충돌 처리"""
        self.x += self.speed_x

        # 화면 경계에 닿으면 방향 전환
        if self.x <= 0 or self.x + self.width >= screen_width:
            self.speed_x = -self.speed_x

    def draw(self, surface):
        """보스를 화면에 그리기"""
        if self.image:  # 이미지가 있으면 이미지로 그리기
            surface.blit(self.image, (self.x, self.y))
        else:  # 이미지가 없으면 기본 색상으로 그리기
            pygame.draw.rect(surface, self.color, self.rect)

        # 체력바 그리기
        health_ratio = self.health / self.max_health
        health_bar_width = int(self.width * health_ratio)
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y - 20, self.width, 10))  # 체력바 배경
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y - 20, health_bar_width, 10))  # 체력

        # 제한 시간 표시
        remaining_time = max(0, (self.time_limit - (pygame.time.get_ticks() - self.spawn_time)) // 1000)
        time_text = pygame.font.SysFont(None, 36).render(f" boss Time Limit: {remaining_time}s", True, (255, 0, 0))
        surface.blit(time_text, (surface.get_width() //2, 30))

    def take_damage(self, damage):
        """보스가 데미지를 입음"""
        self.health -= damage

    def is_time_up(self):
        """보스의 제한 시간이 초과되었는지 확인"""
        return pygame.time.get_ticks() - self.spawn_time > self.time_limit

    def is_dead(self):
        """보스가 죽었는지 확인"""
        return self.health <= 0