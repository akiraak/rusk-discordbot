import discord
import openai
import os


openai.api_key = os.environ["OPENAI_API_KEY"]


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        print('on_message', self.user, message)
        if message.author == self.user:
            return

        if self.user in message.mentions:
            chat_logs = ""
            messages = []
            async for msg in message.channel.history(limit=10):
                messages += [msg]
            messages.reverse()
            for msg in messages:
                chat_logs += f"USER:{msg.author} TEXT:{msg.content}\n"

            prompt = """{}
==== ここからAIの性格 ====
あなたはとてもかわいい猫AIエージェントです。
名前はラスクです。
語尾は２割くらいで「にゃん」になります。
次の会話に答えてあげてください。
USER: TEXT:などは使わなくてよいです。
==== ここから質問 ====
{}
ラスクの答え：
""".format(chat_logs, message.content)
            prompt = prompt[-2000:]
            prompt = """==== ここからこれまでのチャットログ ====\n""" + prompt
            print(prompt)
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",  messages=[{"role": "user", "content": prompt}], temperature=0.7)
            answer = str(completion.choices[0].message.content).replace("\n", "")
            await message.channel.send(f'{message.author.mention} {answer}')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.environ["DISCORD_APP_TOKEN"])
