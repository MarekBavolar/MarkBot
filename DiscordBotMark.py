import discord
import random
import os
import datetime
import pytz
from discord.ext import commands, tasks

TOKEN = "MTA0NjEzMTc3MjA0OTYwODgzOQ.G3ZBwt.l0tvzxra8R4IpliSTkSLDK2BqMPVvdVl-RBCLQ"

events = []
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$',intents=intents)
set_bool = False

class Set_Event:
    def __init__(name, day, hour, minute, count):
        self.name = name
        self.day = day
        self.hour = hour
        self.minute = minute
        self.count = count
    def alarm(now):
        if now.day == self.day:
            if (now.hour)+1 == self.hour:
                self.count -= 1
                return True
        
        return False
    

@client.event
async def on_ready():
  print("Not banned yet!")

@bot.listen()
async def on_ready():
    task_loop.start() # important to start the loop

@tasks.loop(seconds=30)
async def task_loop():
  event_route = client.get_channel(1046133681623937075)
  now = datetime.datetime.now(pytz.timezone('Europe/Bratislava'))
  for event in events:
      if event.alarm(now) == True:
          await event_route.send("<@&1046574440818950246>")



@client.event
async def on_message(message):
  username = str(message.author).split("#")[0]
  user_message = str(message.content)
  channel_name = str(message.channel.name)
  #print(f"{username}: {user_message} ({channel_name})")
  if message.author == client.user:
    return
  #TOMAN 
  if (message.channel == client.get_channel(946581836497317899)) or (message.channel == client.get_channel(1046133681623937075)):
    if user_message.lower() == '!roulette':
      list = ["Red","Black","Green"]
      response = random.choices(list, weights = [4, 4, 2], k = 1)[0]
      await message.channel.send(f'{response}!')
      return
    elif user_message.lower() == "!react":
      emoji = client.get_emoji(1046195643594575972)
      await message.add_reaction(emoji)
      await message.channel.send(f'{emoji}') 
      return
    elif user_message.lower() == "!sus":
      await message.channel.send(file=discord.File('DiscordBotMark\Memes/sus.png'))
      return
    elif user_message.lower() == "<@1046131772049608839>":
      await message.channel.send(file=discord.File('DiscordBotMark\Memes/mark.jpg'))
      return
    elif "yoda" in user_message.lower().split(" "):
      await message.channel.send(file=discord.File('DiscordBotMark\Memes/yoda_sip.gif'))
      await message.channel.send("indeed")
      return 
    elif user_message.lower() == "!getshanked":
      await message.channel.send(file=discord.File('DiscordBotMark\Memes/shank_stab.gif'))
      return
  elif (message.channel == client.get_channel(959554685528858654)) or (message.channel == client.get_channel(1046237995134615582)):
      if user_message.lower() == "!sauce":
        random_file = random.choice(os.listdir("DiscordBotMark\Sauce"))
        source_file="%s\%s"%("DiscordBotMark\Sauce",random_file)
        await message.channel.send(file=discord.File(source_file))
        return
  elif (message.channel == client.get_channel(1046547800575443034)) or (message.channel == client.get_channel(1046519554119057569)):
      if message.channel == client.get_channel(1046519554119057569):  
         route = client.get_channel(1046132801390522420)
      elif message.channel == client.get_channel(1046547800575443034):
         route = client.get_channel(929118971272237087)
      time = "Not Set"
      date = "Not Set"
      opponent = "None"
      max_players = "0"
      if user_message.lower().split(" ")[0] == "!pccp":
         await route.send("<@&935030804063588413>")
         embedVar = discord.Embed(title="Clan Battle", description="<@&935030804063588413> \n{}".format("If u can play please contact your <@&935246053928730664> or <@&954389304073924630>"), color=0xa902c9)
         if len(user_message.lower().split(" ")) >= 2:
            time = "{} {}".format(user_message.lower().split(" ")[1].split("-")[0],user_message.lower().split(" ")[1].split("-")[1])
            if len(user_message.lower().split(" ")) >= 3: 
                date = "{}".format(user_message.lower().split(" ")[2])
                if len(user_message.lower().split(" ")) >= 4:
                    opponent = "{}".format(user_message.split(" ")[3])                  
                    if len(user_message.lower().split(" ")) >= 5:
                        max_players = "{}".format(user_message.split(" ")[4])
         embedVar.add_field(name="Time", value= time, inline=False)
         embedVar.add_field(name="Date", value= date, inline=False)
         embedVar.add_field(name="Opponent", value= opponent, inline=False)
         embedVar.add_field(name="Max players", value= max_players, inline=False)
         await route.send(embed=embedVar)
         return
      if user_message.lower().split(" ")[0] == "!pscp":
         await route.send("<@&935030376752095272>")
         embedVar = discord.Embed(title="Clan Battle", description="<@&935030376752095272> \n{}".format("If u can play please contact your <@&935246053928730664> or <@&954389304073924630>"), color=0x068bff)
         if len(user_message.lower().split(" ")) >= 2:
            time = "{} {}".format(user_message.lower().split(" ")[1].split("-")[0],user_message.lower().split(" ")[1].split("-")[1])
            if len(user_message.lower().split(" ")) >= 3: 
                date = "{}".format(user_message.lower().split(" ")[2])
                if len(user_message.lower().split(" ")) >= 4:
                    opponent = "{}".format(user_message.split(" ")[3])                  
                    if len(user_message.lower().split(" ")) >= 5:
                        max_players = "{}".format(user_message.split(" ")[4])
         embedVar.add_field(name="Time", value= time, inline=False)
         embedVar.add_field(name="Date", value= date, inline=False)
         embedVar.add_field(name="Opponent", value= opponent, inline=False)
         embedVar.add_field(name="Max players", value= max_players, inline=False)
         await route.send(embed=embedVar)
         return
      if user_message.lower().split(" ")[0] == "!xboxcp":
         await route.send("<@&935030608650993674>")
         embedVar = discord.Embed(title="Clan Battle", description="<@&935030608650993674> \n{}".format("If u can play please contact your <@&935246053928730664> or <@&954389304073924630>"), color=0x04be12)
         if len(user_message.lower().split(" ")) >= 2:
            time = "{} {}".format(user_message.lower().split(" ")[1].split("-")[0],user_message.lower().split(" ")[1].split("-")[1])
            if len(user_message.lower().split(" ")) >= 3: 
                date = "{}".format(user_message.lower().split(" ")[2])
                if len(user_message.lower().split(" ")) >= 4:
                    opponent = "{}".format(user_message.split(" ")[3])                  
                    if len(user_message.lower().split(" ")) >= 5:
                        max_players = "{}".format(user_message.split(" ")[4])
         embedVar.add_field(name="Time", value= time, inline=False)
         embedVar.add_field(name="Date", value= date, inline=False)
         embedVar.add_field(name="Opponent", value= opponent, inline=False)
         embedVar.add_field(name="Max players", value= max_players, inline=False)
         await route.send(embed=embedVar)
         return
      if user_message.lower().split(" ")[0] == "!switchcp":
         await route.send("<@&1039127920469364737>")
         embedVar = discord.Embed(title="Clan Battle", description="<@&1039127920469364737> \n{}".format("If u can play please contact your <@&935246053928730664> or <@&954389304073924630>"), color=0xff0000)
         if len(user_message.lower().split(" ")) >= 2:
            time = "{} {}".format(user_message.lower().split(" ")[1].split("-")[0],user_message.lower().split(" ")[1].split("-")[1])
            if len(user_message.lower().split(" ")) >= 3: 
                date = "{}".format(user_message.lower().split(" ")[2])
                if len(user_message.lower().split(" ")) >= 4:
                    opponent = "{}".format(user_message.split(" ")[3])                  
                    if len(user_message.lower().split(" ")) >= 5:
                        max_players = "{}".format(user_message.split(" ")[4])
         embedVar.add_field(name="Time", value= time, inline=False)
         embedVar.add_field(name="Date", value= date, inline=False)
         embedVar.add_field(name="Opponent", value= opponent, inline=False)
         embedVar.add_field(name="Max players", value= max_players, inline=False)
         await route.send(embed=embedVar)
         return
  #NATAN
  if message.channel == client.get_channel(1046462011585863751):
      name = "Event#{}".format(len(events))
      day = 0
      hour = 0
      minute = 0
      count = 0
      if user_message.lower().split(" ")[0] == "!setevent":
          if len(user_message.lower().split(" ")) >= 2:
              name = user_message.lower().split(" ")[1]
              if len(user_message.lower().split(" ")) >= 3:
                day = int(user_message.lower().split(" ")[2])
                if len(user_message.lower().split(" ")) >= 4:
                    hour = int(user_message.lower().split(" ")[3])
                    if len(user_message.lower().split(" ")) >= 5:
                        minute = int(user_message.lower().split(" ")[4])
                        if len(user_message.lower().split(" ")) >= 6:
                            count = int(user_message.lower().split(" ")[5])
      events.append(Set_Event(name,day,hour,minute,count))

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="New")
    await client.add_roles(member, role)
    print("Role added")

client.run(TOKEN)
