import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.getenv('MTA4NTU0OTczNTU0NjQ1ODE1Mg.GBO35l.chw8lKRfY_36sOF4leW3Jy12kyXsXHtuz2o4iQ'))