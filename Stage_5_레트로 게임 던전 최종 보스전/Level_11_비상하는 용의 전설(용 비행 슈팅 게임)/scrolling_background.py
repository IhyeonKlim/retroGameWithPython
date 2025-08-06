import pygame

class ScrollingBackground:
    def __init__(self, screen_width, screen_height, background_image_path, speed=5, alpha=200):
        """
        ScrollingBackground 초기화
        :param screen_width: 화면의 가로 크기
        :param screen_height: 화면의 세로 크기
        :param background_image_path: 배경 이미지 경로
        :param speed: 배경 스크롤 속도
        :param alpha: 이미지 투명도 (0=투명, 255=불투명)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed

        # 배경 이미지 로드 및 크기 조정
        self.background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))

        # 투명도 설정
        self.background_image = self.background_image.convert_alpha()  # 알파 채널 활성화
        self.background_image.set_alpha(alpha)  # 투명도 설정 (0-255)

        # 배경 초기 위치 설정
        self.bg_y1 = 0
        self.bg_y2 = -screen_height

    def update(self):
        """
        배경의 위치를 업데이트
        """
        self.bg_y1 += self.speed
        self.bg_y2 += self.speed

        # 화면 밖으로 나간 배경을 재배치
        if self.bg_y1 >= self.screen_height:
            self.bg_y1 = -self.screen_height
        if self.bg_y2 >= self.screen_height:
            self.bg_y2 = -self.screen_height

    def draw(self, screen):
        """
        화면에 배경을 그리기
        :param screen: pygame 화면 객체
        """
        screen.blit(self.background_image, (0, self.bg_y1))
        screen.blit(self.background_image, (0, self.bg_y2))
