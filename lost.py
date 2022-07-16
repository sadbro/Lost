import os
import discord
import json
from window import Host

TOKEN='Nzk4NjQxNDkzODQ5NTM4NjIw.Go-N1M._6GP82p0nC_HoEVWSo2Kxe8Nv_5IoxGe7svFOg'
API='AIzaSyDAzUwZuBTs_1QqoJiPEwEURFoZPmTZ9J8'

creator_ids= [522158489867649036]

intents= discord.Intents.all()
client= discord.Client(intents=intents)

__all__= ["update", "create", "create-secure","members", "init", "end", "register", "host", "start-league", "start-knockout", "stop-league", "stop-knockout", "send-link"]

def create_match_channel(group): ### League stages
    matches= []
    for i in range(len(group)):
        for j in range(i+1, len(group)):
            matches.append("{} vs {}".format(group[i], group[j]))
    print(matches)
    return matches

def MemoryDump(name, code, fp, top_level):

    with open(fp) as f:
        data= json.load(f)
        nc= {"name":name, "ID":code}
        data[top_level].append(nc)
    with open(fp, "w") as f:
        json.dump(data, f)

def Registered(code, fp, top_level):

    AlreadyRegistered= False
    with open(fp) as f:
        data= json.load(f)
        for player in data[top_level]:
            if player["ID"]==code:
                AlreadyRegistered= True

    return AlreadyRegistered

@client.event
async def on_ready():
    print("Whew....No longer lost.")
    pass

@client.event
async def on_message(message):
    if message.author==client.user:
        return

    if message.content=="!ping":
        await message.channel.send("I'm online.")

    if message.content.startswith("!create "):
        if message.author.id in creator_ids:
            ch_name= str(message.content[8:])
            await message.channel.guild.create_text_channel(ch_name)
        else:
            print("{} is trying !create".format(message.author))

    if message.content.startswith("!create-secure"):
        guild=message.channel.guild
        overwrites={guild.default_role:discord.PermissionOverwrite(read_messages=False)}
        if message.author.id in creator_ids:
            ch_name= str(message.content[14:])
            await message.channel.guild.create_text_channel(ch_name, overwrites=overwrites)
        else:
            print("{} is trying !create-secure".format(message.author))

    if message.content=='*members':
        for guild in client.guilds:
            print("\n{}\n".format(str(guild.name).upper()))
            for member in guild.members:
                print(" - {}".format(member))

    if message.content=='!members':
        print("\n{}\n".format(str(message.channel.guild.name).upper()))
        for member in message.channel.guild.members:
            print(" - {}".format(member))

