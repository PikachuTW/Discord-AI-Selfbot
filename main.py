import json
import discord
import os
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

from dotenv import load_dotenv
load_dotenv()

# config
channelList = [ 948178858610405426 ]

with open('setting.json', 'r') as f:
    setting = json.load(f)

if 'users' not in setting:
    setting['users'] = []

with open('prompt.txt', 'r') as f:
    prompt = f.read()

client = discord.Client()
cookies = json.loads(open("./bing_cookies.json", encoding="utf-8").read())

@client.event
async def on_ready():
    print(f"{client.user} is ready")

@client.event
async def on_message(message):
    success = False
    if message.author.bot or message.channel.id not in channelList or message.content == "" or message.content.startswith("t!") or message.content.startswith("s?") or (client.user and message.author.id == client.user.id):
        return
    if message.content.startswith("l!ping"):
        await message.reply(content=f"ping: {round(client.latency, 1)}")
        return
    if message.content.startswith("l!disable"):
        if(message.author.id not in setting['users']):
            setting['users'].append(message.author.id)
        await message.reply(content=f"我不會再回覆你了 :yum:")
        with open('setting.json', 'w') as f:
            json.dump(setting, f)
        return
    if message.content.startswith("l!enable"):
        if(message.author.id in setting['users']):
            setting['users'].remove(message.author.id)
        await message.reply(content=f"我總是會陪伴著你 :yum:")
        with open('setting.json', 'w') as f:
            json.dump(setting, f)
        return
    if message.author.id in setting['users']:
        return
    
    ask = f"{prompt}\n{message.content}"
    print(f"ask = {message.content}")

    for _ in range(5):
        if success:
            return
        try:   
            chatBot = await Chatbot.create()
            response = await chatBot.ask(prompt=ask, conversation_style=ConversationStyle.creative)
            await chatBot.close()
            print(json.dumps(response, indent=2))
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
        
client.run(f'{os.getenv("DISCORD_TOKEN")}')