# ---------------import 구문 ---------------#

# 먼저 어떤 모듈, 라이브러리를 가져다가 쓰는지 확인해봐야 합니다.
# import는 최상단에 선언하는데 동작 환경에 해당 모듈이 설치되어있지 않거나, 내장되어있지 않으면 하위 코드가 동작하지 않습니다.
import random

# ---------------클래스, 인스턴스, 변수 선언부 구문 ---------------#

# 이 부분은 프로그램이 시작될 때 가장 먼저 읽히는 부분 중 하나입니다.
# 보통 어떤 것을 쓰겠다. 무엇에 관한 내용이다. 이런 '선언부'가 나오는 경우가 많습니다. 필요한 경우 개발자가 설명을 포함한 주석을 달아둡니다.
gumiho = {
    "name": "구미호", # 'name' key에 '구미호'라는 value가 저장됩니다.
    "health": 100, # 'health' key에 100이라는 value가 저장됩니다.
    "skills": [ # 'skills' key에는 스킬 딕셔너리들을 담은 리스트가 value로 저장됩니다.
        {"name": "매혹 스킬", "damage": 45, "quote": "구미호가 매혹 스킬을 시전했습니다!"}, # 각 스킬은 다시 딕셔너리입니다.
        {"name": "불꽃 발사", "damage": 35, "quote": "구미호가 불꽃을 발사했습니다!"},
        {"name": "얼음 화살", "damage": 40, "quote": "구미호가 얼음 화살을 쏘았습니다!"}
    ],
    "final_attack": {"name": "구미호의 필살기", "damage": 50, "quote": "!!!!!!!!!!농협은행!!!!!!!!!!"}, # 'final_attack' key에 필살기 딕셔너리가 value로 저장됩니다.
    "defense": 10,  # 'defense' key에 방어력 value가 저장됩니다.
}
easy_man = {
    "name": "쉬운 남자",
    "health": 100,
    "skills": [
        {"name": "바람 장막 스킬", "damage": 45, "quote": "쉬운 남자가 바람 장막 스킬을 시전했습니다!"},
        {"name": "돌풍 공격", "damage": 35, "quote": "쉬운 남자가 돌풍을 시전했습니다!"},
        {"name": "번개 공격", "damage": 40, "quote": "쉬운 남자가 번개를 발사했습니다!"}
    ],
    "final_attack": {"name": "쉬운 남자의 필살기", "damage": 50, "quote": "!!!!!!!!!!류승룡 기모찌!!!!!!!!!!"},
    "defense": 10,
}

# ---------------함수 선언부 구문 ---------------#

# 'gumiho'와 'easy_man'이라는 두 개의 딕셔너리를 선언하고 초기화했습니다.
# 각 딕셔너리는 게임 캐릭터의 모든 속성(이름, 체력, 스킬, 필살기, 방어력 등)을 key-value 쌍으로 저장합니다.
# 해당 딕셔너리만 눈여겨봐도 어떤 것을 가지고 사용할지 대략적으로 이해할 수 있습니다.

# 'roll_dice' 함수는 주사위를 굴리는 동작을 수행합니다. 함수의 명칭은 보통 동사+명사 위주로 작성됩니다. 이름만 보고도 알 수 있도록 만듭니다.
# 이 함수는 인자(argument)를 받지 않습니다. return 값만 있으니 자주 호출해서 '값'만 얻어가는 형식을 갖고 있습니다.
# 파이썬에서는 상단에 호출할 함수('callable' 이라는 표현을 씁니다.)를 미리 정의해 둡니다.
# 작성자의 의도는 1부터 6 사이의 무작위 정수 값을 반환하는 것입니다. 즉 6면체 주사위를 굴리는 함수겠군요.
# 함수가 최상단에 위치한걸로 보아 자주 사용하는 것을 뜻합니다.
def roll_dice():
    return random.randint(1, 6)

