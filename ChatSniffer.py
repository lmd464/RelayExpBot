# Test_ChatCopy

class ChatSniffer:

    def __init__(self, client):
        self.client = client
        self.my_fetch_channel_id = 1068063085782380626
        self.my_fetch_channel = self.client.get_channel(self.my_fetch_channel_id)

    async def send_to_my_channel(self, message):
        await self.my_fetch_channel.send(message.guild.name + "(" +
                                         message.channel.name + ") ~ " +
                                         message.author.name + "#" +
                                         message.author.discriminator + " : " +
                                         message.content)

    async def message_autosend(self, message, chat_channel_id):
        if message.channel.id == self.my_fetch_channel_id:
            chat_channel = self.client.get_channel(chat_channel_id)
            await chat_channel.send(message.content)