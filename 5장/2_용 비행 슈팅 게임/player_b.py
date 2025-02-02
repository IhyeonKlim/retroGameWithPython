import pygame
from bullet import Bullet

class Player:
    def __init__(self, x, y, width, height, speed, color, bullet_interval=200, image_path=None):
        """
        플레이어 객체 초기화
        :param x: 플레이어의 초기 x 좌표
        :param y: 플레이어의 초기 y 좌표
        :param width: 플레이어의 너비
        :param height: 플레이어의 높이
        :param speed: 플레이어의 이동 속도
        :param color: 플레이어 색상
        :param bullet_interval: 자동 발사 간격 (밀리초 단위)
        :param image_path: 플레이어 이미지 경로
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        self.lives = 3  # 플레이어의 초기 생명

        self.image = None
        if image_path:  # 이미지 경로가 제공된 경우
            self.image = pygame.image.load(image_path)  # 이미지 로드
            self.image = pygame.transform.scale(self.image, (width, height))  # 플레이어 크기에 맞게 조정

        # 총알 관련 상태
        self.bullets = []  # 발사된 총알 리스트
        self.bullet_interval = bullet_interval  # 자동 발사 간격
        self.last_bullet_time = 0  # 마지막 발사 시간
        self.bullet_effect_end_time = None  # 총알 효과 종료 시간
        self.bullet_count = 1  # 동시에 발사할 총알 개수
        self.bullet_level = 1  # 총알 레벨
        self.bullet_damage = self.bullet_level * 10  # 총알 데미지 (레벨에 비례)

        # 하이퍼 플라이트 상태
        self.hyper_flight_active = False  # 하이퍼 플라이트 활성화 여부
        self.hyper_flight_end_time = None  # 하이퍼 플라이트 종료 시간
        self.hyper_flight_message = None  # 하이퍼 플라이트 메시지

        # 자석 상태
        self.magnet_active = False  # 자석 효과 활성화 여부
        self.magnet_effect_end_time = None  # 자석 효과 종료 시간

    @property
    def rect(self):
        """플레이어의 충돌 영역 반환"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys, screen_width):
        """
        플레이어의 이동 처리
        :param keys: 현재 눌린 키 상태
        :param screen_width: 화면 너비
        """
        if keys[pygame.K_LEFT] and self.x > 0:  # 왼쪽 이동 (화면 경계 확인)
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width:  # 오른쪽 이동 (화면 경계 확인)
            self.x += self.speed

    def shoot(self):
        """플레이어가 총알을 발사"""
        offsets = [i * 10 for i in range(-(self.bullet_count // 2), self.bullet_count // 2 + 1)]
        for offset in offsets:  # 총알 개수에 따라 대칭적으로 발사
            bullet_x = self.x + self.width // 2 + offset
            bullet_y = self.y - 15
            new_bullet = Bullet(bullet_x, bullet_y, damage=self.bullet_damage)  # 새 총알 생성
            self.bullets.append(new_bullet)

    def auto_shoot(self):
        """자동으로 일정 간격으로 총알 발사"""
        current_time = pygame.time.get_ticks()  # 현재 시간
        if current_time - self.last_bullet_time > self.bullet_interval:  # 발사 간격 확인
            self.shoot()  # 총알 발사
            self.last_bullet_time = current_time  # 마지막 발사 시간 갱신

    def increase_bullet_count(self):
        """총알 개수 증가 (최대 5발)"""
        if self.bullet_count < 5:
            self.bullet_count += 1
        self.bullet_effect_end_time = pygame.time.get_ticks() + 10000  # 효과 종료 시간 설정 (10초 후)

    def reset_bullet_count(self):
        """총알 개수를 초기화"""
        self.bullet_count = 1
        self.bullet_effect_end_time = None

    def update_bullet_effect(self, ticks_manager):
        """총알 효과의 지속 시간 관리"""
        current_time = ticks_manager.get_ticks()
        if self.bullet_effect_end_time and current_time > self.bullet_effect_end_time:  # 효과 종료 시간 초과 시
            self.reset_bullet_count()  # 총알 개수 초기화

    def update_bullets(self, surface):
        """총알을 이동시키고 화면에 그리기"""
        for bullet in self.bullets[:]:
            bullet.move()  # 총알 이동
            if bullet.y < 0:  # 화면 밖으로 벗어난 총알 제거
                self.bullets.remove(bullet)
            else:
                bullet.draw(surface)  # 화면에 총알 그리기

    def activate_hyper_flight(self, ticks_manager, duration=5000):
        """하이퍼 플라이트 활성화"""
        if not self.hyper_flight_active:  # 이미 활성화된 경우 크기 증가 방지
            self.width *= 2  # 크기 증가
            self.height *= 2  # 크기 증가
        self.hyper_flight_active = True
        self.hyper_flight_end_time = ticks_manager.get_ticks() + duration  # 종료 시간 설정
        self.hyper_flight_message = "Hyper Flight Activated!"  # 메시지 설정

    def deactivate_hyper_flight(self):
        """하이퍼 플라이트 비활성화"""
        self.hyper_flight_active = False
        self.hyper_flight_end_time = None
        self.hyper_flight_message = None
        self.width //= 2  # 크기 복원
        self.height //= 2  # 크기 복원

    def is_hyper_flight_active(self):
        """하이퍼 플라이트 활성화 상태 확인"""
        return self.hyper_flight_active

    def update_hyper_flight(self, ticks_manager):
        """하이퍼 플라이트 상태 업데이트"""
        if self.hyper_flight_active and ticks_manager.get_ticks() > self.hyper_flight_end_time:
            self.deactivate_hyper_flight()

    def get_hyper_flight_time_left(self, ticks_manager):
        """하이퍼 플라이트 남은 시간 반환"""
        if self.hyper_flight_active and self.hyper_flight_end_time:
            remaining_time = (self.hyper_flight_end_time - ticks_manager.get_ticks()) // 1000
            return max(0, remaining_time)
        return 0

    def get_hyper_flight_message(self):
        """하이퍼 플라이트 메시지 반환"""
        return self.hyper_flight_message

    def activate_magnet(self, ticks_manager, duration=5000):
        """자석 효과 활성화"""
        self.magnet_active = True
        self.magnet_effect_end_time = ticks_manager.get_ticks() + duration

    def deactivate_magnet(self):
        """자석 효과 비활성화"""
        self.magnet_active = False
        self.magnet_effect_end_time = None

    def get_magnet_time_left(self, ticks_manager):
        """자석 효과 남은 시간 반환"""
        if self.magnet_active and self.magnet_effect_end_time:
            remaining_time = (self.magnet_effect_end_time - ticks_manager.get_ticks()) // 1000
            return max(0, remaining_time)
        return None

    def update_magnet(self, ticks_manager, coin_list, item_list, coins, attraction_radius=400):
        """
        자석 효과 활성화 시 동전 및 아이템을 끌어당김
        :param coin_list: 화면에 있는 동전 리스트
        :param item_list: 화면에 있는 아이템 리스트
        :param coins: 수집한 동전 개수
        :param attraction_radius: 자석 효과 범위
        """
        if not self.magnet_active:
            return

        # 자석 효과 종료 여부 확인
        if self.magnet_effect_end_time and ticks_manager.get_ticks() > self.magnet_effect_end_time:
            self.deactivate_magnet()
            return

        player_center_x = self.x + self.width // 2
        player_center_y = self.y + self.height // 2

        for coin in coin_list[:]:
            distance_x = player_center_x - coin.x
            distance_y = player_center_y - coin.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance <= attraction_radius:  # 자석 범위 내에 있는 경우
                coin.x += distance_x * 0.2
                coin.y += distance_y * 0.2

                if abs(distance_x) < 5 and abs(distance_y) < 5:  # 가까운 경우 수집
                    coins += coin.value
                    coin_list.remove(coin)

        for item in item_list[:]:
            distance_x = player_center_x - item.x
            distance_y = player_center_y - item.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance <= attraction_radius:  # 자석 범위 내에 있는 경우
                item.x += distance_x * 0.2
                item.y += distance_y * 0.2

                if abs(distance_x) < 5 and abs(distance_y) < 5:  # 가까운 경우 수집
                    item_list.remove(item)

    def draw(self, surface):
        """플레이어를 화면에 그리기"""
        if self.image:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)

    def increase_bullet_power(self):
        """총알 데미지 증가"""
        max_level = 10
        if self.bullet_level < max_level:
            self.bullet_level += 1
            self.bullet_damage = self.bullet_level * 10
        else:
            print("Max bullet level reached!")

    def get_bullet_level(self):
        """총알 레벨 반환"""
        return self.bullet_level

    def add_life(self):
        """플레이어 생명 추가"""
        self.lives += 1
