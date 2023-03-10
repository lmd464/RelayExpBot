from RelayExpTimer import *     # 릴경봇 모듈
#from BossTimer import *    # 보스타이머 모듈
from BankAccount import *
import locale
from random import randint


class Controller:

    def __init__(self):
        self.relay_exp_timer = RelayExpTimer()
        '''
        self.boss_timer = BossTimer()
        self.boss_mode = False  # 보스 타이머 모드
        '''
        self.bank_account = BankAccount()

        locale.setlocale(locale.LC_ALL, '')



    # 명령어 입력받아 파싱, 맞는 명령을 수행
    def parse(self, message):
        try:
            splitted = message.content.split(" ")
            command_type = splitted[0]                      # splitted[0] : 명령 종류


            ###################
            #      릴경명령     #
            ###################

            # 1. 등록
            if command_type == '!등록':
                if len(splitted) < 3:
                    res_msg = "인자가 충분하지 않습니다.\n" + "Usage : !등록 [채널] [시간1]/[시간2]\n"
                    return res_msg

                channel = splitted[1]                                         # splitted 1번 : 채널
                first_minute = "".join(splitted[2:]).split("/")[0].strip()    # splitted 2번 : /로 나눠진 분 정보
                second_minute = "".join(splitted[2:]).split("/")[1].strip()

                # 채널, 시간이 숫자가 아니면 걸러내기
                if (channel.isnumeric() and first_minute.isnumeric() and second_minute.isnumeric()) is not True:
                    res_msg = "숫자를 정확히 입력해주세요.\n"
                    return res_msg

                # String -> 정수 로 변환
                channel = int(channel)
                first_minute = int(first_minute)
                second_minute = int(second_minute)

                # 분이 0~59가 아니면 걸러내기
                if first_minute < 0 or first_minute > 59 or \
                    second_minute < 0 or second_minute > 59:
                    res_msg = "유효한 시간을 입력해주세요.\n"
                    return res_msg

                # 등록
                return self.relay_exp_timer.register(channel, first_minute, second_minute)


            # 2. 삭제
            elif command_type == '!삭제':
                if len(splitted) < 2:
                    res_msg = "인자가 충분하지 않습니다.\n" + "Usage : !삭제 [번호]\n"
                    return res_msg

                delete_number = splitted[1]                 # splitted 1번 : 삭제할 번호

                # 숫자가 아니면 걸러내기
                if delete_number.isnumeric() is not True:
                    res_msg = "정확한 숫자를 넣어주세요.\n"
                    return res_msg

                # 숫자로 변환
                delete_number = int(delete_number)

                # 인덱스 범위 검사
                if delete_number < 1 or delete_number > len(self.relay_exp_timer.relay_list):
                    res_msg = "유효한 번호를 입력해주세요.\n"
                    return res_msg

                # 삭제
                return self.relay_exp_timer.delete(delete_number)


            # 3. 전체삭제
            elif command_type == '!전체삭제':
                return self.relay_exp_timer.delete_all()

            # 4. 출력
            elif command_type == '!릴경':
                return self.relay_exp_timer.print()

            # 5. 사용법 출력
            elif command_type == "!사용법":
                res_msg = "**---------- 사용법 ----------**\n" + \
                          "- 릴경 보기 :   !릴경\n" + \
                          "- 릴경 추가 :   !등록 [채널] [분1]/[분2]\n" + \
                          "- 릴경 삭제 :   !삭제 [번호]\n" + \
                          "- 릴경 전체삭제 :   !전체삭제\n"
                return res_msg


            ##################
            #     부가기능     #
            ##################

            # 6. 따라함 : !echo 만 제거하여 그대로 리턴
            elif command_type == "!echo":
                return " ".join(splitted[1:])

            # 7. vs
            elif " vs " in message.content:
                choice_list = message.content.split(" vs ")
                if len(choice_list) >= 2:
                    return choice_list[randint(0, len(choice_list) - 1)]
                else:
                    return ""

            # 8. 계좌목록
            elif command_type == "!계좌":
                if len(splitted) > 1:   # 인자 있음
                    acc_name = " ".join(splitted[1:])
                    return self.bank_account.get_bank_account(acc_name)
                else:
                    return "이름 넣어야함"

            # 9. 계좌추가, 삭제
            elif command_type == "!계좌추가":
                if len(splitted) > 2:
                    acc_name = splitted[1]
                    acc = " ".join(splitted[2:])
                    self.bank_account.add_bank_account(acc_name, acc)
                    return "추가완료"
                else:
                    return "사용법 : !계좌추가 이름 계좌"

            elif command_type == "!계좌삭제":
                if len(splitted) > 1:
                    acc_name = splitted[1]
                    self.bank_account.delete_bank_account(acc_name)
                    return "삭제완료"
                else:
                    return "사용법 : !계좌삭제 이름"


            '''
            ######################
            #      칼로스 타이머     #
            ######################

            # message를 보낸 사람이 입장해있는 음성채널 & 채팅채널 정보 읽어옴
            # 명령을 시작한 채팅채널로부터 채팅을 읽어와, 타이머 시작
            # 타이머가 만료되면 음성채널로 mp3파일 재생
            elif command_type == "!boss":
                ## 음성채널 입장 부분 ##
                self.boss_mode = True
                res_msg = "**####### 1 : 폭  /  2 : 레이저  /  3 : 전탄 #######**" + \
                          "\n**####### 4 : 폭 삭제  /  5 : 레이저 삭제  /  6 : 전탄 삭제 #######**"
                return res_msg


            elif command_type == "1" and self.boss_mode:
                self.boss_timer.register('폭')
                return "폭 알림 갱신"
            elif command_type == "2" and self.boss_mode:
                self.boss_timer.register('레이저')
                return "레이저 알림 갱신"
            elif command_type == "3" and self.boss_mode:
                self.boss_timer.register('전탄')
                return "전탄 알림 갱신"
            elif command_type == "4" and self.boss_mode:
                self.boss_timer.delete('폭')
                return "폭 알림 삭제"
            elif command_type == "5" and self.boss_mode:
                self.boss_timer.delete('레이저')
                return "레이저 알림 삭제"
            elif command_type == "6" and self.boss_mode:
                self.boss_timer.delete('전탄')
                return "전탄 알림 삭제"

            elif command_type == "!bossoff":
                self.boss_mode = False
                return "Timer off"


            # 명령이 위 형식이 아닐 경우, 공백 스트링 반환 (bot 에서 처리)
            else:
                res_msg = ""
                return res_msg
            '''

        # 명령 종류는 맞으나, 인자 개수를 잘못 적은 경우
        except IndexError as e:
            res_msg = "몰라레후\n"
            return res_msg


    # RelayExpTimer의 메소드 호출
    def relay_exp_notify(self):
        return self.relay_exp_timer.notify()

    '''
    # BossTimer의 메소드 호출
    def boss_pattern_notify(self):
        if self.boss_mode:
            return self.boss_timer.notify()
        else:
            return ""
    '''
