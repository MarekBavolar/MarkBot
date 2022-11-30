import discord
import random
import os
import datetime
import pytz
from discord.ext import commands, tasks

TOKEN = "MTA0NjEzMTc3MjA0OTYwODgzOQ.G3ZBwt.l0tvzxra8R4IpliSTkSLDK2BqMPVvdVl-RBCLQ"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
allowed_channels = []
events = []

class Event:
    def __init__(self, name, day, hour, minute, bool_c):
        self.name = name
        self.day = int(day)
        self.hour = int(hour)
        self.minute = int(minute)
        self.pinged = int(bool_c)
    def GetName(self):
        return self.name
    def GetDay(self):
        return self.day
    def GetHour(self):
        return self.hour
    def GetMinute(self):
        return self.minute
    def was_pinged(self):
        return self.pinged
    def ping(self):
        self.pinged = 1
    def event_ended(self, now):
        if now.day == self.day:
            if now.hour == self.hour:
                if now.minute >= self.minute:
                    return True
        return False
    def ping_event(self, current_time):
        if current_time.day == self.day:
            if (self.hour - current_time.hour) <= 1:
                return True
        return False
class player:
    def __init__(self, name, platform):
        self.name = name
        self.platform = platform
    def GetName(self):
        return self.name
    def GetPlatform(self):
        return self.platform

def load_roster(file):
    final = []
    roster_info = file.read().split("\n")
    for user in roster_info:
        if user == "":
            continue
        final.append(player(user,"None"))
    return final

def load_events(file):
    final = []
    event_info = file.read().split("\n")
    for info in event_info:
        list = info.split(";")  
        if len(list) < 5:
            continue
        final.append(Event(list[0].split(":")[1],list[1].split(":")[1],list[2].split(":")[1],list[3].split(":")[1],list[4].split(":")[1]))
    return final

def load_file(file, list):
    for event in list:
        file.write(f"Name:{event.GetName()};Day:{event.GetDay()};Hour:{event.GetHour()};Minute:{event.GetMinute()};bool:{event.was_pinged()}\n")
def load_roster_file(file, list):
    for player in list:
        file.write("{}\n".format(player.GetName()))
  
@tasks.loop(seconds=5)
async def check_time():
    file = open("Events.txt", "r+")
    events = load_events(file)
    file.close()
    
    now = datetime.datetime.now(pytz.timezone('Europe/Bratislava'))
    
    route = client.get_channel(947664851327664159)
    for event in events:
        if event.ping_event(now) and (event.was_pinged() != 1):
            event.ping()
            file = open("Events.txt", "w")
            load_file(file, events)
            file.close()
            await route.send("<@&946578011300458497>")
            await route.send("{} starts in less than an hour!".format(event.GetName()))
        if event.event_ended(now):
            events.remove(event)
            file = open("Events.txt", "w")
            load_file(file, events)
            file.close()

    

@client.event
async def on_ready():
    print('Booted up.')
    check_time.start()

@client.event
async def on_reaction_add(reaction, user):
    file = open("roster.txt","r")
    cbroster = load_roster(file)
    file.close()
    if reaction.emoji == client.get_emoji(1046853654726070413):
        if user.name == "MarkBot":
            return
        for participant in cbroster:
            if user.name == participant.GetName():
                return
        print("added")
        print(cbroster)
        cbroster.append(player(user.name,"None"))
    elif reaction.emoji == client.get_emoji(1046853705145790525):
        for participant in cbroster:
            if participant.GetName() == user.name:
                cbroster.remove(participant)
    file = open("roster.txt","w")
    load_roster_file(file, cbroster)
    file.close() 

