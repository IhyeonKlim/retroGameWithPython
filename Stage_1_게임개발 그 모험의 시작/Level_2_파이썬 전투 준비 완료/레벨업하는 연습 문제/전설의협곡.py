import random

# 캐릭터 정보 (딕셔너리로 상태 관리)
gumiho = {
    "name": "구미호",
    "health": 80, # 현재 체력
    "initial_health": 80, # 초기 체력 (리셋용)
    "skills": [
        {"name": "매혹 스킬", "damage": 35, "quote": "구미호가 매혹 스킬을 시전했습니다!"},
        {"name": "불꽃 발사", "damage": 45, "quote": "구미호가 불꽃을 발사했습니다!"},
        {"name": "얼음 화살", "damage": 45, "quote": "구미호가 얼음 화살을 쏘았습니다!"}
    ],
    "final_attack": {"name": "구미호의 필살기", "damage": 40, "quote": "!!!!!!!!!!농협은행!!!!!!!!!!"},
    "damage": 25,
    "defense": 5,
    "heal": 10,
    "initial_defense": 5, # 초기 방어력 (리셋용)
}

easy_man = {
    "name": "쉬운 남자",
    "health": 100,
    "initial_health": 100,
    "skills": [
        {"name": "바람 장막 스킬", "damage": 25, "quote": "쉬운 남자가 바람 장막 스킬을 시전했습니다!"},
        {"name": "돌풍 공격", "damage": 35, "quote": "쉬운 남자가 돌풍을 시전했습니다!"},
        {"name": "번개 공격", "damage": 45, "quote": "쉬운 남자가 번개를 발사했습니다!"}
    ],
    "final_attack": {"name": "쉬운 남자의 필살기", "damage": 35, "quote": "!!!!!!!!!!류승룡 기모찌!!!!!!!!!!"},
    "damage": 20,
    "defense": 10,
    "heal": 0,
    "initial_defense": 10,
}

