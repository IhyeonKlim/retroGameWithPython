import time

class TicksManager:
    def __init__(self):
        self.start_time = time.time()  # 게임 시작 시간을 기록

    def get_ticks(self):
        """게임이 시작된 후 경과한 시간을 밀리초 단위로 반환"""
        return int((time.time() - self.start_time) * 1000)

    def reset_ticks(self):
        """현재 시간을 기준으로 시간을 초기화"""
        self.start_time = time.time()
