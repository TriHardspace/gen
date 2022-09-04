# main.py
import discord
import os
from discord.ext import commands
import glob
# static variables

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="*", intents=intents, help_command=None)
token = "provide own token"
directory = "./services/"
channelname = "channel name here (no #)"
#Variable channelid is only used for error messages and does not need to be defined properly for gen to function.
channelid = "put your channel id here"
allowed_chars = set('qwertyuiopasdfghjklzxcvbnm')

rules = [False, False]
# cout when bot is connected
@bot.event
async def on_ready():
    print('The fucking shit is connected lmao')

# gen command
@bot.command(name="generate*", aliases=["generate"])
async def generate(ctx, arg):
    if set(arg).issubset(allowed_chars):
            try:

                servicefile = directory + arg + ".txt"
    

                with open(servicefile, "r") as file:
                        first_line = file.readline()
                        print(len(first_line))        
                with open(servicefile, "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    file.truncate()
                    file.writelines(lines[1:])


#check for correct channel name and send message if the output string is length >1
                if len(first_line) >= 2:
                    rules[0] = True
                if ctx.channel.name == (channelname):
                     rules[1] = True

                if all(rules) == True: 
                    await ctx.send(f'Check your DMs!')
                    await ctx.author.send(f'Output is: `{first_line}`')

	        
    

#handle incorrect channelname
                if rules[1] == False:
                    await ctx.send(f'This command only works in <#{channelid}>!')
    
                if rules[0] == False:
                    await ctx.send(f'Service {arg} does not exist or there is no stock.')


#handle no file
            except FileNotFoundError:
                await ctx.send(f'Service {arg} does not exist, or there was a filesystem error.')
    else:
        await ctx.send(f'Invalid Parameters')


#stock command
@bot.command(name="stock*", aliases=["stock"])
async def stock(ctx):
    os.chdir(directory)
    stock={}
    for fn in glob.glob('*.txt'):
        with open(fn) as f:
            stock[fn]=sum(1 for line in f if line.strip())
    print(stock)
    await ctx.send(f'{stock}')
    os.chdir("..")

bot.run(token)
