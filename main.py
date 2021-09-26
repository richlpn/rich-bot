import discord
from os import getenv
from importlib import reload
import functions
from keep_alive import keep_alive
client = discord.Client()
Func = functions.Functions(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
@client.event
async def on_message(msg):
    global Func
    command = None
    try:
        if(msg.content.startswith('!update')) :
            cargo = False
            for role in msg.author.roles:
                if 'ADM' == role.name:
                    Func=reload(functions).Functions(client)
                    await msg.channel.send('comandos atualizados')
            if not cargo :
                await msg.channel.send('Você não possui um cargo alto o suficiente para usar esse comando')
        elif not (msg.author == client.user):
            if msg.content.startswith("!") and msg.channel.id not in Func.black_list_channel:
                command = Func.get_command(msg.content.split(" ")[0])
            if command != False and command != None:
                await command(msg)
        elif msg.content.startswith('!') and msg.channel.id in Func.black_list_channel:
            await msg.channel.send('comandos não são validos nesse canal')
    except Exception as err:
        await msg.channel.send(f'Erro: {err}')
        print(f'Erro: {err}')
keep_alive()
client.run(getenv('TOKEN'))