# 'blind_monk' 캐릭터의 속성을 정의하는 딕셔너리입니다.
# 다른 캐릭터 딕셔너리와 동일한 구조를 가집니다.
blind_monk = {
    "name": "눈먼 수도승",
    "health": 120,
    "initial_health": 120,
    "skills": [
        {"name": "음파 공격", "damage": 20, "quote": "눈먼 수도승이 음파 공격을 시전합니다!"},
        {"name": "용의 분노", "damage": 30, "quote": "눈먼 수도승이 용의 분노를 발산합니다!"},
        {"name": "폭풍의 눈", "damage": 40, "quote": "눈먼 수도승이 폭풍의 눈으로 적을 교란합니다!"}
    ],
    "final_attack": {"name": "눈먼 수도승의 필살기", "damage": 30, "quote": "!!!!!!!!!!이쿠!!!!!!!!!!"},
    "damage": 15,
    "defense": 15,
    "heal": 5,
    "initial_defense": 15,
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
        defender["health"] -= max(0, attacker["damage"] - defender["defense"])
        print(f"{defender['name']}가 {attacker["damage"] - defender['defense']}의 데미지를 받았습니다. 남은 체력: {defender['health']}")

    elif action == "skill_attack":
        skill = random.choice(attacker["skills"])
        print(f"{attacker['name']}: {skill['quote']}")
        defender["health"] -= max(0, skill["damage"] - defender["defense"])
        print(f"{defender['name']}가 {skill['damage'] - defender['defense']}의 데미지를 받았습니다. 남은 체력: {defender['health']}")

    elif action == "defend":
        print(f"{attacker['name']}가 방어 태세를 취했습니다.")
        attacker["defense"] *= 2  # 방어력 2배로 증가

    elif action == "heal":
        attacker["health"] += attacker["heal"]
        print(f"{attacker['name']}가 체력을 {attacker["heal"]}만큼 회복했습니다. 남은 체력: {attacker['health']}")

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
    # 캐릭터 딕셔너리에 저장된 'initial_defense' 값을 사용합니다.
    character["defense"] = character["initial_defense"]


# 'select_player_character' 함수는 사용자가 플레이할 캐릭터를 선택하도록 합니다.
# 이 함수는 인자(argument)를 받지 않습니다.
# 작성자의 의도는 사용자에게 캐릭터 목록을 보여주고, 유효한 선택을 받을 때까지 반복하여 선택된 캐릭터 딕셔너리를 반환하는 것입니다.
def select_player_character():
    # 게임에 사용될 모든 캐릭터 딕셔너리를 리스트로 묶습니다.
    all_characters = [gumiho, easy_man, blind_monk]

    while True:  # 유효한 선택을 받을 때까지 무한 반복합니다.
        print("***전설의협곡***")
        print("\n--- 캐릭터 선택 ---")
        # enumerate를 사용하여 각 캐릭터에 번호를 매겨 사용자에게 보여줍니다.
        for i, char in enumerate(all_characters):
            print(f"{i + 1}. {char['name']} (체력: {char['health']}, 공격력 : {char['damage']}, 방어력: {char['defense']} 추가힐량 : {char['heal']})")

        try:
            # 사용자로부터 캐릭터 번호를 입력받습니다.
            choice = int(input("플레이할 캐릭터의 번호를 입력하세요: "))

            # 사용자의 입력이 유효한 범위 내에 있는지 확인합니다.
            if 1 <= choice <= len(all_characters):
                # 선택된 캐릭터 딕셔너리를 반환합니다.
                return all_characters[choice - 1]  # 리스트 인덱스는 0부터 시작하므로 -1을 합니다.
                '''
                    ***return으로 함수 및 while 반복문 종료하기
                    return문은 함수를 호출한 곳으로 값을 반환하고 함수의 실행을 멈추는 역할을 합니다. 
                    return이 실행되면 return 문이 속한 함수 전체가 즉시 종료됩니다. 
                    while문 안에서 조건문 이후에 return문이 실행되면, 
                    해당 while문은 물론이고 return문이 속한 함수 전체가 즉시 종료됩니다. 
                '''
            else:
                print("유효하지 않은 번호입니다. 다시 입력해주세요.")
                # 이런식으로 사용자 입력시 개발자가 원치 않는 답변이 나오지 않게 무한반복 시키는 방법이 있습니다.
        except ValueError:
            print("숫자를 입력해주세요. 유효하지 않은 입력입니다.")



# 게임 시뮬레이션
def play_game():
    # 게임 시작 시, 사용자에게 플레이할 캐릭터를 선택하도록 합니다.
    player_character = select_player_character()

    # 모든 가능한 상대방 캐릭터 목록을 생성합니다 (플레이어 캐릭터 제외).
    all_possible_opponents = [gumiho, easy_man, blind_monk]
    # 플레이어가 선택한 캐릭터를 제외한 나머지 캐릭터들을 '남은 상대방' 목록으로 만듭니다.
    remaining_opponents = [char for char in all_possible_opponents if char != player_character]
    '''
        ***리스트 컴프리헨션
    
        remaining_opponents = [char for char in all_possible_opponents if char != player_character]
        
        이 구문은 파이썬의 매우 강력하고 간결한 기능인 리스트 컴프리헨션(List Comprehension)을 사용한 것입니다. 
        리스트 컴프리헨션은 기존 리스트나 다른 순회 가능한(iterable) 객체를 기반으로 새로운 리스트를 만들 때 사용하는 문법입니다. 
        여러 줄의 for 반복문과 if 조건문을 한 줄로 압축하여 표현할 수 있어 코드를 더 짧고 읽기 쉽게 만듭니다.
        
        이것을 풀어서 작성하면 다음과 같습니다. 
        1. 새로운 리스트를 담을 빈 리스트를 먼저 만듭니다.
            remaining_opponents = []
            
        2. 'all_possible_opponents' 리스트의 각 요소를 하나씩 'char' 변수에 할당하며 반복합니다.
            for char in all_possible_opponents:
                # 만약 현재 'char'가 'player_character'와 같지 않다면 (즉, 플레이어가 선택한 캐릭터가 아니라면),
                if char != player_character:
                    # 그 'char'를 'remaining_opponents' 리스트에 추가합니다.
                    remaining_opponents.append(char)
        3. 1과 2를 조합
            remaining_opponents = [char for char in all_possible_opponents if char != player_character]
            저는 이 구문을 이렇게 읽습니다. char가 []안에 담겨있는데 그 char는 all_possible_opponents를 순회해서 
            조건(char가 player_character가 아닌 것)에 따라서 고른걸 넣어 놓은 변수

    '''
    random.shuffle(remaining_opponents) # 상대방 순서를 무작위로 섞습니다.

    # 'remaining_opponents' 리스트가 비어있지 않은 동안 게임을 계속 진행합니다.
    # 즉, 모든 상대방을 물리칠 때까지 반복합니다.
    while remaining_opponents:
        # '남은 상대방' 목록에서 다음 상대방을 선택합니다 (리스트의 첫 번째 요소를 꺼냅니다).
        opponent_character = remaining_opponents.pop(0)

        # 새로운 대결이 시작될 때마다 플레이어와 현재 상대방의 체력 및 방어력을 초기화합니다.
        player_character["health"] = player_character["initial_health"]
        reset_defense(player_character)
        opponent_character["health"] = opponent_character["initial_health"]
        reset_defense(opponent_character)

        print(f"\n--- 대결 시작! ---")
        print(f"{player_character['name']} (플레이어) vs {opponent_character['name']} (상대방)의 대결이 시작됩니다.")

        round_count = 1 # 각 대결마다 라운드 카운트를 1로 초기화합니다.

        # 현재 상대와의 대결을 진행하는 내부 반복문입니다.
        # 플레이어와 상대방 모두 체력이 0보다 큰 동안 라운드를 반복합니다.
        while player_character["health"] > 0 and opponent_character["health"] > 0:
            print(f"\n=== 라운드 {round_count} ===")
            input("주사위를 굴리려면 Enter를 누르세요...")

            # 플레이어 캐릭터의 차례를 처리합니다.
            player_action = select_action(player_character)
            process_action(player_character, opponent_character, player_action)

            # 상대방 캐릭터의 차례를 처리합니다. (상대방이 아직 살아있을 경우에만)
            if opponent_character["health"] > 0:
                opponent_action = select_action(opponent_character)
                process_action(opponent_character, player_character, opponent_action)

            # 각 캐릭터의 방어력을 기본값으로 초기화합니다.
            reset_defense(player_character)
            reset_defense(opponent_character)

            # 라운드 종료 후, 두 캐릭터의 체력을 확인하여 승패를 결정합니다.
            if opponent_character["health"] <= 0:
                print(f"{opponent_character['name']}가 쓰러졌습니다. {player_character['name']}가 승리했습니다!")
                # 현재 상대와의 대결이 끝났으므로 내부 반복문을 종료하고 다음 상대로 넘어갑니다.
                break

            elif player_character["health"] <= 0:
                print(f"{player_character['name']}가 쓰러졌습니다. {opponent_character['name']}가 승리했습니다!")
                print("패배! 게임이 종료됩니다.")
                # 플레이어가 패배하면 게임 전체를 즉시 종료합니다.
                return

            round_count += 1

    # 외부 while 루프가 종료되면, 모든 상대방을 물리쳤다는 의미입니다.
    print("\n마지막 남은 상대와 최종 결투 이후에 모두를 무찌르고 전설이 되었습니다!")

# 게임 실행
play_game()