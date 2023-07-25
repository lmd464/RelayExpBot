from RelayEntity import *
from time import *


class RelayExpTimer:

    def __init__(self):
        self.relay_list = []
        self.relay_chat_channel_id = -1  # 알림 채널 설정

    # RelayEntity의 Getter
    def get_relay_entity(self, num):
        return self.relay_list[num - 1]
    def get_relay_chat_channel(self):
        return self.relay_chat_channel_id
    def set_relay_chat_channel(self, relay_chat_channel_id):
        self.relay_chat_channel_id = int(relay_chat_channel_id)





    # 등록 : !등록 [채널] [분1]/[분2]
    # 시간 순서대로 정렬시킴
    # 인덱스에 의한 순번 자동 부여
    def register(self, channel, first_minute, second_minute):
        relay_entity = RelayEntity(channel, first_minute, second_minute)
        self.relay_list.append(relay_entity)

        # 정렬
        self.relay_list = sorted(self.relay_list, key=lambda entity: entity.first_minute)

        return "등록 완료 되었습니다.\n"

    # 삭제 : !삭제 [번호]
    def delete(self, number):
        if len(self.relay_list) == 0:
            return "삭제할 항목이 없습니다.\n"
        deleted_entity = self.relay_list.pop(number - 1)
        return "삭제 완료되었습니다.\n"

    # 전체삭제 : !전체삭제
    def delete_all(self):
        if len(self.relay_list) == 0:
            return "삭제할 항목이 없습니다.\n"
        self.relay_list.clear()
        return "전체 삭제 완료되었습니다.\n"

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
            return "저장된 정보가 없습니다.\n"


    # 현재 시간이 저장된 시간의 1분 전이라면 해당 정보 스트링을 반환한다.
    # 현재 시간(분, 초) 을 구하고, Relay List 에 있는 Entity 들을 탐색하며
    # 알려야 하는 요소가 있으면 현재 시간과 저장된 시간에 대한 String 반환
    # 없으면 빈 문자열 반환
    def notify(self):
        current_time = localtime()
        current_min = current_time.tm_min
        current_sec = current_time.tm_sec

        # 알릴 정보가 없거나, 채널이 설정되지 않은 상태 :
        if len(self.relay_list) == 0 or self.relay_chat_channel_id == -1:
            return ""

        # 알릴 정보가 있고, 채널이 설정된 상태
        else:
            header = "**----------[ 릴경알림 ]----------**\n"
            footer = "**-------------------------------**\n"

            str_time = strftime('**※ 현재 시각 : %I시 %M분 %S초 %p**\n', current_time)
            concat = header + str_time
            have_to_notify = False

            for relay_entity in self.relay_list:

                # 첫 시간이 00분일 때 1분 전 / # 첫번째 시간의 1분 전 /  # 두번째 시간의 1분 전
                if (current_min == 59 and relay_entity.get_first_minute() == 0 and current_sec == 1) or \
                        (current_min == relay_entity.get_first_minute() - 1 and current_sec == 1) or \
                        (current_min == relay_entity.get_second_minute() - 1 and current_sec == 1):

                    saved_entity = "** ⇒ " + relay_entity.stringify() + "**\n"
                    user_to_mention = "<@{0}>\n".format("> <@".join(relay_entity.get_user())) \
                        if len(relay_entity.get_user()) > 0 else ""

                    concat += saved_entity + user_to_mention
                    have_to_notify = True
                    continue

                # 알릴 시간이 아님. 루프
                else:
                    # print(strftime('[Debug] %I시 %M분 %S초 %p\n', current_time))
                    continue

            res = concat + footer if have_to_notify else ""
            return res

    # 멘션할 유저 추가 : 선택한 채널의 RelayEntity 에서 수행
    def add_user(self, user_id, alert_num):
        self.relay_list[alert_num - 1].add_user(user_id)

    # 멘션할 유저 삭제 : RelayExpTimer의 모든 Entity들 탐색하며 수행
    def delete_user(self, user_id):
        for entity in self.relay_list:
            entity.delete_user(user_id)

