#Created November 2018
#upadted july 8,2019

#Things To Add/Fix
#Replay, multiple server music, Destiny API (stats,gear,weekly..), Block all, Fix restart, fix add voice/text, fix change nicknames, 

import csv
import discord
import asyncio
import time
import youtube_dl
import urllib
import re
import datetime
import os
import random
import requests
import TokenDoc
import sys
import logging
import threading




#os.system('/home/pi/desktop/Backup')

CREATOR_ID="653386075095695361"
HAL_ID="663923530626367509"
LAST_VIDEO=None
Meeting_Room=None
time_message=None
time_array=None
time_s=0
farts=[]
path=r"/home/pi/Desktop/HAL/sounds"
for files in os.walk(path):
  for file in files:  
    farts.append(file)

farts = farts[2]

counter=-1
for fart in farts:
  counter+=1
  farts[counter]=path+"\\"+fart

print (farts)



today = datetime.date.today()
Halfooter=print("Hal {:%b,%d %Y}".format(today))
EmbedColor=0x36393E
countdown = False

#Embed Colors-
DEFAULT = 0
AQUA = 1752220
GREEN = 3066993
BLUE = 3447003
PURPLE = 10181046
GOLD = 15844367
ORANGE = 15105570
RED = 15158332
GREY = 9807270
DARKER_GREY = 8359053
NAVY = 3426654
DARK_AQUA = 1146986
DARK_GREEN = 2067276
DARK_BLUE = 2123412
DARK_PURPLE = 7419530
DARK_GOLD = 12745742
DARK_ORANGE = 11027200
DARK_RED = 10038562
DARK_GREY = 9936031
LIGHT_GREY = 12370112
DARK_NAVY = 2899536
LUMINOUS_VIVID_PINK = 16580705
DARK_VIVID_PINK = 12320855



client=discord.Client()         
Player=None
Memberinfo=[]
Blocked=[]
Voice=[]


Months = {1: "January",
2: "Feburary",
3: "March",
4: "April",
5: "May",
6: "June",
7: 'July',
8: "August",
9: "September",
10: "October",
11: "November",
12: "December"}


#Discord Bot Stat (streaming)
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="2001 A Space Odyssey ",type=1,url="https://www.twitch.tv/mdedits_"))
    
@client.event
async def on_server_join(server):
    readarray=[]
    reader=csv.reader(open(r'./Discord Servers(HAL).txt'))
    for row in reader:
        readarray.append(row)
    infile=False
    for row in readarray:
        if server.name in str(row):
            infile=True
            break
    if not infile:
        for channel in server.channels:
            try:
                inv=await client.create_invite(channel)
                break
            except discord.DiscordException:
                pass
        readarray.append(["{0}:\n{1}\n\n".format(server.name,str(inv))])
        with open (r'./Discord Servers(HAL).txt','w') as f:
            writer=csv.writer(f,delimiter=',')
            for row in readarray:
                if len(row)>0:
                    writer.writerow(row)
                    f.close()
@client.event
async def on_join():
    for role in server.roles:
        if str(role) == "Swarm":
            await client.add_roles(Swarm,role)
            
@client.event
async def on_reaction_add(reaction,user):
    global time_message
    global time_array
    global time_s
    global countdown

    if countdown:
        return
        
    if user.id == HAL_ID:
        return
    if reaction.emoji == "\u25C0":
        await client.remove_reaction(reaction.message,reaction.emoji,user)
        if time_s > 0:
            time_s -=1
            
    if reaction.emoji == "\u25B6":
        await client.remove_reaction(reaction.message,reaction.emoji,user)
        if time_s < 2:
            time_s +=1

    if reaction.emoji == "\u2795":
        await client.remove_reaction(reaction.message,reaction.emoji,user)
        if time_s == 1:
            if time_array[1] < 5:
                time_array[1]+=1
        if time_s == 2:
            if time_array[2]<9:
                time_array[2]+=1
        seconds=int(str(time_array[1])+str(time_array[2]))
        if seconds==59:
            if time_s==2:
                time_array[0]+=1
                time_array[1]=0
                time_array[2]=0
        if time_s==0:
            time_array[0]+=1
                
    if reaction.emoji == "\u2796":
        await client.remove_reaction(reaction.message,reaction.emoji,user)
        if time_array[time_s]>0:
            time_array[time_s]-=1

    if reaction.emoji == "\u2705":
        await client.remove_reaction(reaction.message,reaction.emoji,user)
        countdown=True
        for reaction in reaction.message.reactions:
            await client.remove_reaction(discord.utils.get(client.messages, id=reaction.message.id),reaction.emoji,reaction.message.server.get_member(HAL_ID))


    string_array =[]
    for i in range (3):
        if i==time_s:
            string_array.append("__`{0}`__".format(time_array[i]))
        else:
            string_array.append("`{0}`".format(time_array[i]))
    em=discord.Embed(title="Timer",description="{0}m{1}{2}s".format(string_array[0],string_array[1],string_array[2]).replace('``',''))
    time_message = await client.edit_message(time_message,embed=em)
     
          