# 'select_action' 함수는 이름에서 보듯 행동을 선택하는 함수입니다.
# return 값은 actions라는 리스트에서 하나를 선택해서 반환합니다. 즉, 캐릭터의 다음 행동을 결정합니다.
# 'character'라는 인자(argument)를 받습니다. 이 인자는 'gumiho' 또는 'easy_man'과 같은 캐릭터 딕셔너리입니다.
# 작성자의 의도는 주사위 값에 따라 미리 정의된 행동 중 하나를 선택하여 반환하는 것입니다.
def select_action(character):
    # 'actions'라는 리스트에 가능한 행동들을 정의합니다.
    actions = ["normal_attack", "skill_attack", "defend", "heal", "final_attack", "nothing"]
    # 'roll_dice' 함수를 호출하여 주사위 값을 얻습니다.
    # dice 변수는 인덱스 번호가 되는 군요
    dice = roll_dice()
    print(f"{character['name']}가 주사위를 굴렸습니다. 주사위 값: {dice}")
    # 주사위 값(1~6)에 해당하는 행동을 'actions' 리스트에서 선택하여 반환합니다.
    # 주사위 값은 1부터 시작하므로, 리스트 인덱스(0부터 시작)에 맞추기 위해 -1을 합니다.
    return actions[dice - 1]


# 'process_action' 함수는 공격자와 방어자의 행동에 따른 게임 로직을 처리합니다.
# 'attacker', 'defender', 'action' 세 가지 파라미터를 받습니다.
# 'attacker'와 'defender'는 캐릭터 딕셔너리일 것이라는 유추를 해볼 수 있습니다.
# 'action'은 'select_action'에서 반환된 행동 문자열일 것이라고 유추해볼 수 있죠.
# 작성자의 의도는 선택된 'action'에 따라 체력 감소, 방어력 증가, 체력 회복 등의 게임 규칙을 적용하는 것입니다.
def process_action(attacker, defender, action):
    # 'action'의 값에 따라 다른 조건문(if-elif-else)이 실행됩니다.
    if action == "normal_attack":
        print(f"{attacker['name']}가 일반 공격을 했습니다!")
        damage = 10 # 데미지를 지역변수로 사용에서 이 함수에서만 사용한다는 것을 알 수 있습니다.
        # 방어력을 고려하여 실제 데미지를 계산하고 체력을 감소시킵니다.
        # max(0, ...)는 데미지가 음수가 되는 것을 방지합니다.
        defender["health"] -= max(0, damage - defender["defense"])
        print(f"{defender['name']}가 {damage - defender['defense']}의 데미지를 받았습니다. 남은 체력: {defender['health']}")

    elif action == "skill_attack":
        # 공격자의 스킬 리스트에서 무작위로 하나의 스킬을 선택합니다.
        skill = random.choice(attacker["skills"])
        print(f"{attacker['name']}: {skill['quote']}")
        # 스킬 데미지를 방어력을 고려하여 적용합니다.
        defender["health"] -= max(0, skill["damage"] - defender["defense"])
        print(f"{defender['name']}가 {skill['damage'] - defender['defense']}의 데미지를 받았습니다. 남은 체력: {defender['health']}")

    elif action == "defend":
        print(f"{attacker['name']}가 방어 태세를 취했습니다.")
        # 방어력을 2배로 증가시킵니다.
        attacker["defense"] *= 2

    elif action == "heal":
        heal_amount = 10
        # 체력을 회복시킵니다.
        attacker["health"] += heal_amount
        print(f"{attacker['name']}가 체력을 {heal_amount}만큼 회복했습니다. 남은 체력: {attacker['health']}")

    elif action == "final_attack":
        print(f"{attacker['name']}: {attacker['final_attack']['quote']}")
        # 필살기 데미지는 방어력을 무시하고 적용됩니다.
        defender["health"] -= attacker["final_attack"]["damage"]
        print(f"{defender['name']}가 {attacker['final_attack']['damage']}의 데미지를 받았습니다. (방어력 무시) 남은 체력: {defender['health']}")

        # 필살기를 맞고도 방어자의 체력이 0보다 크면, 방어자가 반격 필살기를 시전합니다.
        if defender["health"] > 0:
            print(f"{defender['name']}가 반격합니다! 필살기를 시전합니다!")
            print(f"{defender['name']}: {defender['final_attack']['quote']}")
            # 반격 필살기 데미지를 공격자에게 적용합니다.
            attacker["health"] -= defender["final_attack"]["damage"]
            print(f"{attacker['name']}가 {defender['final_attack']['damage']}의 데미지를 받았습니다. (방어력 무시) 남은 체력: {attacker['health']}")

    else: # 'actions' 리스트에 없는 'nothing' 등의 행동일 경우
        print(f"{attacker['name']}가 어지러워 정신을 못 차리고 있다.")

