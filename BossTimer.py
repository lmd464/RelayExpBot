from time import *
import sys

class BossTimer:

    def __init__(self):
        self.pattern_time_list = {
            '폭': sys.float_info.max,
            '레이저': sys.float_info.max,
            '전탄': sys.float_info.max
        }

    # 현재 시간을 기반으로 해당 패턴의 다음 시간을 계산하여 저장해놓음
    # pattern_type : '폭' or '레이저' or '전탄'
    def register(self, pattern_type):

        if pattern_type == '폭':
            wait_time = 10.0
        elif pattern_type == '레이저':
            wait_time = 15.0
        elif pattern_type == '전탄':
            wait_time = 150.0
        else:
            print('잘못된 패턴 등록')
            return  # 오류

        self.pattern_time_list[pattern_type] = time() + wait_time


    # 저장된 보스시간 삭제
    def delete(self, pattern_type):
        if pattern_type == '폭':
            self.pattern_time_list['폭'] = sys.float_info.max
        elif pattern_type == '레이저':
            self.pattern_time_list['레이저'] = sys.float_info.max
        elif pattern_type == '전탄':
            self.pattern_time_list['레이저'] = sys.float_info.max




    # 현재 시간이 저장된 시간 n초 전에 도달했다면 알림
    def notify(self):
        current_time = int(time())
        if self.pattern_time_list['폭'] - current_time < 3:
            self.pattern_time_list['폭'] += 10.0
            return '터짐'
        if self.pattern_time_list['레이저'] - current_time < 3:
            self.pattern_time_list['레이저'] += 15.0
            return '레이저'
        if self.pattern_time_list['전탄'] - current_time < 6:
            self.pattern_time_list['전탄'] += 150.0
            return '전탄'

        return ''

