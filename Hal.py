#Created November 2018
#upadted july 8,2019
#Things To Add/Fix
import csv
import discord
#import asyncio
#import time
#import youtube_dl
import urllib
import re
import datetime
import os
import random
import requests
import TokenDoc
#os.system('/home/pi/desktop/Backup')
CREATOR_ID="285641499385921547"
HAL_ID="493927329261813770"
ALLOWED_ID=["322490168034590732","289920025077219328","305845952986480650","285641499385921547"]
LAST_VIDEO=None
Meeting_Room=None
client=discord.Client()
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
async def on_message(message):
    global Player
    global Blocked
    if message.author in Blocked:
        await client.delete_message(message)
        return
    #Simple (*) Commands
    if str(message.content).upper()=="*ADD":
        em = discord.Embed(colour=3447003)
        em.set_author(name="Heres The HAL's Invite Link: https://bit.ly/2FsLi1V")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=='*CODE':
        em = discord.Embed(colour=3447003)
        em.set_author(name="Github Link: https://bit.ly/2QHtYal")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=="*THRONEMAP":
        await client.send_file(message.channel,r"/home/pi/Desktop/Photos/Map.png")
    if str(message.content).upper()=="*BIRTHDAY":
        em = discord.Embed(colour=3447003)
        em.set_author(name="January,9th")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=="*DONATION":
        em = discord.Embed(colour=3447003)
        em.set_author(name="If you want to support MD financially here is a link to his donation page: https://streamlabs.com/MDLive_ ")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=='*STEAM':
        em = discord.Embed(colour=3447003)
        em.set_author(name="MD's steam profile: https://steamcommunity.com/user/cngp-prrd/TDRQTWQC/")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=='*TEST':
        em = discord.Embed(colour=3447003)
        em.set_author(name="Test Complete, Im Online!")
        await client.send_message(message.channel, embed=em)
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
  #  if str(message.content).upper().startswith("*MINE|"):
  #      if message.author.id in ALLOWED_ID:
  #          total= int(str(message.content).split('|')[1])
  #          for i in range (total):
  #              await client.send_message(message.channel, "!Mine")
  #          await client.send_message(message.channel, "!Transfer|{0}|{1}" .format(str (total),str (message.author)))
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
        if message.author.id==CREATOR_ID:
            Blocked.append(message.server.get_member_named(str(message.content).split('|')[1]))
            em = discord.Embed(colour=3447003)
            em.set_author(name="{0} Has Been Blocked.".format(str(message.server.get_member_named(str(message.content).split('|')[1]))))
            await client.send_message(message.channel, embed=em)
        else:
            em = discord.Embed(colour=3447003)
            em.set_author(name="This is a Admin Only command.")
    if str(message.content).upper().startswith("*UNBLOCK|"):
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
    if str(message.content).upper().startswith("*VOLUME|"):
        #Player.volume
        total= int(str(message.content).split('|')[1])
        Player.volume=total/100
        em = discord.Embed(colour=3447003)
        em.set_author(name="Music Volume has been changed to {0}".format(str(total))+"%." )
    #if str(message.content).upper()==("*STATUS")
     #   em = discord.Embed(colour=3447003)
         #em.set_author(name="")
    #Restart
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()==("*RESTART"):
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
    if str(message.content).upper()=='*COMMANDS':
        em = discord.Embed(title='Hals Commands',colour=3447003)
        em=discord.Embed(title="Command List",description="*Add - Will Send an Invite Link to the channel so you can add him to your server.\n\
        *Code - Will send a link to Github for Hals source Code.\n\
        *Block| - Will Block the stated user from messaging any channel *FOR CREATOR USE ONLY*.\n\
        *UnBlock| - Will UnBlock the stated user to allow them to message any channel *FOR CREATOR USE ONLY*.\n\
        *Block|All - Will block all users in the server that the  message is sent in *FOR CREATOR USE ONLY*.\n\
        *UnBlock|All - Will UnBlock all users in the server that the message is sent in *FOR CREATOR USE ONLY*.\n\
        *Restart - Will restart Hal's program to clear any erros. *FOR CREATOR USE ONLY* \n\
        *Meeting | #of voice channels wanted - Will create voice channels | WILL ONLY WORK IF PERMS ARE GIVEN.*FOR CREATOR USE ONLY* \n\
        \n\
        *Clock - Will display the date and time.\n\
        *play| - Will play any music you want, link or title name will work.\n\
        *Pause - Will pause the current music.\n\
        *Repeat - Will replay the last song. \n\
        *Steam - Will display steam profile link. \n\
        *Thronemap- Will display Shattered Throne first encounter symbol map. \n\
        *Test - Will test Hal's Commands in the background to see if he is fully online. \n\
        *KDOverall| Username - Will display the accounts OVERALL PVP KD. \n\
        *KDQP | Username - Will display the accounts Quickplay KD. \n\
        *KDcomp| Username - Will display the accounts COMP PVP KD. \n\
        *Commands - Display this embed message. \n\
        *Resume - Will resume the current music.")
        await client.send_message(message.channel, embed=em)
    #Work in progress
    #if discord.member.get_user_info = status.offline
    #    server.get_member_named(str(message.content).split('|')[1])
    #    client.change_nickname(message.content.replace('IN':str(time.status.offline))
    #if discord.member.get_user_info = status.online
    #    server.get_member_named(str('nickname'):
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
            if message.server.get_member_named("HAL").voice.voice_channel == None:
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
                await client.send_message(message.channel, embed=em)
        except IndexError:
            await client.send_message(message.channel, ("Could not find '"+music4+"' on YouTube."))
    if str(message.content).upper().startswith("*MEETING|"):
        Meeting_Room=await client.create_channel(message.server,"Meeting Room",type=discord.ChannelType.voice)
        await client.edit_channel(Meeting_Room,user_limit=int(str(message.content).split("|")[1]))
        Meeting_Room=Meeting_Room.id
#@client.event
#async def on_voice_state_update(before,after):
#    global Meeting_Room
#    if before.voice_channel==after.server.get_channel(Meeting_Room):
#        Meeting_Room=after.server.get_channel(Meeting_Room)
#        print(Meeting_Room.voice_members)
#        if len(Meeting_Room.voice_members)==0:
#            await client.delete_channel(Meeting_Room)
client.loop.run_until_complete(client.start(TokenDoc.token))
