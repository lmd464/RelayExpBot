from RelayEntity import *
from time import *


class RelayExpTimer:

    def __init__(self):
        self.relay_list = []
        self.user_id_list = []  # 멘션으로 알릴 사용자 리스트

    # 등록 : !등록 [채널] [분1]/[분2]
    # 시간 순서대로 정렬시킴
    # 인덱스에 의한 순번 자동 부여
    def register(self, channel, first_minute, second_minute):
        relay_entity = RelayEntity(channel, first_minute, second_minute)
        self.relay_list.append(relay_entity)

        res_msg = "등록 완료 되었습니다.\n"

        # 정렬
        self.relay_list = sorted(self.relay_list, key=lambda entity: entity.first_minute)

        return res_msg + self.print()

    # 삭제 : !삭제 [번호]
    def delete(self, number):
        if len(self.relay_list) == 0:
            res_msg = "삭제할 항목이 없습니다.\n"
            return res_msg
        self.relay_list.pop(number - 1)
        res_msg = "삭제 완료되었습니다.\n"

        return res_msg + self.print()

    # 전체삭제 : !전체삭제
    def delete_all(self):
        if len(self.relay_list) == 0:
            res_msg = "삭제할 항목이 없습니다.\n"
            return res_msg
        self.relay_list.clear()
        res_msg = "전체 삭제 완료되었습니다.\n"
        return res_msg

    # 출력 : !릴경
    def print(self):
        num = 1
        res_msg = ""
        if len(self.relay_list) != 0:
            for entity in self.relay_list:
                res_msg += (str(num) + " )  " + entity.stringify()) + "\n"
                num += 1
            return res_msg
        else:
            res_msg = "저장된 정보가 없습니다.\n"
            return res_msg

    # 현재 시간이 저장된 시간의 1분 전이라면 해당 정보 스트링을 반환한다.
    # 현재 시간(분, 초) 을 받아와서, Relay List 에 있는 Entity 들을 탐색하며
    # 알려야 하는 요소가 있으면 현재 시간과 저장된 시간에 대한 String 반환
    # 없으면 빈 문자열 반환
    def notify(self):
        current_time = localtime()
        current_min = current_time.tm_min
        current_sec = current_time.tm_sec

        # 알릴 정보가 없는 상태 :
        if len(self.relay_list) == 0:
            return ""

        # 알릴 정보가 있는 상태
        else:
            for relay_entity in self.relay_list:

                # 첫 시간이 00분일 때 1분 전 / # 첫번째 시간의 1분 전 /  # 두번째 시간의 1분 전
                if (current_min == 59 and relay_entity.get_first_minute() == 0 and current_sec == 1) or \
                        (current_min == relay_entity.get_first_minute() - 1 and current_sec == 1) or \
                        (current_min == relay_entity.get_second_minute() - 1 and current_sec == 1):

                    str_time = strftime('**※ 현재 시각 : %I시 %M분 %S초 %p**\n', current_time)
                    saved_entity = "** ⇒ " + relay_entity.stringify() + "**\n"
                    user_to_mention = "<@{0}>\n".format("> <@".join(self.user_id_list)) if len(self.user_id_list) > 0 \
                        else ""
                    info_str = "(!알림 / !알림삭제)\n"
                    return str_time + saved_entity + user_to_mention + info_str

                # 알릴 시간이 아님. 루프
                else:
                    # print(strftime('[Debug] %I시 %M분 %S초 %p\n', current_time))
                    continue

            return ""

    # 멘션할 유저 추가/삭제/반환
    def add_user(self, user_id):
        self.user_id_list.append(user_id)
        self.user_id_list = list(set(self.user_id_list))

    def delete_user(self, user_id):
        if user_id not in self.user_id_list:
            return
        else:
            self.user_id_list.remove(user_id)

    def get_user(self):
        return self.user_id_list
