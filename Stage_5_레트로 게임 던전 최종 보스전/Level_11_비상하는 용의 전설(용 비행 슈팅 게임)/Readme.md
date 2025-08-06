프로젝트 구조
├── main.py                          # 게임 시작 지점 (전체 통합 및 루프)
        ├─── player.py                       # 플레이어 동작, 이동
        ├─── monster.py                      # 일반 몬스터 로직
        ├─── boss.py                         # 보스 몬스터
        ├─── bullet.py                       # 총알(공격)
        ├─── item.py                         # 아이템
        ├─── coin.py                         # 코인
        ├─── meteo.py                        # 운석
        ├─── utils.py                        # 범용 유틸
        ├─── scrolling_background.py         # 배경 스크롤 처리
        ├─── ticks_manager.py                # 프레임/시간 간격 관리
├── assets                          # 이미지 파일 모음 폴더