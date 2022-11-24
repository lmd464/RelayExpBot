from time import *


class BossTimer:

    def __init__(self):
        self.pattern_time_list = {
            '폭': -1,
            '레이저': -1,
            '전탄': -1
        }

    # 현재 시간을 기반으로 해당 패턴의 다음 시간을 계산하여 저장해놓음
    # pattern_type : '폭' or '레이저' or '전탄'
    def register(self, pattern_type):

        if pattern_type == '폭':
            wait_time = 10
        elif pattern_type == '레이저':
            wait_time = 15
        elif pattern_type == '전탄':
            wait_time = 150
        else:
            print('잘못된 패턴 등록')
            return  # 오류

        self.pattern_time_list[pattern_type] = int(time()) + wait_time


    # 현재 시간이 저장된 시간 2초 전에 도달했다면 알림
    def notify(self):
        current_time = int(time())
        if current_time == self.pattern_time_list['폭'] - 1:
            self.pattern_time_list['폭'] += 10
            return '터짐'
        if current_time == self.pattern_time_list['레이저'] - 2:
            self.pattern_time_list['레이저'] += 15
            return '레이저'
        if current_time == self.pattern_time_list['전탄'] - 5:
            self.pattern_time_list['전탄'] += 150
            return '전탄'

        return ''

