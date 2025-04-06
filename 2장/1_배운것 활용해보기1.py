## 구미호 vs 쉬운 남자 - 파이썬 기초 예제

gumiho_name = "구미호"
easy_man_name = "쉬운 남자"
# 체력 상태를 변수로 정의
gumiho_health = 100
easy_man_health = 100

gumiho_charm = 30  # 구미호의 매혹 스킬 데미지
easy_man_wind_wall = 30  # 쉬운 남자의 바람 장막 방어

# 각 케릭터의 대사 변수
easy_man_quote = "죽음은 바람과..."
gumiho_quote = "우리 같이 홀려 볼..."

# 게임 시뮬레이션 텍스트
print(f"게임 시작! {gumiho_name}와 {easy_man_name}의 대결이 시작됩니다.")
#print 함수의 f 이후 ""안의 값에다 중괄호로 {} 변수를 지정해두면 변수의 값이 출력됩니다.
print(f"{gumiho_name}: {gumiho_quote}")
print(f"{easy_man_name}: {easy_man_quote}")

#게임이 진행되는 동안 반복되는 반복문
while gumiho_health > 0 and easy_man_health > 0:
    action = input(f"{gumiho_name}가 공격할까요? (yes/no): ")

    #공격을 결정하는 조건문
    if action == ("y" or "yes"):
        print(f"{gumiho_name}가 매혹을 시전했습니다!")
        easy_man_health -= gumiho_charm
        # 같은 표현
        # easy_man_health = easy_man_health - gumiho_charm
        print(f"{easy_man_name}가 {gumiho_charm}의 데미지를 받았습니다. 남은 체력: {easy_man_health}")
    else:
        print(f"{gumiho_name}가 공격하지 않았습니다. {easy_man_name}가 반격합니다!")
        print(f"{easy_man_name}가 바람 장막을 펼쳤습니다!")
        gumiho_health -= easy_man_wind_wall
        print(f"{gumiho_name}가 {easy_man_wind_wall}의 데미지를 받았습니다. 남은 체력: {gumiho_health}")

    if easy_man_health <= 0:
        print(f"{easy_man_name}가 쓰러졌습니다. {gumiho_name}가 승리했습니다!")

    elif gumiho_health <= 0:
        print(f"{gumiho_name}가 쓰러졌습니다. {easy_man_name}가 승리했습니다!")

