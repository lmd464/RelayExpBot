# Test_ChatCopy

class ChatSniffer:

    def __init__(self, client):
        self.client = client
        self.my_fetch_channel_id = 1068063085782380626  # 채팅 저장소
        self.my_fetch_channel = self.client.get_channel(self.my_fetch_channel_id)
        self.fetch_mode = False

    # 모든 채널에 대한 채팅을 my_fetch_channel 로 송출
    async def send_to_my_channel(self, message):
        if message.channel.id != self.my_fetch_channel_id:
            server_nick = 'None' if message.author.nick is None else message.author.nick
            await self.my_fetch_channel.send(message.guild.name + "(" +
                                             message.channel.name + ") ~ " +
                                             server_nick + "[" +
                                             message.author.name + "#" +
                                             message.author.discriminator + "] : " +
                                             message.content)

    # 채팅채널 fetch한 채널에 메시지 쓰면 그대로 전달 (자동 echo)
    async def message_autosend(self, message, chat_channel_id):
        if message.channel.id == self.my_fetch_channel_id:
            chat_channel = self.client.get_channel(chat_channel_id)
            await chat_channel.send(message.content)

    def toggle(self):
        self.fetch_mode = not self.fetch_mode
        return self.fetch_mode
