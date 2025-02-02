import random

# 캐릭터 정보 (딕셔너리로 상태 관리)
gumiho = {
    "name": "구미호",
    "health": 100,
    "skills": [
        {"name": "매혹 스킬", "damage": 45, "quote": "구미호가 매혹 스킬을 시전했습니다!"},
        {"name": "불꽃 발사", "damage": 35, "quote": "구미호가 불꽃을 발사했습니다!"},
        {"name": "얼음 화살", "damage": 40, "quote": "구미호가 얼음 화살을 쏘았습니다!"}
    ],
    "final_attack": {"name": "구미호의 필살기", "damage": 50, "quote": "구미호: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!농협은행!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"},
    "defense": 10,  # 방어력
}

easy_man = {
    "name": "쉬운 남자",
    "health": 100,
    "skills": [
        {"name": "바람 장막 스킬", "damage": 45, "quote": "쉬운 남자가 바람 장막 스킬을 시전했습니다!"},
        {"name": "돌풍 공격", "damage": 35, "quote": "쉬운 남자가 돌풍을 시전했습니다!"},
        {"name": "번개 공격", "damage": 40, "quote": "쉬운 남자가 번개를 발사했습니다!"}
    ],
    "final_attack": {"name": "쉬운 남자의 필살기", "damage": 50, "quote": "쉬운 남자: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!류승룡 기모찌!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"},
    "defense": 10,  # 방어력
}

# 주사위를 굴리는 함수
def roll_dice():
    return random.randint(1, 6)

# 캐릭터 액션 선택 (주사위 기반 랜덤 선택)
def select_action(character):
    actions = ["normal_attack", "skill_attack", "defend", "heal", "final_attack", "nothing"]
    dice = roll_dice()
    print(f"{character['name']}가 주사위를 굴렸습니다. 주사위 값: {dice}")
    return actions[dice - 1]

# 행동을 처리하는 함수
def process_action(attacker, defender, action):
    if action == "normal_attack":
        print(f"{attacker['name']}가 일반 공격을 했습니다!")
        damage = 10
        defender["health"] -= max(0, damage - defender["defense"])
        print(f"{defender['name']}가 {damage - defender['defense']}의 데미지를 받았습니다. 남은 체력: {defender['health']}")

    elif action == "skill_attack":
        skill = random.choice(attacker["skills"])
        print(f"{attacker['name']}: {skill['quote']}")
        defender["health"] -= max(0, skill["damage"] - defender["defense"])
        print(f"{defender['name']}가 {skill['damage'] - defender['defense']}의 데미지를 받았습니다. 남은 체력: {defender['health']}")

    elif action == "defend":
        print(f"{attacker['name']}가 방어 태세를 취했습니다.")
        attacker["defense"] *= 2  # 방어력 2배로 증가

    elif action == "heal":
        heal_amount = 10
        attacker["health"] += heal_amount
        print(f"{attacker['name']}가 체력을 {heal_amount}만큼 회복했습니다. 남은 체력: {attacker['health']}")

    elif action == "final_attack":
        print(f"{attacker['name']}: {attacker['final_attack']['quote']}")
        defender["health"] -= attacker["final_attack"]["damage"]  # 방어력 무시
        print(f"{defender['name']}가 {attacker['final_attack']['damage']}의 데미지를 받았습니다. (방어력 무시) 남은 체력: {defender['health']}")

        # 필살기를 맞고도 살아있으면, 반대편 필살기 시전
        if defender["health"] > 0:
            print(f"{defender['name']}가 반격합니다! 필살기를 시전합니다!")
            print(f"{defender['name']}: {defender['final_attack']['quote']}")
            attacker["health"] -= defender["final_attack"]["damage"]
            print(f"{attacker['name']}가 {defender['final_attack']['damage']}의 데미지를 받았습니다. (방어력 무시) 남은 체력: {attacker['health']}")

    else:
        print(f"{attacker['name']}가 어지러워 정신을 못 차리고 있다.")

# 방어력을 초기화하는 함수 (방어 태세 종료 시)
def reset_defense(character):
    character["defense"] = 10  # 기본 방어력으로 복구

# 게임 시뮬레이션
def play_game():
    print(f"게임 시작! {gumiho['name']}와 {easy_man['name']}의 대결이 시작됩니다.")

    round_count = 1
    while gumiho["health"] > 0 and easy_man["health"] > 0:
        print(f"\n=== 라운드 {round_count} ===")

        input("주사위를 굴리려면 Enter를 누르세요...")

        # 구미호의 차례
        gumiho_action = select_action(gumiho)
        process_action(gumiho, easy_man, gumiho_action)

        # 쉬운 남자의 차례
        easy_man_action = select_action(easy_man)
        process_action(easy_man, gumiho, easy_man_action)

        # 방어력이 증가했을 경우, 한 번의 공격 후 다시 초기화
        reset_defense(gumiho)
        reset_defense(easy_man)

        # 체력 체크
        if easy_man["health"] <= 0:
            print(f"{easy_man['name']}가 쓰러졌습니다. {gumiho['name']}가 승리했습니다!")
            break
        elif gumiho["health"] <= 0:
            print(f"{gumiho['name']}가 쓰러졌습니다. {easy_man['name']}가 승리했습니다!")
            break

        round_count += 1

# 게임 실행
play_game()