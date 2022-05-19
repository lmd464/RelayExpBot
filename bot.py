import discord
from Controller import *
import asyncio
import sys



# Token, 채널 ID, 멘션할 역할 ID를 info.txt에서 읽어옴
''' 
info.txt 형식 : 
token = [토큰]
channel_id = [채널 id]
role_id = [역할 id]
'''
info_file = open("info.txt", 'r')
token = info_file.readline().split("=")[1].strip()
channel_id = int(info_file.readline().split("=")[1].strip())
role_id = int(info_file.readline().split("=")[1].strip())
info_file.close()


client = discord.Client()
c = Controller()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        if message.content.startswith('!kill'):
            await message.channel.send("종료합니다.")
            sys.exit("종료합니다.")

        res_msg = c.input(message.content)

        # 공백 스트링이 리턴될 경우 에러로 간주
        if res_msg == "":
            return

        await message.channel.send(res_msg)


# 릴경 시간 1분 전 알리는 기능
async def alert_bg():
    await client.wait_until_ready()
    while not client.is_closed():
        res_msg = c.notify()

        if res_msg != "":
            channel = client.get_channel(channel_id)
            res_msg = "<@&" + str(role_id) + ">\n" + res_msg  # 역할 멘션
            await channel.send(res_msg)     # 메시지 보냄
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(0.01)


client.loop.create_task(alert_bg())
client.run(token)
