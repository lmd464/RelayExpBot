# Test_ChatCopy

class ChatSniffer:

    def __init__(self, client):
        self.client = client
        self.my_channel = self.client.get_channel(1068063085782380626)

    async def send_to_my_channel(self, message):
        await self.my_channel.send(message.guild.name + "_" +
                                   message.channel.name + " - " +
                                   message.author.name + " : " +
                                   message.content)
