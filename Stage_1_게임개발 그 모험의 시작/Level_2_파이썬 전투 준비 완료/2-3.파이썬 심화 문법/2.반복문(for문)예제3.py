# 쇼핑 리스트를 정의합니다.
shopping_list = ["apple", "banana", "cherry", "orange", "grape", "kiwi", "melon","tomato", "pineapple", "potato", "onion"]

print("--- 쇼핑 리스트 순회 시작 ---")

# len() 함수와 range() 함수, 그리고 인덱스를 사용하여 리스트를 순회합니다.
# len(shopping_list)는 리스트의 총 요소 개수를 반환합니다.
# range()은 0부터 len(shopping_lsit)까지의 정수 시퀀스를 생성합니다.
for i in range(len(shopping_list)):
    current_fruit = shopping_list[i] # 현재 인덱스에 해당하는 과일을 가져옵니다.

    # 1. 특정 과일을 건너뛰기 (continue 사용)
    # 'banana' 또는 'kiwi'일 경우, 이번 반복을 건너뛰고 다음 과일로 넘어갑니다.
    if current_fruit == "banana" or current_fruit == "kiwi":
        print(f"인덱스 {i}: {current_fruit} - 이 과일은 건너뜁니다.")
        continue # 현재 반복을 중단하고 다음 반복으로 넘어갑니다.

    # 2. 특정 과일이 포함되어 있는지 확인 (in 연산자 사용)
    # 'apple'이 현재 과일에 포함되어 있는지 확인합니다.
    if "apple" in current_fruit:
        print(f"인덱스 {i}: {current_fruit} - 'apple'이 포함된 쇼핑 리스트입니다..")
    # 'z'가 현재 과일에 포함되어 있지 않은지 확인 (not in 연산자 사용)
    elif "z" not in current_fruit:
        print(f"인덱스 {i}: {current_fruit} - 'z'가 포함되어 있지 않은 쇼핑 리스트입니다..")

    # 3. 특정 조건에서 반복 중단 (break 사용)
    # 'grape'를 만나면 반복문을 완전히 종료합니다.
    if current_fruit == "grape":
        print(f"인덱스 {i}: {current_fruit} - 'grape'를 찾았습니다! 반복을 중단합니다.")
        break # 반복문을 완전히 종료합니다.

    # 위의 조건에 해당하지 않는 경우 기본 출력입니다.
    # 이 부분은 continue에 의해 'banana'와 'kiwi'일 때는 실행되지 않습니다.
    # 또한 break에 의해 'grape' 이후의 과일들은 처리되지 않습니다.
    print(f"인덱스 {i}: {current_fruit} - 일반 처리되었습니다.")

print("--- 쇼핑 리스트 순회 종료 ---")


# 출력
#--- 쇼핑 리스트 순회 시작 ---
#인덱스 0: apple - 'apple'이 포함된 쇼핑 리스트입니다..
#인덱스 0: apple - 일반 처리되었습니다.
#인덱스 1: banana - 이 과일은 건너뜁니다.
#인덱스 2: cherry - 'z'가 포함되어 있지 않은 쇼핑 리스트입니다..
#인덱스 2: cherry - 일반 처리되었습니다.
#인덱스 3: orange - 'z'가 포함되어 있지 않은 쇼핑 리스트입니다..
#인덱스 3: orange - 일반 처리되었습니다.
#인덱스 4: grape - 'z'가 포함되어 있지 않은 쇼핑 리스트입니다..
#인덱스 4: grape - 'grape'를 찾았습니다! 반복을 중단합니다.
#--- 쇼핑 리스트 순회 종료 ---