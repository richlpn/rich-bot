from random import randint
from replit import db
class Functions():
    def __init__(self,client):
        self.commands = {
            '!addQ':self.addQ,
            '!pesquisar':self.pesquisar,
            '!corno':self.corno,
            '!opa':self.opa,
            '!pontos':self.get_pontos,
            '!add_pontos':self.add_pontos,
            '!jokenpo':self.jokenpo
        }
        self.client = client
        self.black_list_channel = [763495584925352013]
    def get_command(self,command):
        if command in self.commands:
            return self.commands[command]
        else: return False
    async def corno(self,msg):
        if len(msg.mentions)>0:
            player = msg.mentions[0].mention
        else:player = msg.author.mention
        await msg.channel.send(f'{player} já foi corno {randint(0,100)} vezes !!!')
    async def opa(self,msg):
        if len(msg.mentions)>0:
            player = msg.mentions[0].mention
        else:player = msg.author.mention
        await msg.channel.send(f"opá bom {player}?")
    
    async def get_pontos(self,msg,id = None):
        if id == None:
            if len(msg.mentions)>0:
                id = str(msg.mentions[0].id)
                author = msg.mentions[0]
            else:
                author = msg.author
                id = str(msg.author.id)
        if id not in db.keys():
            db[id]={'money': 100}
            await msg.channel.send(f'{author.mention} tem {db[id]["money"]} pontos!!')
        else:
            await msg.channel.send(f'{author.mention} tem {db.get(id)["money"]} pontos!!')

    async def add_pontos(self,msg,id = None,cont = None,author = None):
        if id == None and cont == None and author==None:
            if len(msg.mentions)>0:
                id = str(msg.mentions[0].id)
                cont = int(msg.content.split(" ")[2])
                author = msg.mentions[0]
            else:
                id = str(msg.author.id)
                cont = int(msg.content.split(" ")[1])
                author = msg.author
        if id in db.keys():
            Dt = db.get(id) 
            Dt['money'] += cont
            db[id] = Dt
            await msg.channel.send(f'{author.mention} possui {db.get(id)["money"]} pontos')
        else:db[id]={'money': 100}

    async def addQ(self,msg):
        msgL = msg.content.split(" ")[1:]
        if msgL[0] not in db or msgL[1] not in db[msgL[0]]:
            db[msgL[0]] = {msgL[1]:{msgL[2]:msg.id}}
        else:
            if msgL[1] in db[msgL[0]] and msgL[2] not in db[msgL[0]][msgL[1]]:
                db[msgL[0]][msgL[1]] = {msgL[2]:msg.id}
            else:
                await msg.channel.send('questão ja existe')
    async def pesquisar(self,msg):
        print(len(msg.content.split()))
        if len(msg.content.split(" ")[1:]) == 1:
            mate = msg.content.split(" ")[0]
            if mate in db:
                print(db[mate])
                await msg.channel.send(db[mate])
            else:
                print('materia n existe')
                print(db.keys())
        elif len(msg.content.split(" ")[1:]) == 2:
            mate,questionario = msg.content.split(" ")[1:]
            if mate in db:
                if questionario in db[mate]:
                    print(db[mate][questionario])
                    txt = ''
                    for i in db[mate][questionario].keys():
                        txt = f'{txt}\n{i}'
                    await msg.channel.send(txt)
                else:print('questionario n existe')
        elif len(msg.content.split(" ")[1:]) == 3:
            mate,questionario,quest = msg.content.split(" ")[1:]
            if mate in db:
                if questionario in db[mate]:
                    if quest in db[mate][questionario]:
                        await msg.channel.send(db[mate][questionario][quest])
    async def jokenpo(self,msg):
            self.count = 1
            self.choice1 = None
            self.choice2  = None
            self.t = 5
            if len(msg.content.split(" "))>=3:
                try:
                    self.bet = int(msg.content.split(" ")[2])
                except:
                    await msg.channel.send('aposta inválida')
            else:
                self.bet = None
            #-------------------------check()------------------------#
            def check(reaction,user):
                if self.player2 != self.client.user:
                    if user==self.player2 :
                        if reaction.emoji == ("✅") :
                            self.count += 1
                            self.emote2=reaction.emoji
                        elif reaction.emoji == ("❌")  :
                            self.count -= 1
                            self.emote2=reaction.emoji
                        return True
                return False
            #-------------------------check()------------------------#
            def check2(reaction,user):
                if user == self.player1:
                    self.choice1 = reaction.emoji
                elif user == self.player2:
                    self.choice2 =  reaction.emoji
                elif self.t == 0: return True
                return (self.choice1 !=None and self.choice2 != None)
            #-------------------------check()------------------------#
            if len(msg.mentions)>0:
                    self.player1 = msg.author
                    self.player2 = msg.mentions[0]
                    self.emote1 ='✅'
                    self.emote2 ='<:monkaS:817178725229133865> '
                    text = f'jokenpo!!!\n{self.player1.mention} {self.emote1} \nVS\n{self.player2.mention} {self.emote2}'
                    answer = await msg.channel.send(text)
                    if self.player2 == self.client.user:
                        await answer.channel.send('player indisponível !!!')
                    else:
                        await answer.add_reaction("✅")
                        await answer.add_reaction("❌")
                        if self.count != 2:
                            try:
                                await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                                await answer.clear_reactions()
                            except TimeoutError:
                                await answer.channel.send('Tempo acabou')
                            text = f'jokenpo!!!\n{self.player1.mention} {self.emote1} \n   VS\n{self.player2.mention} {self.emote2}'
                            await answer.edit(content =text)
                        if self.count ==2:
                            await answer.add_reaction("🪨")
                            await answer.add_reaction("✂️")
                            await answer.add_reaction("🧻")
                            answer = await answer.channel.send(f'COMEÇANDO EM: {self.t}')
                            while self.t >= 0:
                                if self.choice1 == None or self.choice2 == None:
                                    try:
                                        await self.client.wait_for('reaction_add',timeout=1.0,check=check2)
                                    except:
                                        pass
                                else:
                                    self.t = 0 
                                    await answer.edit(content=f'COMEÇANDO EM: {self.t}')
                                    break 
                                if self.t > 0:
                                    self.t-= 1
                                    await answer.edit(content=f'COMEÇANDO EM: {self.t}')
                            if True:
                                if self.choice1 != None and self.choice2 != None:
                                    if self.choice1 == '🧻':
                                        if self.choice2 =='✂️':
                                            winner = self.player2
                                            loser = self.player1
                                        elif self.choice2 == '🪨':
                                            winner = self.player1
                                            loser = self.player2
                                        else: winner = 'empate'                 
                                    elif self.choice1 == '✂️':
                                        if self.choice2 == '🧻':
                                            winner = self.player1
                                            loser = self.player2
                                        elif self.choice2 == '🪨':
                                            winner = self.player2
                                            loser = self.player1
                                        else: winner = 'empate'
                                    elif self.choice1 == '🪨':
                                        if self.choice2 == '🧻':
                                            winner = self.player2
                                            loser = self.player1
                                        elif self.choice2 == '🪨':
                                            winner = 'empate'
                                        else: 
                                            winner = self.player1
                                            loser = self.player2
                                    cond = True 
                                else:
                                    cond  = False
                                if cond and winner != 'empate':
                                    await answer.edit(content =f'{winner.mention} venceu!!!')
                                    await self.add_pontos(answer,str(winner.id),self.bet,winner)
                                    await self.add_pontos(answer,str(loser.id),-self.bet,loser)
                                elif winner == "empate":
                                    await answer.edit(content ='empate!!!')
                                else:
                                    await answer.edit(content ='alguem não escolheu a tempo')