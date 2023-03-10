import discord
from Controller import *
import asyncio
import sys
from ChatSniffer import *


''' 
<< Token, 채널 ID를 info.txt에서 읽어옴 >>
info.txt 형식 : 

token = [토큰]
relay_channel_id = [릴경 알림용 채널 id]
chat_channel_id = [따라말하기용 채팅채널 id]
'''

info_file = open("info.txt", 'r')
token = info_file.readline().split("=")[1].strip()
relay_channel_id = int(info_file.readline().split("=")[1].strip())
chat_channel_id = int(info_file.readline().split("=")[1].strip())
info_file.close()


client = discord.Client()
c = Controller()
chat_sniffer = None


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global chat_sniffer
    chat_sniffer = ChatSniffer(client)


@client.event
async def on_message(message):

    # 봇 자신의 메시지는 거름
    if message.author == client.user:
        return

    # 종료 : 메시지가 온 채널로 보냄
    if message.content.startswith('!kill'):
        await message.channel.send("종료합니다.")
        sys.exit("종료합니다.")


    # 파싱 결과를 "특정 채널 (채팅채널)" 로 전송
    # 채팅용 특정 채널 명시 필요하므로 따로 처리
    elif message.content.startswith('!echo'):
        res_msg = c.parse(message)
        if res_msg == "" or res_msg is None:
            return
        chat_channel = client.get_channel(chat_channel_id)
        await chat_channel.send(res_msg)

    # Fetch mode ON/OFF
    elif message.content.startswith('!fetch'):
        mode = str(chat_sniffer.toggle())
        await message.channel.send(mode)


    # 파싱 결과를 "메시지가 온 채널"로 전송 (릴경명령 등 일반적인 명령)
    # 명령어가 아닌 경우는 Controller 에서 걸러져 공백 스트링이 리턴됨
    # 공백 스트링이 리턴될 경우 아무것도 하지 않음
    else:
        # Test : 채팅복사, 채팅보내기
        if chat_sniffer.fetch_mode:
            await chat_sniffer.send_to_my_channel(message)
            await chat_sniffer.message_autosend(message, chat_channel_id)
        #################

        res_msg = c.parse(message)
        if res_msg == "" or res_msg is None:
            return

        await message.channel.send(res_msg)



# 현재 시각에 따라 알림 or 빈 스트링 받아와서 결과를 걸러 보냄 (loop)
# 알림을 보낼, 릴경용 특정 채널 명시 필요
async def relay_exp_alert_bg():
    await client.wait_until_ready()
    while not client.is_closed():
        res_msg = c.relay_exp_notify()

        # 릴경 항목을 "특정 채널 (릴경채널)" 로 전송 (릴경알림)
        if res_msg != "":   # 시간이 안됐을 경우 빈 문자열 받음
            channel = client.get_channel(relay_channel_id)
            res_msg = "####### 릴경알림 #######\n" + res_msg
            await channel.send(res_msg)     # 메시지 보냄
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(0.01)

'''
async def boss_pattern_alert_bg():
    await client.wait_until_ready()
    while not client.is_closed():
        res_msg = c.boss_pattern_notify()

        # TODO : 릴경채널로 보내도록 임시 설정, 나중에 변경할 것
        if res_msg != "":
            channel = client.get_channel(relay_channel_id)
            await channel.send(res_msg)
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(0.01)
            
client.loop.create_task(boss_pattern_alert_bg())
'''

client.loop.create_task(relay_exp_alert_bg())

client.run(token)