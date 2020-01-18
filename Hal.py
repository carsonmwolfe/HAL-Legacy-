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
#ALLOWED_ID=["322490168034590732","289920025077219328","305845952986480650","285641499385921547"]
LAST_VIDEO=None
Meeting_Room=None
time_message=None
time_array=None
time_s=0
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
#photos(1)=["/home/pi/Desktop/20190119163521_1.JPG","/home/pi/Desktop/20190119162904_1.jpg","/home/pi/Desktop/20190119153640_1.jpg","/home/pi/Desktop/20190119163119_1.jpg","/home/pi/Desktop/20190119162922_1.jpg","/home/pi/Desktop/2019011918210350_1.jpg","/home/pi/Desktop/20190119163119_1.jpg","/home/pi/Desktop/20190119162640_1.jpg","/home/pi/Desktop/20190119161440_1.jpg","/home/pi/Desktop/2019011811719_1.jpg","/home/pi/Desktop/20190119163114_1.jpg","/home/pi/Desktop/20190119143642_1.jpg","/home/pi/Desktop/20170507152646_1.jpg","/home/pi/Desktop/20190120171108_1.jpg","/home/pi/Desktop/20190119162035_1.jpg","/home/pi/Desktop/20190119133028_1.jpg","/home/pi/Desktop/20190119163803_1.jpg","/home/pi/Desktop/20190119162823_1.jpg","/home/pi/Desktop/20190119155705_1.jpg"]     
commands = []
command = []             
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


#sg.theme('DarkAmber')

#layout = [  [sg.Text('Hal Dashboard')],
#            [sg.Text('Status: Online')],
#            [sg.Text('Core Temp:'),sg.InputText()],
#            [sg.Button('Test'), sg.Button('Cancel Program')]]

#window = sg.Window('Hal Dashboard',layout)

#while True:
#        event, values = window.read()
#        if event in (None, 'Stop'):
#            break
#window.close()


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
        
        
        
        
        
        
        
    #if str(message.content).upper().startswith==(*FART|):
     #   if Player!=None:
      #      if Player.is_playing():
       #         Player.stop()
        #try:
         #   if message.server.get_member_named("HAL").voice.voice_channel == None:
          #      channel=message.author.voice.voice_channel
           #     await client.join_voice_channel(channel)
            
        
    
    
    
    
    
    
    
    
    
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
        em.add_field(name="Miscellaneous", value="```"+"*Code"+"\n"+ "*Test" + "\n" + "*Avatar| Username" + "\n" + "*SetTimer"+"\n"+"*Invite"+"\n"+"*Clock" + "\n"+ "*Help" + "\n"+ "*Test" + "\n"+ "*KDQP | Username" + "\n"+ "*KDcomp | Username" +"\n".join(misc)+"```")
        em.add_field(name="Owner Only", value="```"+ "*Block" + "\n" + "*Leave" + "\n" + "*UnBlock|" + "\n" + "*Block|All" + "\n"+ "*UnBlock|All" + "\n" +"*Restart" +"\n".join(OO)+"```")
        em.add_field(name="Music", value ="```"+"*Play|" + "\n" + "*Volume" + "\n"+ "*Resume" + "\n" +"*Repeat" + "\n" + "*Pause" + "\n" + "*Repeat"+ "\n" + "*Move" + "\n"+"```")
        em.set_footer(text="Hal | {:%b,%d %Y}".format(today))
        await client.send_message(message.channel, embed=em)
        
    #Work in progress
    #if discord.member.get_user_info = status.offline
     #   server.get_member_named(str(message.content).split('|')[1])
      #  client.change_nickname(message.content.replace('IN':str(time.status.offline))
    #if discord.member.get_user_info = status.online
     #   server.get_member_named(str('nickname'):
        
    #if str(message.content).upper()=="*ADDCVOICE":
     #   await client.create_channel(message.server, 'Voice', type=discord.ChannelType.Voice)
    #if str(message.content).upper()=='*ADDTEXT':
     #   my_perms = discord.PermissionOverwrite(read_messages=True)                                        
      #  await client.create_channel(server, 'secret', everyone, mine)
    #if str(message.content).upper().startswith("*IM SORRY"):
     #  await client.send_message(await client.get_user_info('289920025077219328'),(str(message.content)))  

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
                em = discord.Embed(title=Player.title, Duration=Player.duration, colour=3447003)
                em.set_author(name="Now Playing")
                em.set_footer(text="Hal | {:%b,%d %Y}".format(today))
                await client.send_message(message.channel, embed=em)
        except IndexError:
            await client.send_message(message.channel, ("Could not find '"+music4+"' on YouTube."))
            
@client.event        
#async def on_voice_state_update(before,after):
 #   global Meeting_Room
 #   if before.voice_channel==after.server.get_channel(Meeting_Room):
 #       Meeting_Room=after.server.get_channel(Meeting_Room)    
 #       print(Meeting_Room.voice_members)
 #       if len(Meeting_Room.voice_members)==0:
 #           await client.delete_channel(Meeting_Room)
#Join Server Message (Work in progress            
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


