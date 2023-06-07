from nextcord.ext import commands
import nextcord
import os

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

@bot.event
async def on_ready():
    print('Bot się odpalił')
    await bot.change_presence(activity=nextcord.Game(name='Jedyna taka gra'))


bot.run('TOKEN')
