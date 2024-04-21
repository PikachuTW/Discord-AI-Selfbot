import json
import discord
from sydney import SydneyClient
import asyncio
import random
import re
import os

# config
channelList = [ 1120013953070796950 ]
with open('basePrompt.txt', 'r', encoding="utf-8") as file:
    basePrompt = file.read()
with open('config.json', 'r', encoding="utf-8") as file:
    config = json.load(file)
os.environ["BING_COOKIES"] = config['bingCookies']

idList = []

#main
async def run_bot(botConfig):
    client = discord.Client()
    sydney = SydneyClient()
    await sydney.start_conversation()

    @client.event
    async def on_ready():
        print(f'{client.user} is ready')
        if(client.user):
            idList.append(client.user.id)
            print(idList)

    @client.event
    async def on_message(message):
        success = False
        if message.author.bot or message.channel.id not in channelList or message.content == '' or message.content.startswith('t!') or message.content.startswith('s?') or (client.user and message.author.id == client.user.id):
            return
        if message.author.id in idList:
            return  # if you want the bot reply to other bots, remove this line
        
        pattern = re.compile(r'<@(\d+)>')
        matches = pattern.findall(message.content)
        for match in matches:
            user = await message.guild.fetch_member(match)
            if user == None:
                user = await client.fetch_user(match)
            if user:
                message.content = message.content.replace(f'<@{match}>', user.display_name)
        
        ask = f"{botConfig['prompt']}\n\n{basePrompt}\n{message.content}"
        print(f"ask = {message.content}")

        for _ in range(15):
            if success:
                return
            try:
                reply = await sydney.ask(ask, citations=True)
                if "sorry" in reply or "Sorry" in reply or "try" in reply or "mistake" in reply:
                    print("Failed")
                    return
                print("reply = " + reply)
                success = True
                await message.reply(content=reply)
            except Exception as error:
                print(f"Error {error}")
                return

    await client.start(botConfig['token'])

loop = asyncio.get_event_loop()

for botConfig in config['botList']:
    loop.create_task(run_bot(botConfig))

loop.run_forever()
