from Timer import Timer
import locale
from random import randint


class Controller:

    def __init__(self):
        self.timer = Timer()
        locale.setlocale(locale.LC_ALL, '')


    # 명령어 입력받아 파싱, 맞는 명령을 수행
    def parse(self, message):
        command = message
        try:
            splitted = command.split(" ")
            command_type = splitted[0]                      # splitted[0] : 명령 종류

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
                return self.timer.register(channel, first_minute, second_minute)


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
                if delete_number < 1 or delete_number > len(self.timer.relay_list):
                    res_msg = "유효한 번호를 입력해주세요.\n"
                    return res_msg

                # 삭제
                return self.timer.delete(delete_number)


            # 3. 전체삭제
            elif command_type == '!전체삭제':
                return self.timer.delete_all()

            # 4. 출력
            elif command_type == '!릴경':
                return self.timer.print()

            # 5. 사용법 출력
            elif command_type == "!사용법":
                res_msg = "**---------- 사용법 ----------**\n" + \
                          "- 릴경 보기 :   !릴경\n" + \
                          "- 릴경 추가 :   !등록 [채널] [분1]/[분2]\n" + \
                          "- 릴경 삭제 :   !삭제 [번호]\n" + \
                          "- 릴경 전체삭제 :   !전체삭제\n"
                return res_msg


            # 6. 복화술 기능 : !echo 만 제거하여 그대로 리턴
            elif command_type == "!echo":
                return " ".join(splitted[1:])

            # 7. vs
            elif " vs " in message:
                choice_list = message.split(" vs ")
                return choice_list[randint(0, len(choice_list) - 1)]

            # 8. 애옹
            elif "애옹" in message:
                return "ㅋㅋㅋ"


            # 명령이 위 형식이 아닐 경우, 공백 스트링 반환 (bot 에서 처리)
            else:
                res_msg = ""
                return res_msg


        # 명령 종류는 맞으나, 인자 개수를 잘못 적은 경우
        except IndexError as e:
            res_msg = "몰라레후\n"
            return res_msg


    # Timer의 메소드 호출
    def notify(self):
        return self.timer.notify()
