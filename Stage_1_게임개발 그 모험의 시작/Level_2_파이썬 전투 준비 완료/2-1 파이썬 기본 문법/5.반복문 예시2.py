# break로 무한 반복 종료
count = 0

while True:
    count += 1
    # 짝수일 경우, 이번 반복을 건너뛰고 다음 반복으로 넘어갑니다.
    if count % 2 == 0: # %는 나머지를 뜻합니다. 2로 나눈 나머지가 0 == 짝수.
        continue
    # count가 5가 되면, 반복문을 완전히 종료합니다.
    if count == 5:
        break
    print(count)

# 출력:
# 1
# 3