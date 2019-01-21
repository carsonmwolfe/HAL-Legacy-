import csv
import discord
import asyncio
import time
import youtube_dl
import urllib
import re
import datetime
CREATOR_ID="285641499385921547"
HAL_ID="493927329261813770"

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
        await client.send_file(message.channel,r"C:\Users\cmwol\Desktop\IMG_1679.JPG")
    if str(message.content).upper()=="*SOCIALISM":
        await client.send_file(message.channel,r"C:\Users\cmwol\Desktop\IMG_6969.JPG")
    if str(message.content).upper()=="*BIRTHDAY":
        em = discord.Embed(colour=3447003)
        em.set_author(name="January,9th")
        await client.send_message(message.channel, embed=em)
    if str(message.content).upper()=="*INTERSTELLAR":
        await client.send_file(message.channel,r"C:\Users\cmwol\Desktop\interstellar_poster_0.JPG")
    if str(message.content).upper().startswith("*BLOCK|"):
        Blocked.append(message.server.get_member_named(str(message.content).split('|')[1]))
        em = discord.Embed(colour=3447003)
        em.set_author(name="{0} Has Been Blocked.".format(str(message.server.get_member_named(str(message.content).split('|')[1]))))
        await client.send_message(message.channel, embed=em)    
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
        await client.send_message(message.channel, "Music is Paused.")
    if str(message.content).upper()==("*RESUME"):
        Player.resume()
        await client.send_message(message.channel, "Music Has Been Resumed.")

    #if discord.member.get_user_info = status.offline
     #   server.get_member_named(str(message.content).split('|')[1])
      #  client.change_nickname(message.content.replace('IN':str(time.status.offline))
    #if discord.member.get_user_info = status.online
     #   server.get_member_named(str('nickname'):
        
    #if str(message.content).upper()=="*ADDCVOICE":
     #   await client.create_channel(message.server, 'Voice', type=discord.ChannelType.Voice)
    #if str(message.content).upper()=='*ADDTEXT':
     #   my_perms = discord.PermissionOverwrite(read_messages=True                                        
        #mine = discord.ChannelPermissions(target=server.me, overwrite=my_perms)
         #await client.create_channel(server, 'secret', everyone, mine)

                                               
    if str(message.content).upper().startswith("*PLAY|"):
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
                #await client.send_message(message.channel,"NOW PLAYING:|{0}".format(Player.title))
                em = discord.Embed(title=Player.title, Duration=Player.duration, colour=3447003)
                em.set_author(name="Now Playing")
                await client.send_message(message.channel, embed=em)
        except IndexError:
            await client.send_message(message.channel, ("Could not find '"+music4+"' on YouTube.")) 
    if str(message.content).upper()=="*BESTSONG":
        await client.send_message(message.channel, '''
*Notice, Interstellar is the best soundtrack of all time*
Ain't no surprise
That I can't sleep tonight
My only vice
Is standing by your side
So won't you love me better
I'm waiting here
I need you now
Gravity can't hold us down
So just take me there
To higher ground
Save me
I'm holding onto you
My sun is fading
I'm falling into blue
Why don't you save me
My blood is running cold
So lift me up
And get me to higher ground
Would you give me shelter
I need you now
If you lead, I'll follow
I'm reaching out
So won't you love me better
I'm waiting here
I need you now
Gravity can't hold us down
So just take me there
So won't you love me better
I'm waiting here
I need you now
Gravity can't hold us down
So just take me there
To higher ground
Save me
I'm holding onto you
My sun is fading
I'm falling into blue
Why don't you save me
My blood is running cold
So lift me up
And get me to higher ground
Link To Song: https://youtu.be/RdTmwmCIcFM''')
        if message.server.get_member_named("HAL").voice.voice_channel == None:
           channel=message.author.voice.voice_channel
           await client.join_voice_channel(channel)
           Player=await message.server.voice_client.create_ytdl_player("https://youtu.be/RdTmwmCIcFM")
           Player.start()
           em = discord.Embed(title=Player.title, Duration=Player.duration, colour=3447003)
           em.set_author(name="Now Playing Best Song")       
async def on_server_join(server):
    for channel in server.channels:
        if channel.name=='general':
            await client.send_message(channel, "Hello, Im HAL!, There are lots of commands to help improve your server. Thank you for chooseing HAL")
       
        #if message.author == client.user:
     #   return
    #me = await client.get_user_info('ID')
    #await client.send_message(me, "Hello!")     

    
        
                                  
#all HAL haters
#HAL will become much more different from Kipp
#its just in the early stages of development
#and there are some key features that are overlapping with kipp
#For example *play|

client.run("NDkzOTI3MzI5MjYxODEzNzcw.DpCMiw.fgbAnjJsl6fvriiREm4Ir9D65lA")
