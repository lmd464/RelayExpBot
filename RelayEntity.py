class RelayEntity:
    def __init__(self, channel, first_minute, second_minute):
        self.channel = channel
        self.first_minute = first_minute
        self.second_minute = second_minute
        self.user_id_list = []  # 멘션으로 알릴 유저 리스트

    def stringify(self):
        string = str(self.channel) + "ch " + \
                 str(self.first_minute) + "분, " + \
                 str(self.second_minute) + "분"
        return string

    def get_channel(self):
        return self.channel

    def get_first_minute(self):
        return self.first_minute

    def get_second_minute(self):
        return self.second_minute



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





