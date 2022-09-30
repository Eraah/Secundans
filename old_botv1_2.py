import discord
import asyncio
import random
keys_file = open('keys.txt', 'r')
keys = keys_file.readlines()
keys_file.close()
token = keys[0]

class MyClient(discord.Client):
    available = 1
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print(discord.__version__)

    async def on_message(self, message):

        if message.author.id == self.user.id:
            return

        if message.content.startswith('!вызов') and self.available == 1:
            self.available = 0
            duel = 0
            enemycheck = 0
            participant1 = message.author
            for member in message.guild.members:
                if str(member.id) == str(message.content)[10:-1]:
                    await message.channel.send("Ты в игре, ждем твоего противника.")
                    await asyncio.sleep(0.5)
                    await message.channel.send('{0.mention}, Ты принимаешь вызов?'.format(member))
                    enemy = member
                    enemycheck = 1
            if enemycheck != 1:
                await message.channel.send("Просто пингануть человека и не задеть лишних клавиш не судьба, да?", delete_after=2.5)
                await message.delete()
                self.available = 1
                return
            if enemy == self.user:
                await message.channel.send('!принимаю')
                participant2 = self.user
                duel = 1
                await message.channel.send('Участники дуэли ' + str(participant1) + ' и ' + str(participant2) + ' готовы')
            else:
                while duel == 0:
                    try:
                        participation = await self.wait_for('message', timeout=10)
                        if str(participation.content) == '!принимаю' and participation.author == enemy:
                            participant2 = participation.author
                            duel = 1
                            await message.channel.send('Участники дуэли '+ str(participant1) + ' и ' + str(participant2) + ' готовы')
                    except asyncio.TimeoutError:
                        self.available = 1
                        print(self.available)
                        duel = 2
                        return await message.channel.send('{0.mention} зассал выйти раз на раз.'.format(enemy))

            if duel == 1:
                await message.channel.send("Дуэль начнется через")
                for i in range(5, 0, -1):
                    await asyncio.sleep(1)
                    await message.channel.send(str(i))
                await message.channel.send("Да начнется смертоубийство! :gun:")
                while duel == 1:
                    try:
                        shoot = await self.wait_for('message', timeout=10)
                        if str(shoot.content) == '!выстрел' and shoot.author == participant1:
                            if participant2 == self.user:
                                await message.channel.send('Пуля рикошетит от стальной головы ' + participant2.mention + ' прямо в лицо тупого кожанного мешка  ' + participant1.mention + '!! Как ему вообще пришло в голову играть с безупречной машиной?!')
                                duel = 0
                                self.available = 1
                                role = discord.utils.get(message.guild.roles, name='убит')
                                await participant1.add_roles(role)
                                return
                            await message.channel.send('Голова ' + participant2.mention + ' разлетается на куски! Отличный выстрел ' + participant1.mention + ' !')
                            role = discord.utils.get(message.guild.roles, name='убит')
                            await participant2.add_roles(role)
                            duel = 0
                            self.available = 1
                            return
                        elif str(shoot.content) == '!выстрел' and shoot.author == participant2:
                            await message.channel.send('Голова ' + participant1.mention + ' разлетается на куски! Отличный выстрел ' + participant2.mention + ' !')
                            role = discord.utils.get(message.guild.roles, name='убит')
                            await participant1.add_roles(role)
                            duel = 0
                            self.available = 1
                            return
                    except asyncio.TimeoutError:
                        if participant2 != self.user:
                            await message.channel.send('Какие-то миролюбивые дуэльянты, я таких терпеть не могу.')
                            role = discord.utils.get(message.guild.roles, name='убит')
                            r = random.random()
                            if r > 0.5:
                                print(r)
                                await participant1.add_roles(role)
                                await message.channel.send('Голова ' + participant1.mention + ' разлетается на куски! Отличный выстрел ' + self.user.mention + '!')
                            else:
                                print(r)
                                await participant2.add_roles(role)
                                await message.channel.send('Голова ' + participant2.mention + ' разлетается на куски! Отличный выстрел ' + self.user.mention + '!')
                        else:
                            await message.channel.send('А я хотел дать тебе шанс...')
                            await message.channel.send('!выстрел')
                            role = discord.utils.get(message.guild.roles, name='убит')
                            await participant1.add_roles(role)
                            await message.channel.send('Голова ' + participant1.mention + ' разлетается на куски! Отличный выстрел ' + self.user.mention + '!')
                        duel = 0
                        self.available = 1
                        return
            self.available = 1
            return

client = MyClient()
client.run(token)
