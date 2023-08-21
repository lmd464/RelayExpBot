import discord
from discord.ext import tasks
from Controller import *
import asyncio
import sys
from random import randint

''' 
<< Token, 채널 ID를 info.txt에서 읽어옴 >>
info.txt 형식 : 

token = [토큰]
'''

info_file = open("info.txt", 'r')
token = info_file.readline().split("=")[1].strip()
info_file.close()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
c = Controller()

wrapper_h = "```\n"
wrapper_f = "```"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    relay_exp_alert_bg.start()


@client.event
async def on_message(message):

    # 봇 자신의 메시지는 거름
    if message.author == client.user:
        return

    # 종료 : 메시지가 온 채널로 보냄
    if message.content.startswith('!kill'):
        await message.channel.send(wrapper_h + "종료합니다." + wrapper_f)
        sys.exit("종료합니다.")

    # vs
    elif " vs " in message.content:
        choice_list = message.content.split(" vs ")
        if len(choice_list) >= 2:
            res_msg = wrapper_h + choice_list[randint(0, len(choice_list) - 1)] + wrapper_f
            await message.channel.send(res_msg)


    # 파싱 결과를 "메시지가 온 채널"로 전송 (릴경명령 등 일반적인 명령)
    # 명령어가 아닌 경우는 Controller 에서 걸러져 공백 스트링이 리턴됨
    # 공백 스트링이 리턴될 경우 아무것도 하지 않음
    elif message.content.startswith('!'):
        res_msg = c.parse(message)
        if res_msg == "" or res_msg is None:
            return
        res_msg = wrapper_h + res_msg + wrapper_f

        dummy = wrapper_h + wrapper_f

        # 링크를 표시할 경우, 이를 wrapper에서 분리하기 위해 생긴 꼬투리를 제거 (```\n```)
        res_msg = res_msg if dummy not in res_msg else res_msg.split(dummy)[0]
        await message.channel.send(res_msg)



# 현재 시각에 따라 알림 or 빈 스트링 받아와서 결과를 걸러 보냄 (loop)
# 알림을 보낼, 릴경용 특정 채널 명시 필요
@tasks.loop(seconds=0.5)
async def relay_exp_alert_bg():
    await client.wait_until_ready()
    while not client.is_closed():
        res_msg = c.relay_exp_notify()

        # 릴경 항목을 "특정 채널 (채팅채널)" 로 전송 (릴경알림)
        if res_msg != "":
            channel = client.get_channel(c.get_relay_chat_channel())
            await channel.send(">>> " + res_msg)     # 메시지 보냄 (>>> : 강조 마크업)
            await asyncio.sleep(1)

        # 시간이 안됐을 경우 빈 문자열 받음, 알림X
        else:
            await asyncio.sleep(0.01)


@tasks.loop(seconds=60)
async def delete_outdated():
    await client.wait_until_ready()

    while not client.is_closed():
        channel = client.get_channel(c.get_relay_chat_channel())        # 릴경채널 받아옴

        # 등록된 리스트 받아와서 16시간 이상 지난 항목들 자동 제거
        current_list = c.relay_exp_timer.get_relay_list()
        for ent in current_list:

            elapsed_time = ent.get_elapsed_num()      # 경과 시간
            if elapsed_time >= 960:
                current_list.remove(ent)
                await channel.send(wrapper_h + "[!] 16시간 이상 경과된 항목들을 자동으로 삭제하였습니다.\n" + wrapper_f)


client.run(token)
