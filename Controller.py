from RelayExpTimer import *  # 릴경봇 모듈
import locale


class Controller:

    def __init__(self):
        self.relay_exp_timer = RelayExpTimer()

        locale.setlocale(locale.LC_ALL, '')

    # 명령어 입력받아 파싱, 맞는 명령을 수행
    def parse(self, message):
        try:
            splitted = message.content.split(" ")
            command_type = splitted[0]  # splitted[0] : 명령 종류

            # Init : 알림 띄울 채널 초기설정, 알림
            if command_type == "!채널설정" or command_type == "!ㅊ":
                if len(splitted) == 1:
                    self.relay_exp_timer.set_relay_chat_channel(message.channel.id)
                    return message.channel.name + " 채널로 알림이 설정되었습니다.\n"

            elif self.relay_exp_timer.get_relay_chat_channel() == -1:
                return "초기설정 : 알림받을 채팅채널을 설정해주세요. (!채널설정 / !ㅊ 입력)"


            ###################
            #      릴경명령     #
            ###################

            # 1. 등록
            elif command_type == '!등록' or command_type == "!ㄷ":

                if len(splitted) < 3:
                    return "인자가 충분하지 않습니다.\n" + ">>  !등록 [채널] [시간1]/[시간2]\n"

                location = splitted[1]  # splitted 1번 : 위치 정보
                first_minute = "".join(splitted[2:]).split("/")[0].strip()  # splitted 2번 : /로 나눠진 분 정보
                second_minute = "".join(splitted[2:]).split("/")[1].strip()

                # 시간이 숫자가 아니면 걸러내기
                if (first_minute.isnumeric() and second_minute.isnumeric()) is not True:
                    return "시간 부분에 숫자를 입력해주세요.\n" + ">>  !등록 [채널] [시간1]/[시간2]\n"

                # String -> 정수 로 변환
                first_minute = int(first_minute)
                second_minute = int(second_minute)

                # 분이 0~59가 아니면 걸러내기
                if first_minute < 0 or first_minute > 59 or \
                        second_minute < 0 or second_minute > 59:
                    return "유효한 시간을 입력해주세요.\n" + ">>  !등록 [채널] [시간1]/[시간2]\n"

                # 등록
                return self.relay_exp_timer.register(location, first_minute, second_minute) + \
                       self.relay_exp_timer.print()


            # 2. 삭제
            elif command_type == '!삭제' or command_type == '!ㅅ':

                if len(splitted) < 2:
                    return "인자가 충분하지 않습니다.\n" + ">>  !삭제 [번호]\n" + \
                           self.relay_exp_timer.print()

                delete_number = splitted[1]  # splitted 1번 : 삭제할 번호

                # 숫자가 아니면 걸러내기
                if delete_number.isnumeric() is not True:
                    return "번호 부분에 숫자를 넣어주세요.\n" + ">>  !삭제 [번호]\n"

                # 숫자로 변환
                delete_number = int(delete_number)

                # 인덱스 범위 검사
                if delete_number < 1 or delete_number > len(self.relay_exp_timer.relay_list):
                    return "유효한 범위의 번호를 입력해주세요.\n" + ">>  !삭제 [번호]\n" + \
                           self.relay_exp_timer.print()

                # 삭제
                return self.relay_exp_timer.delete(delete_number) + self.relay_exp_timer.print()


            # 3. 전체삭제
            elif command_type == '!전체삭제' or command_type == "!ㅈ":
                return self.relay_exp_timer.delete_all() + self.relay_exp_timer.print()

            # 4. 출력
            elif command_type == '!릴경' or command_type == '!ㄹ':
                wrapper = "```\n"
                link = "등록을 진행해주세요.\n" + \
                       wrapper + "https://www.afreecatv.com/total_search.html?szLocation=main&szSearchType=total&szKeyword=%EB%A3%A8%EB%82%98%20%EB%A6%B4%EA%B2%BD\n" + wrapper
                       # 끝에 생기는 wrapper 꼬투리는 bot 모듈에서 제거

                return self.relay_exp_timer.print() + (link if len(self.relay_exp_timer.relay_list) == 0 else "")

            # 5. 사용법 출력
            elif command_type == "!사용법" or command_type == "!ㅁㄹ":
                wrapper = "```\n"
                return "---------- 릴경알림 사용법 ----------\n" + \
                       "- !릴경 \n" + \
                       "- !등록 [채널] [분1]/[분2] \n" + \
                       "- !삭제 [번호] \n" + \
                       "- !전체삭제 \n" + \
                       "- !알림 [번호]  /  !알림해제 \n" + \
                       "\n(12시간 이상 지난 항목은 자동으로 삭제됩니다.)" + \
                       wrapper + "https://www.afreecatv.com/total_search.html?szLocation=main&szSearchType=total&szKeyword=%EB%A3%A8%EB%82%98%20%EB%A6%B4%EA%B2%BD\n" + wrapper
                       # 끝에 생기는 wrapper 꼬투리는 bot 모듈에서 제거

            # 6. 멘션 알림
            # 인자 개수 불일치, 숫자아닌 인자, 인덱스 벗어나는 인자 거름
            elif command_type == "!알림" or command_type == "!ㅇ":
                if len(splitted) == 2 and splitted[1].isnumeric() and \
                        1 <= int(splitted[1]) <= len(self.relay_exp_timer.relay_list):
                    user_id_to_alert = str(message.author.id)
                    self.relay_exp_timer.add_user(user_id_to_alert, int(splitted[1]))

                    return message.author.name + " 에게 알림 설정되었습니다.\n(" + \
                           self.relay_exp_timer.get_relay_entity(int(splitted[1])).stringify() + ")\n"
                else:
                    return "잘못된 명령입니다.\n" + ">>  !알림 [번호]\n" + \
                           self.relay_exp_timer.print()

            elif command_type == "!알림해제" or command_type == "!ㅎ":
                user_id_to_unalert = str(message.author.id)
                self.relay_exp_timer.delete_user(user_id_to_unalert)

                return message.author.name + " 에게 전체 알림이 해제되었습니다.\n"



        # 명령 종류는 맞으나, 인자 개수를 잘못 적은 경우
        except IndexError as e:
            res_msg = "명령 형식이 잘못되었습니다.\n"
            return res_msg

    # RelayExpTimer의 알림 메소드 호출
    def relay_exp_notify(self):
        return self.relay_exp_timer.notify()

    # RelayExpTimer의 알림채널 id Getter 호출 : 채팅채널 id를 넘겨서, bot에서 알림 전송
    def get_relay_chat_channel(self):
        return self.relay_exp_timer.get_relay_chat_channel()

    # RelayExpTimer의 만료항목 제거 메소드 호출
    def delete_outdated(self):
        return self.relay_exp_timer.delete_outdated()