### TOURNAMENT FUNCTIONS & HOSTING

    if message.content=='!reset':
        with open("register.json") as f:
            data= json.load(f)
            guild_id= data["guild_id"]
        if message.channel.guild.id==guild_id:
            if message.author.id in creator_ids:
                with open("register.json") as f:
                    data= json.load(f)
                    data["players"]= []
                    data["times"]= {"start": "", "end": ""}
                    data["guild_id"]= ""
                with open("register.json", "w") as f:
                    json.dump(data, f)
                with open("matches.json") as f:
                    data= json.load(f)
                    data["groups"]= []
                with open("matches.json", "w") as f:
                    json.dump(data, f)
                await message.channel.send("Tournament has been reset!!")
        else:
            await message.channel.send("Nothing here. you should move on")

    if message.content.startswith("!send-link"):
        with open("register.json") as f:
            data= json.load(f)
            names= []
            guild_id= data["guild_id"]
            for player in data["players"]:
                names.append(player["name"])
        if guild_id is not None:
            if str(message.author).split("#")[0] in names:
                channel= client.get_channel(target_channel)
                link= await channel.create_invite(max_age=1800, max_uses=1)
                await message.channel.send(link)
            else:
                await message.channel.send("You are not registered yet!!")
                print("{} is not registered yet trying to get link".format(message.author))
        else:
            await message.channel.send("Tournament has not yet started yet!!")
            print("{} is trying to get links though the tourney has not yet started".format(message.author))

    if message.content=='!register':
        with open("register.json") as f:
            data= json.load(f)
            regStart= data["times"]["start"]
            regEnd= data["times"]["end"]
            guild_id= data["guild_id"]

        if message.channel.guild.id==guild_id:
            if regStart=="started" and regEnd!="ended":
                name, code= str(message.author).split('#')
                if Registered(code, "register.json", "players"):
                    print("Attempted Register Request from {}".format(name))
                    await message.channel.send("You are already Registered!!")
                else:
                    await message.channel.send("Requesting Registration...")
                    cmd=input(">>>{} is asking for registration[y/n] ".format(name))
                    if cmd=="y":
                        response=f"{name} sucessfully registered!"
                        MemoryDump(name, code, "register.json", "players")
                        print(" - {} has REGISTERED.".format(name))
                        await message.channel.send(response)
                    else:
                        response="the admin has rejected your request for registration. please (don't) contact the admins."
                        print(" - {} has been REJECTED.".format(name))
                        await message.channel.send(response)
            elif regEnd=="ended":
                await message.channel.send("The early birds got the first worms. None left for you. Better luck next time.")
            else:
                await message.channel.send("Registration has not started yet!! please (don't) contact the admins.")

        else:
            await message.channel.send("Too much excitement is injurious to health")

    if message.content.startswith('!host'):
        try:
            grps= message.content.split()[1]
        except:
            grps= 2
        with open("register.json") as f:
            data= json.load(f)
            guild_id= data["guild_id"]
        if message.channel.guild.id==guild_id:
            if message.author.id in creator_ids:
                host= Host("register.json", groups=grps)
                host.start()
        else:
            await message.channel.send("Please learn Hosting to host")

    if message.content=='!init':
        try:
            guild_id= message.channel.guild.id
            if message.author.id in creator_ids:
                start= "started"
                with open("register.json") as f:
                    data= json.load(f)
                    data["times"]["start"]= start
                    data["guild_id"]= guild_id
                with open("register.json", "w") as f:
                    json.dump(data, f)
                await message.channel.send("Registration has started!!!")
        except AttributeError:
            await message.channel.send("Registration can only be started in a guild.")

    if message.content=='!end':
        with open("register.json") as f:
            data= json.load(f)
            guild_id= data["guild_id"]
        if message.channel.guild.id==guild_id:
            if message.author.id in creator_ids:
                end= "ended"
                with open("register.json") as f:
                    data= json.load(f)
                    data["times"]["end"]= end
                with open("register.json", "w") as f:
                    json.dump(data, f)
                await message.channel.send("Registration has ended!!!")
        else:
            await message.channel.send("Armageddon Prevented Sucessfully")

    if message.content=='!start-knockout':
        with open("register.json") as f:
            data= json.load(f)
            guild_id= data["guild_id"]
        if message.channel.guild.id==guild_id:
            if message.author.id in creator_ids:
                with open("matches.json") as f:
                    data= json.load(f)
                    G1= data["groups"][0]
                    G2= data["groups"][1]
                ko= await message.channel.guild.create_category("KnockOut")
                guild= message.channel.guild
                members= guild.members

                overwrites= {guild.default_role:discord.PermissionOverwrite(read_messages=False)}
                for player1, player2 in zip(G1, G2):
                    pair= (player1, player2)
                    match= "{} vs {}".format(player1, player2)
                    ch= await message.channel.guild.create_text_channel(match, category=ko, overwrites=overwrites)
                    for member in pair:
                        for mem in guild.members:
                            if mem.name==member:
                               member=mem
                        perms= ch.overwrites_for(member)
                        perms.send_messages= True
                        perms.read_messages= True
                        await ch.set_permissions(member, overwrite=perms)
        else:
            await message.channel.send("Wrong planet to start a knockOut")

    if message.content=='!start-league':
        with open("register.json") as f:
            data= json.load(f)
            guild_id= data["guild_id"]
        if message.channel.guild.id==guild_id:
            if message.author.id in creator_ids:
                with open("matches.json") as f:
                    data= json.load(f)
                    Gs= data["groups"]

                    guild= message.channel.guild
                    overwrites= {guild.default_role:discord.PermissionOverwrite(read_messages=False)}

                    for i, grp in enumerate(Gs):
                        ch= create_match_channel(grp)
                        print("G{}: {} matches".format(i+1, len(ch)))
                        ct= await message.channel.guild.create_category("Group-{}".format(i+1))
                        for match in ch:
                            pair= match.split(" vs ")
                            c= await message.channel.guild.create_text_channel(match, category=ct, overwrites=overwrites)
                            for member in pair:
                                for mem in guild.members:
                                    if mem.name==member:
                                        m=mem

                                perms= c.overwrites_for(m)
                                perms.send_messages= True
                                perms.read_messages= True
                                await c.set_permissions(m, overwrite=perms)

        else:
            await message.channel.send("What is the use of channels on another planet?")

    if message.content=='!stop-league':
        with open("register.json") as f:
            data= json.load(f)
            guild_id= data["guild_id"]
        with open("matches.json") as f:
            data= json.load(f)
            Gs= data["groups"]
        if message.channel.guild.id==guild_id:
            if message.author.id in creator_ids:
                server= message.channel.guild
                for i in range(len(Gs)):
                    ct= discord.utils.get(server.categories, name="Group-{}".format(i+1))
                    for c in ct.text_channels:
                        await c.delete()

        else:
            await message.channel.send("Are you even worthy?")

    if message.content=='!stop-knockout':
        with open("register.json") as f:
            data= json.load(f)
            guild_id= data["guild_id"]
        if message.channel.guild.id==guild_id:
            if message.author.id in creator_ids:
                server= message.channel.guild
                ko= discord.utils.get(server.categories, name="KnockOut")
                for ch in ko.text_channels:
                    await ch.delete()
        else:
            await message.channel.send("Buzzoff.")

client.run(TOKEN)