@client.event
async def on_message(message):
    global Player
    global Blocked
    import datetime



    if str(message.content).upper()==("*SETTIMER"):
        em=discord.Embed(title="Timer",description="`0`m`00`s")
        global time_message
        time_message = await client.send_message(message.channel,embed=em)
        await client.add_reaction(time_message,"\u2795")
        await client.add_reaction(time_message,"\u2796")
        await client.add_reaction(time_message,"\u25C0")
        await client.add_reaction(time_message,"\u25B6")
        await client.add_reaction(time_message,"\u2705")
        global time_array
        time_array=[0,0,0]
        global time_s
        time_s=0
        



    if message.author in Blocked:
        await client.delete_message(message)
        return
    #Simple (*) Commands
    if str(message.content).upper()=='*CODE':
        em = discord.Embed(colour=3447003)
        em.set_author(name="Github Link: https://bit.ly/2QHtYal")
        await client.send_message(message.channel, embed=em)
        
        
   # if str(message.content).upper()=="*CORETEMP":
    #    em = discord.Embed(colour=3447003)
     #   em.set_author(name="{0}".format(int(open('/sys/class/thermal/thermal_zoneO/temp').read())/1000))
      #  await client.send_message(message.channel, embed=em)
        
    if str(message.content).upper()=='*TEST':
        em = discord.Embed(colour=3447003)
        em.set_author(name="Test Complete, Im Online!")
        await client.send_message(message.channel, embed=em)
        
    if str(message.content).upper()=='*INVITE':
        await client.send_message(message.channel,"https://bit.ly/2QSEWvX")
                                  
    if str(message.content).upper() == "*INVITES":
        if message.author.id:
            reader=csv.reader(open(r'./Discord Servers(HAL).txt'))
            msg=""
            for row in reader:
                if str(row).startswith("['https:"):
                    msg=msg+"\n{0}".format(str(row[0]))
                    await client.send_message(await client.get_user_info(CREATOR_ID),msg)
                    msg=""
                if len(str(row))>2 and str(row).startswith("['http")==False:
                    msg=msg+str(row[0])                                                                
    if str(message.content).upper().startswith("*MINE|"):
        if message.author.id in ALLOWED_ID:
            total= int(str(message.content).split('|')[1])
            for i in range (total):
                await client.send_message(message.channel, "!Mine")
            await client.send_message(message.channel, "!Transfer|{0}|{1}" .format(str (total),str (message.author)))


            
    if str(message.content).upper().startswith("*KDCOMP|"):
        username=str(message.content).split('|')[1]
        url="https://destinytracker.com/d2/profile/pc/{0}".format(username.replace('#','-'))
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        req=str(requests.get(url,headers).content)
        KD=req.split('"},{"label":"KDA"')[0].split('"displayValue":"')[1]
        await client.send_message(message.channel,"PVP Competitive KD:{0}".format(KD))
        
    if str(message.content).upper().startswith("*KDOVERALL|"):
        username=str(message.content).split('|')[1]
        url="https://destinytracker.com/d2/profile/pc/{0}".format(username.replace('#','-'))
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        req=str(requests.get(url,headers).content)
        KD=req[66200:].split('"},{"label":"KDA"')[0].split('"displayValue":"')[1]
        await client.send_message(message.channel,"PVP Overall KD:{0}".format(KD))

    if str(message.content).upper().startswith("*KDQP|"):
        username=str(message.content).split('|')[1]
        url="https://destinytracker.com/d2/profile/pc/{0}".format(username.replace('#','-'))
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        req=str(requests.get(url,headers).content)
        KD=req[60590:].split('"},{"label":"KDA"')[0].split('"displayValue":"')[1]
        await client.send_message(message.channel,"PVP Quickplay KD:{0}".format(KD))     
    #Block/Unblock Feature 
    if str(message.content).upper().startswith("*BLOCK|"):
        if message.author.id!=CREATOR_ID:
            em = discord.Embed(colour=3447003)
            em.set_author(name="This Command Is A Creator Only Command.")
            await client.send_message(message.channel, embed=em)
        if message.author.id==CREATOR_ID:
            Blocked.append(message.server.get_member_named(str(message.content).split('|')[1]))
            em = discord.Embed(colour=3447003)
            em.set_author(name="{0} Has Been Blocked.".format(str(message.server.get_member_named(str(message.content).split('|')[1]))))
            await client.send_message(message.channel, embed=em)
        else:
            em = discord.Embed(colour=3447003)
            em.set_author(name="This is a Admin Only command.")
                                               
    if str(message.content).upper().startswith("*UNBLOCK|"):
        if message.author.id!=CREATOR_ID:
            em = discord.Embed(colour=3447003)
            em.set_author(name="This Command Is A Creator Only Command.")
            await client.send_message(message.channel, embed=em)
        if message.author.id==CREATOR_ID:
            Blocked.remove(message.server.get_member_named(str(message.content).split('|')[1]))
            em = discord.Embed(colour=3447003)
            em.set_author(name="{0} Has Been Unblocked.".format(str(message.server.get_member_named(str(message.content).split('|')[1]))))
            await client.send_message(message.channel, embed=em)
    #Random Photos    
    if str(message.content).upper()=="*KSP":
        randphoto= photos[random.randrange(0,len(photos))]
        em = discord.Embed(colour=3447003)
        await client.send_file(message.channel,open(randphoto,'rb'))
    #Clock Command
    if str(message.content).upper()=="*CLOCK":
        now=datetime.datetime.now()
        AMPM=""
        hour=now.hour
        if now.hour < 13:
            AMPM ="AM"
        else:
            AMPM ="PM"
            hour=hour-12
        em = discord.Embed(colur=3447003,description="{0} {1}, {2}\n{3}:{4} {5}".format(Months[now.month],now.day,now.year,str(hour),str(now.minute),AMPM))
        await client.send_message(message.channel, embed=em)
    #Pause/Resume
    if str(message.content).upper()==("*PAUSE"):
        Player.pause()
        em = discord.Embed(colour=3447003)
        em.set_author(name="Music is Paused.")
        await client.send_message(message.channel, embed=em) 
    if str(message.content).upper()==("*RESUME"):
        Player.resume()
        em = discord.Embed(colour=3447003)
        em.set_author(name="Music Has been Resumed.")
        await client.send_message(message.channel, embed=em) 
        
    if str(message.content).upper().startswith("*VOLUME|"):
        Player.volume
        total= int(str(message.content).split('|')[1])
        Player.volume=total/100
        em = discord.Embed(colour=3447003)
        em.set_author(name="Music Volume has been changed to {0}".format(str(total))+"%." )
        
    if str(message.content).upper()==("*LEAVE"):
        if message.author.id==CREATOR_ID:
            await client.voice_client_in(message.server).disconnect()
            em = discord.Embed(colour=3447003)
            em.set_author(name="Hal has been disconnect from the voice channel")
            await client.send_message(message.channel, embed=em)
            
        if message.author.id!=CREATOR_ID:
            em = discord.Embed(colour=3447003)
            em.set_author(name="This Command Is A Creator Only Command.")
            await client.send_message(message.channel, embed=em)
        
    user = message.server.get_member(HAL_ID)
    channel = message.author.voice.voice_channel
        
        
    
        
    if str(message.content).upper()==("*FART"):

        em = discord.Embed(colour=3447003)
        em.set_author(name="Here it comes...")
        await client.send_message(message.channel, embed=em)
        time.sleep(1)
        em = discord.Embed(colour=3447003)
        em.set_author(name="3")
        await client.send_message(message.channel, embed=em)
        time.sleep(1)
        em = discord.Embed(colour=3447003)
        em.set_author(name="2")
        await client.send_message(message.channel, embed=em)
        time.sleep(1)
        em = discord.Embed(colour=3447003)
        em.set_author(name="1")
        await client.send_message(message.channel, embed=em)
        channel=message.author.voice.voice_channel
        
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player(random.choice(farts))
        player.start()


    
        time.sleep(4)
        em = discord.Embed(colour=3447003)
        em.set_author(name="Funny has concluded")
        await client.send_message(message.channel, embed=em)
        await client.voice_client_in(message.server).disconnect()
        

        


        
            
    if str(message.content).upper()==("*MOVE"):
        await client.move_member(user, channel)
        em = discord.Embed(colour=3447003)
        em.set_author(name="Hal has moved channels")
        await client.send_message(message.channel, embed=em)
        
    if str(message.content).upper().startswith("*AVATAR|"):
        member = str(message.content).split('|')[1]
        member = message.server.get_member_named(member)
        await client.send_message(message.channel, str(member)+"'s disocrd icon URL is"+ str(member.avatar_url))
        
    if str(message.content).upper()==("*RESTART"):
        if message.author.id!=CREATOR_ID:
            em = discord.Embed(colour=3447003)
            em.set_author(name="This Command Is A Creator Only Command.")
            await client.send_message(message.channel, embed=em)
            
        if message.author.id==CREATOR_ID:
            client.loop.run_until_complete(client.logout())
            os.system("python3 /home/pi/Hal.py")
            raise SystemExit
           
           
           
        
    if str(message.content).upper()==("*REPEAT"):
        if Player!=None:
            if Player.is_playing():
                Player.stop()
        try:
            query_string = urllib.parse.urlencode({"search_query" : str(message.content).split('|')[1]})
            req = urllib.request.Request("http://www.youtube.com/results?" + query_string)
            if message.server.get_member_named("HAL").voice.voice_channel == None:
                channel=message.author.voice.voice_channel
                await client.join_voice_channel(channel)
                Player=await message.server.voice_client.create_ytdl_player(LAST_VIDEO)
                Player.start()
                em = discord.Embed(title=Player.title, description=('Duration: ')+str(int(round(Player.duration/60)))+(' Minutes \nLink: '+link), colour=3447003)
                em.set_author(name="-Now Playing-")
                await client.send_message(message.channel, embed=em)
            else:
                channel=message.author.voice.voice_channel
                try:
                    Player=await message.server.voice_client.create_ytdl_player(link)
                except:
                    channel=message.author.voice.voice_channel
                    await client.join_voice_channel(channel)
                    Player=await message.server.voice_client.create_ytdl_player(link)
                Player.start()
                #await  client.send_message(message.channel,"NOW PLAYING:|{0}".format(Player.title))
                em = discord.Embed(title=Player.title, Duration=Player.duration, colour=3447003)
                em.set_author(name="Now Playing")
                await client.send_message(message.channel, embed=em)
        except IndexError:
            await client.send_message(message.channel, ("Could not find '"+music4+"' on YouTube."))

    #async def USERINFO(message,str(message.content).upper()):
    playerinfo = {}

    #if str(message.content).upper()=="*USERINFO":
    #    em = discord.Embed(tile=str(playerinfo[message.author])+"'s"+"Profile Infomation",colour=DARK_NAVY)
    #    em.set_author(name=str(message.author)+"'s User Info", icon_url=message.author.avatar_url)
    #    em.add_field(name="Currenlty Active on",value = "```"+str(playerinfo[message.author].game+"```"+"\n"+"*Nickname in Server:** "+str(playerinfo[message.author].nickname)))
    #    em.set_footer(text="Hal | {:%b,%d %Y}".format(today))
    #    await client.send_message(message.channel, embed=em)


    if str(message.content).upper()=='*HELP':
        
        misc=[]
        musc=[]
        OO=[]

        em = discord.Embed(title='Help',description="** *HelpCommands for command-specific information**",colour=DARK_NAVY)
        em.add_field(name="Miscellaneous", value="```"+"*Code"+"\n"+ "*Test" + "\n" + "*SetTimer"+"\n"+"*Invite"+"\n"+"*Clock" + "\n"+ "*Help" + "\n"+ "*Test" + "\n" + "*Avatar|Username" + "\n"+ "*KDQP|Username" + "\n"+ "*KDcomp|Username" +"\n".join(misc)+"```")
        em.add_field(name="Music", value ="```"+"*Play|" + "\n" + "*Volume" + "\n"+ "*Resume" + "\n" +"*Repeat" + "\n" + "*Pause" + "\n" + "*Repeat"+ "\n" + "*Move" + "\n"+"```")
        em.add_field(name="Owner Only", value="```"+ "*Block" + "\n" +"*Restart" +"\n"+ "*Leave"  + "\n" + "*Block|All" + "\n"+ "*UnBlock|All" + "\n" + "\n" + "*UnBlock|Username".join(OO)+"```")
        em.set_footer(text="Hal | {:%b,%d %Y}".format(today))
        await client.send_message(message.channel, embed=em)

    #Youtube_DL Music System                                            
    if str(message.content).upper().startswith("*PLAY|"):
        if Player!=None:
            if Player.is_playing():
                Player.stop()
        try:
            query_string = urllib.parse.urlencode({"search_query" : str(message.content).split('|')[1]})
            req = urllib.request.Request("http://www.youtube.com/results?" + query_string)
            with urllib.request.urlopen(req) as html:
                searchresults = re.findall(r'href=\"\/watch\?v=(.{11})', html.read().decode())
                link = ("http://www.youtube.com/watch?v=" + searchresults[0])
            if message.server.get_member_named("Hal").voice.voice_channel == None:
                channel=message.author.voice.voice_channel
                await client.join_voice_channel(channel)
                Player=await message.server.voice_client.create_ytdl_player(link)
                Player.start()
                #await client.send_message(message.channel,"NOW PLAYING:|{0}".format(Player.title))
                em = discord.Embed(title=Player.title, description=('Duration: ')+str(int(round(Player.duration/60)))+(' Minutes \nLink: '+link), colour=3447003)
                em.set_author(name="Now Playing")
                await client.send_message(message.channel, embed=em)
            else:
                channel=message.author.voice.voice_channel
                try:
                    Player=await message.server.voice_client.create_ytdl_player(link)
                except:
                    channel=message.author.voice.voice_channel
                    await client.join_voice_channel(channel)
                    Player=await message.server.voice_client.create_ytdl_player(link)
                Player.start()
                #await  client.send_message(message.channel,"NOW PLAYING:|{0}".format(Player.title))
                em = discord.Embed(title=Player.title, description=('Duration: ')+str(int(round(Player.duration/60)))+(' Minutes \nLink: '+link), colour=3447003)
                em.set_author(name="Now Playing")
                em.set_footer(text="Hal | {:%b,%d %Y}".format(today))
                await client.send_message(message.channel, embed=em)
        except IndexError:
            await client.send_message(message.channel, ("Could not find '"+music4+"' on YouTube."))
            
@client.event                   
async def on_server_join(server):
    for channel in server.channels:
        if channel.name=='general':
            await client.send_message(channel, "Hello, Im HAL!, I have lots of commands to help improve your server!")
@client.event
async def on_ready():
    client.loop.create_task(countdown_loop())

async def countdown_loop():
  global countdown
  while countdown:
    if time_array[2]>0:
      time_array[2]-=1
    else:
      time_array[2]=9
      if time_array[1]>0:
        time_array[1]-=1
      else:
        time_array[1]=5
        if time_array[0]>0:
          time_array[0]-=1
        else:
          countdown=False
          em=discord.Embed(title="Timer",description="**Timer Finished**")
          await client.edit_message(time_message,em=em)
    await asyncio.sleep(1)
    
    
client.loop.run_until_complete(client.start(TokenDoc.token))


