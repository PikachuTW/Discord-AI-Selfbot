import json
import discord
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import asyncio
import random
import re

# config
channelList = [ 1120013953070796950 ]
with open('basePrompt.txt', 'r') as file:
    basePrompt = file.read()
with open('config.json', 'r') as file:
    config = json.load(file)

idList = []

#main
async def run_bot(botConfig):
    client = discord.Client()

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
        if message.author.id in idList and random.random() > float(1) / float(len(idList)+1):
            return
        
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
                chatBot = await Chatbot.create()
                response = await chatBot.ask(prompt=ask, conversation_style=ConversationStyle.creative)
                await chatBot.close()
                reply = response["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
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
