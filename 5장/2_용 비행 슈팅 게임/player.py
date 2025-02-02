import pygame
from bullet import Bullet

class Player:
    def __init__(self, x, y, width, height, speed, color, bullet_interval=200, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        self.lives = 3  # 생명

        self.image = None

        if image_path:  # 이미지 경로가 제공된 경우
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))  # 플레이어 크기에 맞게 이미지 크기 조정

        # bullet 상태
        self.bullets = []
        self.bullet_interval = bullet_interval  # 자동 발사 간격 (밀리초)
        self.last_bullet_time = 0
        self.bullet_effect_end_time = 10
        self.bullet_count = 1  # 현재 발사할 총알 개수 (최대 5발)
        self.bullet_level = 1  # 총알 레벨 (초기값)
        self.bullet_damage = self.bullet_level * 10  # 총알 데미지

        # Hiper Flight 상태
        self.hyper_flight_active = False
        self.hyper_flight_end_time = None
        self.hyper_flight_message = None

        #자석 상태
        self.magnet_active = False  # 자석 활성화 상태
        self.magnet_effect_end_time = None  # 자석 효과 종료 시간

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys, screen_width):
        """플레이어의 키 입력에 따라 이동"""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width:
            self.x += self.speed

    def shoot(self):
        """플레이어가 탄환을 발사 (총알 개수에 따라 대칭적으로 나감)"""
        offsets = [i * 10 for i in range(-(self.bullet_count // 2), self.bullet_count // 2 + 1)]
        for offset in offsets:
            bullet_x = self.x + self.width // 2 + offset
            bullet_y = self.y - 15
            new_bullet = Bullet(bullet_x, bullet_y, damage=self.bullet_damage)
            self.bullets.append(new_bullet)

    def auto_shoot(self):
        """자동으로 탄환 발사"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_time > self.bullet_interval:
            self.shoot()
            self.last_bullet_time = current_time

    # 아이템 + 더블샷
    def increase_bullet_count(self):
        """총알 개수 증가 (최대 5발)"""
        if self.bullet_count < 5:
            self.bullet_count += 1
        # 효과 종료 시간을 현재 시간 + 10초로 설정
        self.bullet_effect_end_time = pygame.time.get_ticks() + 10000

    def reset_bullet_count(self):
        """총알 개수를 초기화"""
        self.bullet_count = 1
        self.bullet_effect_end_time = None

    def update_bullet_effect(self, ticks_manager):
        """총알 아이템 효과가 지속되는 동안 효과를 관리"""
        current_time = ticks_manager.get_ticks()  # TicksManager로 현재 시간 가져오기
        if self.bullet_effect_end_time and current_time > self.bullet_effect_end_time:
            self.reset_bullet_count()  # 총알 개수를 초기화

    def update_bullets(self, surface):
        """모든 탄환을 이동하고 화면에 그리기"""
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:  # 화면을 벗어난 탄환은 제거
                self.bullets.remove(bullet)
            else:
                bullet.draw(surface)

    # 아이템 + 하이퍼 플라이트
    def activate_hyper_flight(self, ticks_manager, duration=5000):
        """하이퍼 플라이트 활성화"""
        if not self.hyper_flight_active:  # 이미 활성화된 경우 크기 증가 방지
            self.width *= 2  # 크기 증가
            self.height *= 2  # 크기 증가
        self.hyper_flight_active = True
        self.hyper_flight_end_time = ticks_manager.get_ticks() + duration
        self.hyper_flight_message = "Hyper Flight Activated!"  # 메시지 설정

    def deactivate_hyper_flight(self):
        """하이퍼 플라이트 비활성화"""
        self.hyper_flight_active = False
        self.hyper_flight_end_time = None
        self.hyper_flight_message = None  # 메시지 초기화
        self.width //= 2  # 크기 복원
        self.height //= 2  # 크기 복원

    def is_hyper_flight_active(self):
        """하이퍼 플라이트 상태 확인"""
        return self.hyper_flight_active

    def update_hyper_flight(self, ticks_manager):
        """하이퍼 플라이트 상태 업데이트"""
        if self.hyper_flight_active and ticks_manager.get_ticks() > self.hyper_flight_end_time:
            self.deactivate_hyper_flight()

    def get_hyper_flight_time_left(self, ticks_manager):
        """하이퍼 플라이트 남은 시간 반환 (초 단위)"""
        if self.hyper_flight_active and self.hyper_flight_end_time:
            remaining_time = (self.hyper_flight_end_time - ticks_manager.get_ticks()) // 1000
            return max(0, remaining_time)
        return 0
    def get_hyper_flight_message(self):
        """현재 하이퍼 플라이트 메시지를 반환"""
        return self.hyper_flight_message

    # 자석 효과
    def activate_magnet(self, ticks_manager, duration=5000):
        """자석 효과 활성화"""
        self.magnet_active = True
        self.magnet_effect_end_time = ticks_manager.get_ticks() + duration

    def deactivate_magnet(self):
        """자석 효과 비활성화"""
        self.magnet_active = False
        self.magnet_effect_end_time = None

    def get_magnet_time_left(self, ticks_manager):
        """자석 효과 남은 시간 반환 (초 단위)"""
        if self.magnet_active and self.magnet_effect_end_time:
            remaining_time = (self.magnet_effect_end_time - ticks_manager.get_ticks()) // 1000
            return max(0, remaining_time)
        return None

    def update_magnet(self, ticks_manager, coin_list, item_list, coins, attraction_radius=400):
        """
        자석 효과 활성화 시 아이템과 동전을 끌어당김.
        - coin_list: 화면에 표시된 동전 리스트
        - item_list: 화면에 표시된 아이템 리스트
        - coins: 수집한 동전 개수
        - items_collected: 수집한 아이템 개수
        - attraction_radius: 자석 범위
        """
        if not self.magnet_active:
            return

        # 효과 종료 확인
        if self.magnet_effect_end_time and ticks_manager.get_ticks() > self.magnet_effect_end_time:
            self.deactivate_magnet()
            return

        player_center_x = self.x + self.width // 2
        player_center_y = self.y + self.height // 2

        # 200px 이내의 아이템과 코인을 끌어당김
        for coin in coin_list[:]:
            distance_x = player_center_x - coin.x
            distance_y = player_center_y - coin.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5  # 거리 계산

            if distance <= attraction_radius:
                coin.x += distance_x * 0.2
                coin.y += distance_y * 0.2

                if abs(distance_x) < 5 and abs(distance_y) < 5:  # 약간의 오차 허용
                    coins += coin.value  # 코인의 가치를 추가
                    coin_list.remove(coin)

        for item in item_list[:]:
            distance_x = player_center_x - item.x
            distance_y = player_center_y - item.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5  # 거리 계산

            if distance <= attraction_radius:
                item.x += distance_x * 0.2
                item.y += distance_y * 0.2

                if abs(distance_x) < 5 and abs(distance_y) < 5:  # 약간의 오차 허용
                    item_list.remove(item)

    def draw(self, surface):
        """플레이어를 화면에 그리기"""
        """
        플레이어를 화면에 그리기
        :param screen: pygame 화면 객체
        """
        if self.image:  # 이미지가 있는 경우
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:  # 이미지가 없는 경우 색상으로 그리기
            pygame.draw.rect(surface, self.color, self.rect)

    def increase_bullet_power(self):
        """총알 레벨 증가 및 데미지 업데이트"""
        max_level = 10
        if self.bullet_level < max_level:
            self.bullet_level += 1
            self.bullet_damage = self.bullet_level * 10  # 데미지 업데이트
        else:
            print("Max bullet level reached!")

    def get_bullet_level(self):
        """총알 레벨 반환"""
        return self.bullet_level

    def add_life(self):
        """생명력 추가"""
        self.lives += 1
