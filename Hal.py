#Created November 2018

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
import TokenDoc


os.system('/home/pi/desktop/Backup')

CREATOR_ID="285641499385921547"
HAL_ID="493927329261813770"

client=discord.Client()

photos=["/home/pi/Desktop/20190119163521_1.JPG","/home/pi/Desktop/20190119162904_1.jpg","/home/pi/Desktop/20190119153640_1.jpg","/home/pi/Desktop/20190119163119_1.jpg","/home/pi/Desktop/20190119162922_1.jpg","/home/pi/Desktop/2019011918210350_1.jpg","/home/pi/Desktop/20190119163119_1.jpg","/home/pi/Desktop/20190119162640_1.jpg","/home/pi/Desktop/20190119161440_1.jpg","/home/pi/Desktop/2019011811719_1.jpg","/home/pi/Desktop/20190119163114_1.jpg","/home/pi/Desktop/20190119143642_1.jpg","/home/pi/Desktop/20170507152646_1.jpg","/home/pi/Desktop/20190120171108_1.jpg","/home/pi/Desktop/20190119162035_1.jpg","/home/pi/Desktop/20190119133028_1.jpg","/home/pi/Desktop/20190119163803_1.jpg","/home/pi/Desktop/20190119162823_1.jpg","/home/pi/Desktop/20190119155705_1.jpg"]
       
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

@client.event
async def on_message(message):
    global Player
    global Blocked
    if message.author in Blocked:
        await client.delete_message(message)
        return
    if str(message.content).upper()=="*ADD":
        em = discord.Embed(colour=3447003)
        em.set_author(name="Heres The HAL's Invite Link: https://bit.ly/2FsLi1V")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=='*CODE':
        em = discord.Embed(colour=3447003)
        em.set_author(name="Github Link: https://bit.ly/2QHtYal")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=="*CURSEDIMAGE":
        await client.send_file(message.channel,r"/home/pi/Desktop/IMG_1679.JPG")
    if str(message.content).upper()=="*SOCIALISM":
        await client.send_file(message.channel,r"//home/pi/Desktop/IMG_6969.JPG")
    if str(message.content).upper()=="*BIRTHDAY":
        em = discord.Embed(colour=3447003)
        em.set_author(name="January,9th")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=="*INTERSTELLAR":
        await client.send_file(message.channel,r"C:\Users\cmwol\Desktop\interstellar_poster_0.JPG")
    if str(message.content).upper().startswith("*BLOCK|"):
        if message.author.id==CREATOR_ID:
            Blocked.append(message.server.get_member_named(str(message.content).split('|')[1]))
            em = discord.Embed(colour=3447003)
            em.set_author(name="{0} Has Been Blocked.".format(str(message.server.get_member_named(str(message.content).split('|')[1]))))
            await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=="*KSP":
        randphoto= photos[random.randrange(0,len(photos))]
        em = discord.Embed(colour=3447003)
        await client.send_file(message.channel,open(randphoto,'rb'))   
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
    if str(message.content).upper().startswith("*IM SORRY"):
        await client.send_message(await client.get_user_info('289920025077219328'),(str(message.content)))    
    if str(message.content).upper().startswith("*UNBLOCK|"):
        Blocked.remove(message.server.get_member_named(str(message.content).split('|')[1]))
        em = discord.Embed(colour=3447003)
        em.set_author(name="{0} Has Been Unblocked.".format(str(message.server.get_member_named(str(message.content).split('|')[1]))))
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()==("*PAUSE"):
        Player.pause()
        em = discord.Embed(colour=3447003)
        em.set_author(name="Music is Paused.")
        await client.send_message(message.channel, embed=em)
        #await client.send_message(message.channel, "Music is Paused.")   
    if str(message.content).upper()==("*RESUME"):
        Player.resume()
        em = discord.Embed(colour=3447003)
        em.set_author(name="Music Has been Resumed.")
        await client.send_message(message.channel, embed=em)
        #await client.send_message(message.channel, "Music Has Been Resumed.")

    #if str(message.content).upper('*SHUTDOWN'):
     #   if message.author.id==Creator_ID:
      #      client.loop.run_until_complete(client.logout())
            

    #    
    if str(message.content).upper()==("*RESTART"): 
        if message.author.id==CREATOR_ID:
            client.loop.run_until_complete(client.logout())
            os.system("python3 /home/pie/ Hal.py")

                
    
    if str(message.content).upper()=='*COMMANDS':
        em = discord.Embed(title='Hals Commands',colour=3447003)
        em=discord.Embed(title="Command List",description="*Add - Will Send an Invite Link to the channel so you can add him to your server.\n\
        *Code - Will send a link to Github for Hals source Code.\n\
        *CursedImage - Will send a Cursed Image.\n\
        *Block| - Will Block the stated user from messaging any channel *FOR CREATOR USE ONLY*.\n\
        *UnBlock| - Will UnBlock the stated user to allow them to message any channel *FOR CREATOR USE ONLY*.\n\
        *Ksp - Will send a random KSP screenshot from my game libary.\n\
        *Clock - Will display the date and time.\n\
        *play| - Will play any music you want, link or title name will work.\n\
        *Pause - Will pause the current music.\n\
        *Resume - Will resume the current music.")           
        await client.send_message(message.channel, embed=em)
        
        

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
                em = discord.Embed(title=Player.title, Duration=Player.duration, colour=3447003)
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
async def on_server_join(server):
    for channel in server.channels:
        if channel.name=='general':
            await client.send_message(channel, "Hello, Im HAL!, There are lots of commands to help improve your server. Thank you for chooseing HAL")
       
        #if message.author == client.user:
     #   return
    #me = await client.get_user_info('ID')
    #await client.send_message(me, "Hello!")
     
client.run(TokenDoc.token)
