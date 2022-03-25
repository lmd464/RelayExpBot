from RelayEntity import *


class Timer:

    def __init__(self):
        self.relay_list = []

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


    # 저장된 시간의 1분 전이 되면 알린다.
    # 현재 시간을 인자로 받고, Relay List에 있는 Entity들을 탐색하며
    # 알려야 하는 요소가 있으면 저장된 시간에 대한 String 반환
    # 없으면 빈 문자열 반환
    def notify(self, current_min, current_sec):

        if len(self.relay_list) == 0:
            return ""
        else:
            for relay_entity in self.relay_list:

                # 첫 시간이 00분일 때 1분 전
                if current_min == 59 and relay_entity.get_first_minute() == 0 and current_sec == 1:
                    return "** ⇒ " + relay_entity.stringify() + "**\n"
                # 첫번째 시간의 1분 전
                elif current_min == relay_entity.get_first_minute() - 1 and current_sec == 1:
                    return "** ⇒ " + relay_entity.stringify() + "**\n"
                # 두번째 시간의 1분 전
                elif current_min == relay_entity.get_second_minute() - 1 and current_sec == 1:
                    return "** ⇒ " + relay_entity.stringify() + "**\n"
                else:
                    continue
            return ""
