import os

# 파일 경로 설정
SCORE_FILE = "score.txt"

# 최고 점수를 파일에서 불러오기
def load_high_score():
    """파일에서 최고 점수를 불러온다."""
    if os.path.exists(SCORE_FILE):  # 파일이 존재하는지 확인
        with open(SCORE_FILE, 'r') as f:
            try:
                high_score = int(f.read().strip())  # 파일에서 읽은 값을 정수로 변환
                return high_score
            except ValueError:
                print("파일이 비어있거나 형식이 잘못되었습니다.")
                return 0
    return 0  # 파일이 없으면 0을 반환

# 최고 점수를 파일에 저장하기
def save_high_score(score):
    """파일에 최고 점수를 저장한다."""
    with open(SCORE_FILE, 'w') as f:
        f.write(str(score))  # 점수를 문자열로 변환하여 파일에 기록

# 점수를 업데이트하고 필요시 저장하기
def update_high_score(new_score):
    """새로운 점수가 최고 점수보다 높으면 파일을 갱신한다."""
    high_score = load_high_score()  # 현재 최고 점수를 불러옴
    if new_score > high_score:  # 새로운 점수가 더 높다면
        save_high_score(new_score)  # 새로운 최고 점수를 파일에 저장
        print(f"새로운 최고 점수: {new_score}")
    else:
        print(f"현재 최고 점수: {high_score}")

# 예제 실행
if __name__ == "__main__":
    # 임의의 점수를 업데이트
    score = int(input("점수를 입력하세요: "))
    update_high_score(score)

