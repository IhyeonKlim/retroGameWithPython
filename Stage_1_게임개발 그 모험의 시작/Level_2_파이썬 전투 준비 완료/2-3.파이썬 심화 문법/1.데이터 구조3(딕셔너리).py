# 딕셔너리 선언 및 초기화
# 유명인들의 정보와 영어 점수를 저장합니다.
celebrity_scores = {
    "유재석": 85,
    "손흥민": 92,
    "카리나": 78
}

print("--- 초기 유명인 영어 점수 딕셔너리입니다 ---")
print(celebrity_scores)
print("\n") # 가독성을 위한 줄바꿈

# 출력
#--- 초기 유명인 영어 점수 딕셔너리입니다 ---
#{'유재석': 85, '손흥민': 92, '카리나': 78}

# 1. 딕셔너리 요소 접근
print("--- 딕셔너리 요소에 key로 value에 접근합니다 ---")
# '유재석' key에 해당하는 value를 가져옵니다.
key_yoo = "유재석"
# 리스트에 인덱스 번호를 넣는것 처럼 딕셔너리에 key를 넣으면 value값을 얻을 수 있습니다.
value_yoo = celebrity_scores[key_yoo]
print(f"'{key_yoo}'의 영어 점수: {value_yoo}")
print("\n") # 가독성을 위한 줄바꿈

# 출력
#--- 딕셔너리 요소에 접근합니다 ---
#'유재석'의 영어 점수: 85


# 2. 딕셔너리에 새로운 유명인 추가
print("--- 딕셔너리에 새로운 유명인을 추가합니다 ---")
new_celebrity_name = "아이유"
new_celebrity_score = 99

# 새로운 key-value 쌍 추가 인덱스처럼 key값 작성시 생성
celebrity_scores[new_celebrity_name] = new_celebrity_score
print(f"새로운 유명인 '{new_celebrity_name}' (영어 점수: {new_celebrity_score}) 추가 후:")
print(celebrity_scores)
print("\n") # 가독성을 위한 줄바꿈

# 출력
#--- 딕셔너리에 새로운 유명인을 추가합니다 ---
#새로운 유명인 '아이유' (영어 점수: 95) 추가 후:
#{'유재석': 85, '손흥민': 92, '카리나': 78, '아이유': 95}

# 3. 기존 유명인의 영어 점수 수정
print("--- 기존 유명인의 영어 점수를 수정합니다 ---")
celebrity_to_modify = "카리나"
old_score_karina = celebrity_scores[celebrity_to_modify]
new_score_karina = 88
celebrity_scores[celebrity_to_modify] = new_score_karina # '카리나' key의 value를 88로 수정
print(f"'{celebrity_to_modify}'의 영어 점수를 {old_score_karina}점에서 {new_score_karina}점으로 수정 후:")
print(celebrity_scores)
print("\n") # 가독성을 위한 줄바꿈

# 출력
#--- 기존 유명인의 영어 점수를 수정합니다 ---
#'카리나'의 영어 점수를 78점에서 88점으로 수정 후:
#{'유재석': 85, '손흥민': 92, '카리나': 88, '아이유': 99}

# 4. 딕셔너리에서 유명인 삭제 (del 사용)
print("--- 'del'을 사용하여 유명인을 삭제합니다 ---")
celebrity_to_delete_del = "유재석"
if celebrity_to_delete_del in celebrity_scores: # 삭제할 key가 딕셔너리에 존재하는지 확인
    del celebrity_scores[celebrity_to_delete_del]
    print(f"'{celebrity_to_delete_del}' key와 해당 value 삭제 후:")
    print(celebrity_scores)
else:
    print(f"'{celebrity_to_delete_del}'는 딕셔너리에 존재하지 않습니다.")
print("\n") # 가독성을 위한 줄바꿈

# 출력
#--- 'del'을 사용하여 유명인을 삭제합니다 ---
#'유재석' key와 해당 value 삭제 후:
#{'손흥민': 92, '카리나': 88, '아이유': 99}


# 5. 딕셔너리에서 유명인 삭제 (내장함수 pop() 사용)
print("--- 'pop()'을 사용하여 유명인을 삭제합니다 ---")
celebrity_to_delete_pop = "손흥민"
if celebrity_to_delete_pop in celebrity_scores: # 삭제할 key가 딕셔너리에 존재하는지 확인
    removed_score = celebrity_scores.pop(celebrity_to_delete_pop) # key 삭제 및 해당 value 반환
    print(f"'{celebrity_to_delete_pop}' key 삭제 후, 반환된 영어 점수: {removed_score}")
    print(f"딕셔너리 현재 상태: {celebrity_scores}")
else:
    print(f"'{celebrity_to_delete_pop}'는 딕셔너리에 존재하지 않습니다.")
print("\n") # 가독성을 위한 줄바꿈


# 출력
#--- 'pop()'을 사용하여 유명인을 삭제합니다 ---
#'손흥민' key 삭제 후, 반환된 영어 점수: 92
#딕셔너리 현재 상태: {'카리나': 88, '아이유': 99}


# 6. 존재하지 않는 key에 접근 시도 (KeyError 발생 예시)
print("--- 존재하지 않는 key에 접근 시도 (KeyError 발생) ---")
#print(celebrity_scores["없는유명인"]) # 이 줄의 주석을 해제하면 KeyError가 발생합니다.
print("주석 처리된 '없는유명인' key 접근 시도 시 KeyError가 발생합니다.")
print("\n") # 가독성을 위한 줄바꿈