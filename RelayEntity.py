class RelayEntity:
    def __init__(self, channel, first_minute, second_minute):
        self.channel = channel
        self.first_minute = first_minute
        self.second_minute = second_minute

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


