from Timer import Timer
from time import *


class Controller:

    def __init__(self):
        self.timer = Timer()

    # 명령어 입력받아 파싱
    # 맞는 Timer의 메소드 호출
    def input(self, message):
        command = message
        try:
            splitted = command.split(" ")
            command_type = splitted[0]                      # splitted 0번 : 명령 종류

            # 등록
            if command_type == '!등록':
                if len(splitted) < 3:
                    res_msg = "인자가 충분하지 않습니다.\n" + "Usage : !등록 [채널] [시간1]/[시간2]\n"
                    return res_msg

                channel = splitted[1]                                         # splitted 1번 : 채널
                first_minute = "".join(splitted[2:]).split("/")[0].strip()    # splitted 2번 : /로 나눠진 분 정보
                second_minute = "".join(splitted[2:]).split("/")[1].strip()

                # 숫자가 아니면 걸러내기
                if (channel.isnumeric() and first_minute.isnumeric() and second_minute.isnumeric()) is not True:
                    res_msg = "숫자를 정확히 입력해주세요.\n"
                    return res_msg

                # 숫자로 변환
                channel = int(channel)
                first_minute = int(first_minute)
                second_minute = int(second_minute)

                # 분이 0~59가 아니면 걸러내기
                if first_minute < 0 or first_minute > 59 or \
                    second_minute < 0 or second_minute > 59:
                    res_msg = "유효한 시간을 입력해주세요.\n"
                    return res_msg

                # 등록
                return self.timer.register(channel, first_minute, second_minute)


            # 삭제
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
                if delete_number < 1 or delete_number > len(self.timer.relay_list):
                    res_msg = "유효한 번호를 입력해주세요.\n"
                    return res_msg

                # 삭제
                return self.timer.delete(delete_number)


            elif command_type == '!전체삭제':
                return self.timer.delete_all()

            # 출력
            elif command_type == '!릴경':
                return self.timer.print()

            # 위의 형식이 아닐 경우, 에러 메시지 반환
            else:
                res_msg = "**---------- 사용법 ----------**\n" + \
                          "- 릴경 보기 :   !릴경\n" + \
                          "- 릴경 추가 :   !등록 [채널] [분1]/[분2]\n" + \
                          "- 릴경 삭제 :   !삭제 [번호]\n" + \
                          "- 릴경 전체삭제 :   !전체삭제\n"
                return res_msg


        except IndexError as e:
            res_msg = "몰라 레후\n"
            return res_msg


    # 현재 시간(분, 초) 를 받아와서, Timer 모듈에 넘겨줌
    # Timer 에서는 기존에 저장된 정보와 비교하여, 알려야 할 경우 저장된 정보를 반환
    # 저장된 정보와, 현재 시간 정보를 합친 String 반환
    def notify(self):
        current_time = localtime()
        current_min = current_time.tm_min
        current_sec = current_time.tm_sec
        relay_string = self.timer.notify(current_min, current_sec)

        if relay_string != "":
            str_time = strftime('**※ 현재 시각 : %I시 %M분 %S초 %p**\n', current_time)
            res_msg = str_time + relay_string
            return res_msg

        else:
            #print(strftime('[Debug] %I시 %M분 %S초 %p\n', current_time))
            return relay_string

