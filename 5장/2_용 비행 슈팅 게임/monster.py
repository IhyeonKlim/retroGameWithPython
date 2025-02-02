import pygame
import random
from coin import Coin
from item import Item

class Monster:
    # 클래스 속성: 기본값 설정
    default_width = 80
    default_height = 80

    def __init__(self, x, y, width=default_width, height=default_height, speed=3, color=(128, 128, 128), health=10,special=False, stage=1, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed + stage * 0.1
        self.color = color
        self.health = health + stage * 0.1
        self.max_health = health
        self.special = special  # 특별 몬스터 여부

        # 이미지 로드 및 크기 조정
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except pygame.error as e:
                self.image = None  # 이미지 로드 실패 시 None으로 설정
        else:
            self.image = None

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """몬스터를 아래로 이동"""
        self.y += self.speed

    def draw(self, surface):
        """몬스터를 화면에 그리기"""
        if self.image:  # 이미지가 있는 경우
            surface.blit(self.image, (self.x, self.y))
        else:  # 이미지가 없는 경우 기본 색상으로 사각형 그리기
            pygame.draw.rect(surface, self.color, self.rect)

        # 체력 막대 그리기
        health_ratio = max(0, self.health / self.max_health)  # 체력 비율 계산
        health_bar_width = self.width * health_ratio  # 체력 비율에 따른 너비
        health_bar_height = 5
        health_bar_color = (255, 0, 0)  # 빨간색 체력 바

        # 체력바 그리기
        pygame.draw.rect(surface, health_bar_color,
                         (self.x, self.y - health_bar_height - 2, health_bar_width, health_bar_height))

    def take_damage(self, damage):
        """몬스터가 데미지를 받음"""
        self.health -= damage

    @classmethod
    def create_row(cls, screen_width, y, count, margin=20, distance=0, stage=1, image_path=None, special_image_path=None):
        """
        화면의 중심을 기준으로 몬스터를 한 줄로 균등 배치.
        - screen_width: 화면 가로 길이
        - y: 몬스터의 초기 y 좌표
        - count: 몬스터 수
        - margin: 화면 가장자리와 몬스터 간의 최소 거리
        """
        available_width = screen_width - 2 * margin
        gap = (available_width - count * cls.default_width) // (count - 1)
        monsters = []
        start_x = margin

        special_index = random.randint(0, count - 1)  # 특별 몬스터의 위치

        for i in range(count):
            x = start_x + i * (cls.default_width + gap)

            # 거리 기반 속성 변경
            if distance < 500:
                color = (128, 128, 128)  # 회색
                health = 30
            elif distance < 3000:
                color = (255, 255, 0)  # 노란색
                health = 50
            elif distance < 5000:
                color = (0, 0, 255)  # 파란색
                health = 70
            else:
                color = (255, 0, 0)  # 빨간색
                health = 100

            # 특별 몬스터 설정
            if i == special_index:
                special = True
                image_to_use = special_image_path
            else:
                special = False
                image_to_use = image_path

            # 몬스터 생성
            monster = cls(x=x, y=y, color=color, health=health, special=special, stage=stage, image_path=image_to_use)
            monsters.append(monster)

        return monsters

    @staticmethod
    def handle_collision(monsters, bullets, score, coin_list, item_list):
        """
        몬스터와 탄환 간 충돌 처리.
        - monsters: 몬스터 리스트
        - bullets: 탄환 리스트
        - score: 현재 점수 (참조형 변수)
        - coin_list: 생성된 코인 리스트
        - item_list: 생성된 아이템 리스트
        - screen_width: 화면 가로 길이
        """
        for bullet in bullets[:]:
            for monster in monsters[:]:
                if bullet.rect.colliderect(monster.rect):
                    monster.take_damage(bullet.damage)

                    if monster.health <= 0:
                        # 특별 몬스터 처치 시 전체 줄 제거
                        if monster.special:
                            monsters.clear()  # 해당 줄의 모든 몬스터 제거
                            score[0] += 500  # 특별 몬스터 점수 추가
                        else:
                            # 일반 몬스터 제거
                            score[0] += 100  # 점수 100점 추가
                            monsters.remove(monster)

                        # 100% 확률로 코인 생성
                        if random.randint(1, 100) <= 50:  # 코인 생성 확률 100%
                            coin_list.append(Coin.create_random_coin(monster.x + monster.width // 2, monster.y))

                        # 하이퍼 플라이트
                        if random.randint(1, 100) <= 1:
                             item_list.append(Item.create_hyper_flight_item(monster.x + monster.width // 2, monster.y))

                        # 더블샷
                        if random.randint(1, 100) <= 10:
                            item_list.append(Item.create_bullet_item(monster.x + monster.width // 2, monster.y))

                        # 자석 아이템 생성
                        if random.randint(1, 100) <= 10:  # 5% 확률
                            item_list.append(Item.create_magnet_item(monster.x + monster.width // 2, monster.y))

                    bullets.remove(bullet)  # 탄환 제거
                    break
        if not monsters:
            score[0] += 1000

    @staticmethod
    def handle_hyper_flight_collision(monsters, mid_screen_height, score, coin_list, item_list, item_spawn_chance):
        """
        하이퍼 플라이트 상태에서 화면 중간 높이 이하의 몬스터를 충돌 처리.
        - mid_screen_height: 화면 중간 높이
        - item_spawn_chance: 아이템 생성 확률 (기본값 30%)
        """
        for monster in monsters[:]:
            if monster.rect.y >= mid_screen_height:  # 화면 중간 높이 이하의 몬스터만 처리
                # 점수 추가
                score[0] += 100  # 점수 100점 추가

                # item_spawn_chance 확률로 아이템 생성
                if random.randint(1, 100) <= item_spawn_chance:
                    item_list.append(Item.create_bullet_item(monster.rect.centerx, monster.rect.centery))  # 아이템 생성
                    coin_list.append(Coin(x=monster.rect.centerx, y=monster.rect.centery))  # 코인 생성

                # 하이퍼 플라이트
                if random.randint(1, 100) <= 5:
                    item_list.append(Item.create_hyper_flight_item(monster.x + monster.width // 2, monster.y))

                # 몬스터 제거
                monsters.remove(monster)
        if not monsters:
            score[0] += 1000