@client.event
async def on_message(message):
    base_commands = [("!events", "Sends a list of upcomming events."), ("!sus","Posts a SUSSY image."),("!roulette","Spins a wheel of roulette."),("!getshanked","U just get shanked."),("!sauce","Rolls a random hentai image.(Only works in #Sauce channel)")]
    cb_commands = [("!cb-roster","Sends a list of players who want to participate in a upcomming clan battle"),("!cb","!cb-(platforms excluded by -) time(hours:minutes)-(timezone) date(example: 24.12.2021) Name_of_clan number_of_participants\n Example: !cb-ps-xbox-pc 8:30-est 24.12.2021 TestClan 10"),("!cb_end","!cb-end W/L, this will conclude the cb and remove it from events.")]
    file = open("Events.txt", "r")
    events = load_events(file)
    file.close()
    file = open("roster.txt", "r")
    cbroster = load_roster(file)
    file.close()

    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel_name = str(message.channel.name)
    
    logs = open("logs.txt","a")
    print(f"{username}: {user_message} ({channel_name})")
    logs.write("Log time - {}\n".format("None"))
    logs.close()
    
    if message.author == client.user:
        return
    if user_message.lower() == '!help':
        embedVar = discord.Embed(title="List of commands", color=0xffd200)
        for command in base_commands:
            embedVar.add_field(name="{}".format(command[0]), value= "- {}".format(command[1]), inline=False)
        await message.channel.send(embed=embedVar)
        return
    if user_message.lower() == '!help-cb':
        embedVar = discord.Embed(title="List of commands", color=0xffd200)
        for command in cb_commands:
            embedVar.add_field(name="{}".format(command[0]), value= "- {}".format(command[1]), inline=False)
        await message.channel.send(embed=embedVar)
        return
    if user_message.lower() == '!events':
      embedVar = discord.Embed(title="Events", color=0xff0000)
      for event in events:
          if len(event.GetName().split("_")) > 1:
            embedVar.add_field(name="{} {}".format(event.GetName().split("_")[0],event.GetName().split("_")[1]), value= "At {}:{}".format(event.GetHour(),event.GetMinute()), inline=False)
          else:
            embedVar.add_field(name="{}".format(event.GetName()), value= "At {}:{}".format(event.GetHour(),event.GetMinute()), inline=False)
      await message.channel.send(embed=embedVar)
      return
    if user_message.lower() == '!cb-roster':
      embedVar = discord.Embed(title="Players", color=0x068bff)
      i = 1
      for participant in cbroster:
          embedVar.add_field(name="#{}".format(i), value= "> {}".format(participant.GetName()), inline=False)
          i += 1
      
      await message.channel.send(embed=embedVar)
      return
    
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
          await message.channel.send(file=discord.File('Memes/sus.png'))
          return
    elif user_message.lower() == "<@1046131772049608839>":
          await message.channel.send(file=discord.File('Memes/mark.jpg'))
          return
    elif "yoda" in user_message.lower().split(" "):
          await message.channel.send(file=discord.File('Memes/yoda_sip.gif'))
          await message.channel.send("indeed")
          return 
    elif user_message.lower() == "!getshanked":
          await message.channel.send(file=discord.File('Memes/shank_stab.gif'))
          return
    
    if (message.channel == client.get_channel(959554685528858654)) or (message.channel == client.get_channel(1046237995134615582)):
      if user_message.lower() == "!sauce":
        random_file = random.choice(os.listdir("Sauce"))
        source_file="%s\%s"%("Sauce",random_file)
        await message.channel.send(file=discord.File(source_file))
        return
    elif (message.channel == client.get_channel(1046547800575443034)) or (message.channel == client.get_channel(1046519554119057569)):
      if user_message.lower().split(" ")[0] == '!cb-end':
        await message.channel.send("List has been cleared!")
        file = open("roster.txt","w")
        file.close()
        await message.channel.send("Clan battle has been concluded!")
        announcements = client.get_channel(947664851327664159)
        if user_message.lower().split(" ")[1] == "w":
            await announcements.send("<@&946578011300458497>")
            await announcements.send("Lets GOOO! We won!")
            await announcements.send(file=discord.File('Memes/W.gif'))
        if user_message.lower().split(" ")[1] == "l":
            await announcements.send("<@&946578011300458497>")
            await announcements.send("We will learn from this loss and get em next time for sure! GGs Boys")
            await announcements.send(file=discord.File('Memes/L.gif'))
        for event in events:
            if event.GetName() == "Clan Battle":
                events.remove(event)
                break
        file = open("Events.txt","w")
        load_file(file, events)
        file.close()
        return

      if message.channel == client.get_channel(1046519554119057569):  
         route = client.get_channel(1046132801390522420)
      elif message.channel == client.get_channel(1046547800575443034):
         route = client.get_channel(929118971272237087)
      
      platforms = []
      time = "Not Set"
      date = "Not Set"
      opponent = "None"
      max_players = "0"
      if user_message.lower().split(" ")[0].split("-")[0] == "!cb":
          if "pc" in user_message.lower().split(" ")[0].split("-"):
                 platforms.append("<@&935030804063588413>")
          if "ps" in user_message.lower().split(" ")[0].split("-"):
                 platforms.append("<@&935030376752095272>")
          if "xbox" in user_message.lower().split(" ")[0].split("-"):
                 platforms.append("<@&935030608650993674>")
          if "switch" in user_message.lower().split(" ")[0].split("-"):
                 platforms.append("<@&1039127920469364737>")
         
          embedVar = discord.Embed(title="Clan Battle", description="{}".format("If u can play please contact your \n <@&935246053928730664> or <@&954389304073924630>"), color=0xa902c9)
          if len(user_message.lower().split(" ")) >= 2:
                if (user_message.split(" ")[1][0] == "-") or (user_message.split(" ")[1].split(":")[1][0] == "-"):
                    await message.channel.send("Invalid time!")
                    await message.channel.send("Time must be a positive number!")
                    return
                if (int(user_message.split(" ")[1].split("-")[0].split(":")[0]) > 24) or (int(user_message.split(" ")[1].split("-")[0].split(":")[1]) > 60):
                    await message.channel.send("Invalid time!")
                    await message.channel.send("Valid time format: hour:minute-timezone")
                    return
            
                time = "{} {}".format(user_message.split(" ")[1].split("-")[0],user_message.split(" ")[1].split("-")[1])
          if len(user_message.split(" ")) >= 3:
                 if (int(user_message.split(" ")[2].split(".")[0]) > 31) or (int(user_message.split(" ")[2].split(".")[1]) > 12):
                        await message.channel.send("Invalid date!")
                        await message.channel.send("Valid date format: day.month.year")
                        return
                 date = "{}".format(user_message.lower().split(" ")[2])
          if len(user_message.lower().split(" ")) >= 4:
                 opponent = "{}".format(user_message.split(" ")[3])                  
          if len(user_message.lower().split(" ")) >= 5:
                 if int(user_message.split(" ")[4]) < 1:
                      await message.channel.send("Number of opponents must be greater than 0.")
                      return
                 max_players = "{}".format(user_message.split(" ")[4])
          file = open("Events.txt","a")
          file.write("Name:Clan Battle;Day:{};Hour:{};Minute:{};bool:0\n".format(date.split(".")[0],time.split(" ")[0].split(":")[0],time.split(" ")[0].split(":")[1]))
          file.close()
          file = open("Events.txt","r")
          events = load_events(file)
          file.close()
          embedVar.add_field(name="Time", value= time, inline=False)
          embedVar.add_field(name="Date", value= date, inline=False)
          embedVar.add_field(name="Opponent", value= opponent, inline=False)
          embedVar.add_field(name="Max players", value= max_players, inline=False)
          print(len(platforms))
          for platform in platforms:
              await route.send(platform)
          cb_embed = await route.send(embed=embedVar)
          yes = client.get_emoji(1046853654726070413)
          no = client.get_emoji(1046853705145790525)
          await cb_embed.add_reaction(yes)
          await cb_embed.add_reaction(no)
          return
    if message.channel == client.get_channel(1046547800575443034):
      name = "Event#{}".format(len(events))
      day = 0
      hour = 0
      minute = 0
      if user_message.lower().split(" ")[0] == "!setevent":
          if len(user_message.split(" ")) >= 2:
              name = user_message.split(" ")[1]
              
              if len(user_message.split(" ")) >= 3:
                day = int(user_message.split(" ")[2])
                
                if len(user_message.split(" ")) >= 4:
                    hour = int(user_message.split(" ")[3])
                    
                    if len(user_message.split(" ")) >= 5:
                        minute = int(user_message.lower().split(" ")[4])
          file = open("Events.txt", "a")
          file.write(f"Name:{name};Day:{day};Hour:{hour};Minute:{minute};bool:0\n")
          file.close()
          file = open("Events.txt", "r")
          events = load_events(file)
          file.close()

client.run(TOKEN)
