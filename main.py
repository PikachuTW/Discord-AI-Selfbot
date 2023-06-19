import json
import discord
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import asyncio

# config
channelList = [ 948178858610405426, 1120013953070796950 ]
with open('basePrompt.txt', 'r') as file:
    basePrompt = file.read()
with open('config.json', 'r') as file:
    config = json.load(file)

#main
async def run_bot(botConfig):
    global shutdown
    shutdown = False
    prefix = botConfig['prefix']
    with open('blacklist.json', 'r') as file:
        blacklist = json.load(file)
    if botConfig['prefix'] not in blacklist:
        blacklist[f'{prefix}'] = []
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is ready')

    @client.event
    async def on_message(message):
        global shutdown
        success = False
        if message.author.bot or message.channel.id not in channelList or message.content == '' or message.content.startswith('t!') or message.content.startswith('s?') or (client.user and message.author.id == client.user.id):
            return
        if message.content.startswith(prefix):
            message.content = message.content[len(prefix):]
            if message.content.startswith('ping'):
                await message.reply(content=f"ping: {round(client.latency, 1)}")
            elif message.content.startswith("enable"):
                if(message.author.id in blacklist[f'{prefix}']):
                    blacklist[f'{prefix}'].remove(message.author.id)
                await message.reply(content=f"我總是會陪伴著你 :yum:")
                with open('blacklist.json', 'w') as f:
                    json.dump(blacklist, f)
            elif message.content.startswith("disable"):
                if(message.author.id not in blacklist[f'{prefix}']):
                    blacklist[f'{prefix}'].append(message.author.id)
                await message.reply(content=f"我不會再回覆你了 :yum:")
                with open('blacklist.json', 'w') as f:
                    json.dump(blacklist, f)
            elif message.content.startswith("shutdown"):
                if(message.author.id == 650604337000742934):
                    await message.reply(content=f"我要去睡覺了 :sleeping:")
                    shutdown = True
                else:
                    await message.reply(content=f"你沒有權限 :yum:")
            elif message.content.startswith("wakeup"):
                if(message.author.id == 650604337000742934):
                    await message.reply(content=f"你好! 我回來了 :smile:")
                    shutdown = False
                else:
                    await message.reply(content=f"你沒有權限 :yum:")
            return
        if message.channel.id == channelList[0]:
            if message.author.id in blacklist[f'{prefix}'] or shutdown:
                return
        
        ask = f"{botConfig['prompt']}\n\n{basePrompt}\n{message.content}"
        print(f"ask = {message.content}")

        for _ in range(15): # try 15 times
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

    await client.start(botConfig['token'])

loop = asyncio.get_event_loop()

for botConfig in config['botList']:
    loop.create_task(run_bot(botConfig))

loop.run_forever()