# 'reset_defense' 함수는 캐릭터의 방어력을 기본값으로 되돌립니다.
# 'character'라는 인자(argument)를 받습니다.
# 작성자의 의도는 방어 태세로 증가했던 방어력을 다음 라운드 시작 전에 원래대로 돌려놓는 것입니다.
# 이 함수가 없으면 방어만 했을 경우 계속 방어력이 상단의 함수에 선택된 액션에 의해서 2배가 유지됩니다.
def reset_defense(character):
    character["defense"] = 10  # 기본 방어력으로 복구

# 'play_game' 함수는 전체 게임의 흐름을 제어하는 핵심 함수입니다.
# 이 함수는 인자(argument)를 받지 않습니다.
# 작성자의 의도는 두 캐릭터의 체력이 모두 0보다 클 때까지 라운드를 반복하며 게임을 진행하는 것입니다.
def play_game():
    print(f"게임 시작! {gumiho['name']}와 {easy_man['name']}의 대결이 시작됩니다.")

    round_count = 1
    # 'while' 반복문은 두 캐릭터 중 한 명이라도 체력이 0보다 큰 동안 게임을 계속 진행합니다.
    # 이것이 게임의 종료 조건입니다.
    while gumiho["health"] > 0 and easy_man["health"] > 0:
        print(f"\n=== 라운드 {round_count} ===") # 라운드 구분을 위한 출력입니다.
        # 사용자 입력을 기다려 다음 라운드로 진행합니다.
        input("주사위를 굴리려면 Enter를 누르세요...")

        # '구미호'의 차례를 처리합니다.
        # 'select_action' 함수에 'gumiho' 딕셔너리를 인자로 전달하여 행동을 선택합니다.
        gumiho_action = select_action(gumiho)
        # 'process_action' 함수에 공격자, 방어자, 선택된 행동을 인자로 전달하여 게임 로직을 실행합니다.
        process_action(gumiho, easy_man, gumiho_action)

        # '쉬운 남자'의 차례를 처리합니다.
        # 'select_action' 함수에 'easy_man' 딕셔너리를 인자로 전달하여 행동을 선택합니다.
        easy_man_action = select_action(easy_man)
        # 'process_action' 함수에 공격자, 방어자, 선택된 행동을 인자로 전달하여 게임 로직을 실행합니다.
        process_action(easy_man, gumiho, easy_man_action)

        # 각 캐릭터의 방어력을 기본값으로 초기화합니다.
        reset_defense(gumiho)
        reset_defense(easy_man)

        # 라운드 종료 후, 두 캐릭터의 체력을 확인하여 승패를 결정합니다.
        if easy_man["health"] <= 0:
            print(f"{easy_man['name']}가 쓰러졌습니다. {gumiho['name']}가 승리했습니다!")
            # 승패가 결정되면 'break'를 사용하여 'while' 반복문을 즉시 종료합니다.
            break
        elif gumiho["health"] <= 0:
            print(f"{gumiho['name']}가 쓰러졌습니다. {easy_man['name']}가 승리했습니다!")
            # 승패가 결정되면 'break'를 사용하여 'while' 반복문을 즉시 종료합니다.
            break

        # 다음 라운드로 진행하기 위해 라운드 카운트를 1 증가시킵니다.
        round_count += 1

# ---------------엔트리 포인트 구문 ---------------#
# 이 부분이 프로그램의 실제 실행 시작 지점입니다.
# 'play_game' 함수를 호출하여 게임을 시작합니다.
play_game()
