import pygame

# Shop 클래스 수정
class Shop:
    def __init__(self, player, coins):
        self.player = player
        self.coins = coins
        self.selected_option = 0  # 초기값을 첫 번째 옵션으로 설정
        self.options = [
            {"label": "Increase Bullet Power (Cost: 50)", "cost": 50, "action": self.increase_bullet_power},
            {"label": "Increase Life (Cost: 100)", "cost": 100, "action": self.increase_life},
            {"label": "Exit Shop", "cost": 0, "action": self.exit_shop},
        ]

    def display(self, screen):
        """상점 화면을 표시"""
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)

        # 상점 제목
        title_text = font.render("SHOP", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_text, title_rect)

        # 옵션 리스트 표시
        for i, option in enumerate(self.options):
            # 선택된 옵션 강조 색상
            color = (0, 255, 0) if self.selected_option == i else (255, 255, 255)
            option_text = font.render(option["label"], True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, 150 + i * 50))
            screen.blit(option_text, option_rect)

        # 현재 코인 표시
        coin_text = font.render(f"Coins: {self.coins}", True, (255, 255, 255))
        coin_rect = coin_text.get_rect(topleft=(20, 20))
        screen.blit(coin_text, coin_rect)

        # ESC 텍스트 표시
        esc_text = font.render("Press ESC to Exit Shop", True, (255, 255, 255))
        esc_rect = esc_text.get_rect(bottomleft=(20, screen.get_height() - 20))
        screen.blit(esc_text, esc_rect)


    def handle_input(self, event):
        """사용자 입력 처리"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options) if self.selected_option is not None else 0
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options) if self.selected_option is not None else 0
            elif event.key == pygame.K_RETURN:
                # ENTER 키로 선택 항목 실행
                if self.selected_option is not None:
                    selected = self.options[self.selected_option]
                    if self.coins >= selected["cost"]:  # 코인 부족 여부 확인
                        self.coins -= selected["cost"]  # 코인 차감
                        selected["action"]()  # 선택된 동작 수행
                        return False  # 구매 성공
                    else:
                        print("Not enough coins!")  # 코인 부족 메시지 출력
                        return False
            elif event.key == pygame.K_ESCAPE:
                self.exit_shop()
                return True  # 상점 나가기

        return False

    def increase_bullet_power(self):
        """총알 파워 증가"""
        self.player.increase_bullet_power()
        print("Bullet power increased!")

    def increase_life(self):
        """생명력 증가"""
        self.player.add_life()
        print("Life increased!")

    def exit_shop(self):
        """상점 나가기"""
        print("Exiting shop.")
