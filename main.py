import discord
import json
import random
import subprocess as sp

flopCount = 0
client = discord.Client()
config_name = "config.json"
with open(config_name) as f:
    config = json.load(f)
    token = config["token"]
    prefix = config["prefix"]
    guilds = config["guilds"]

def find_command(command_name):
    with open(config_name) as f:
        config = json.load(f)
    
    for command in config["commands"]:
        if command["call"].lower() == command_name:
            return command
        
    return None

def string_builder(list):
    val = list[0]
    for word in list[1:]:
        val = val + " " + word
    return val

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global flopCount
    if message.author == client.user:
        return
    elif message.content.split()[0] == prefix + "flopCount":
        await message.channel.send("{0} flops reacted to since last reset".format(flopCount))
    elif message.content.split()[0] == prefix + "eval":
        run = False
        guild = message.guild
        guild_admin = guild.get_role(guilds[str(guild.id)])


        for role in message.author.roles:
            if role == guild_admin:
                run = True

        if run:
            await message.channel.send(eval(" ".join(message.content.split()[1:]),{}, {} ))
        else:
            await message.channel.send("Error: you dont have the permissons to run this command")
    elif message.content.split()[0] == prefix + "addCommand":
        msg_split = message.content.split()
        guild = message.guild
        guild_admin = guild.get_role(guilds[str(guild.id)])
        run = False
        found = False

        for role in message.author.roles:
            if role == guild_admin:
                run = True
        
        if run:
            with open(config_name) as f:
                old_cfg = json.load(f)
        
            for i,command in enumerate(old_cfg["commands"]):
                if command["call"] == msg_split[1]:
                    old_cfg["commands"][i]["responses"].append(
                        string_builder(msg_split[2:]))
                    found = True
                else:
                    pass
            if not found:
                old_cfg["commands"].append({"call": msg_split[1], "responses": [
                                           string_builder(msg_split[2:])]})

            with open(config_name, "w") as f:
                json.dump(old_cfg, f, indent=4)
        else:
            await message.channel.send("Error: you dont have the permissons to run this command")


    elif message.content.split()[0] == prefix + "removeCommand":
        msg_split = message.content.split()
        guild = message.guild
        guild_admin = guild.get_role(guilds[str(guild.id)])
        run = False
        found = False

        for role in message.author.roles:
            if role == guild_admin:
                run = True

        if run:
            with open(config_name) as f:
                old_cfg = json.load(f)

            for i,command in enumerate(old_cfg["commands"]):
                if command["call"] == msg_split[1]:
                    old_cfg["commands"].pop(i)
                    found = True
                else:
                    pass
            if not found:
                message.channel.send("Error: command doesnt exist")

            with open(config_name, "w") as f:
                json.dump(old_cfg, f, indent=4)

        else:
            await message.channel.send("Error: you dont have the permissons to run this command")
    elif message.content.split()[0].lower() == prefix + "help":
        msg = ""
        with open(config_name) as f:
            config = json.load(f)
        for command in config["commands"]:
            msg = msg + prefix + command["call"] + ", "
        await message.channel.send(msg)

    elif message.content.split()[0].lower() == prefix + "mods":
        msg = ""
        if type(message.content.split()[1]) != str  :
            msg = "Error: Search query not supplied."
        else:
            msg = "https://www.curseforge.com/minecraft/mc-mods/search?search=" + "+".join(message.content.split()[1:])
        await message.channel.send(msg)

    elif message.content.split()[0].lower() == prefix + "modpacks":
        msg = ""
        if type(message.content.split()[1]) != str  :
            msg = "Error: Search query not supplied."
        else:
            msg = "https://www.curseforge.com/minecraft/modpacks/search?search=" + "+".join(message.content.split()[1:])
        await message.channel.send(msg)
                                                                            

    elif message.content[0] == prefix:
        cmd_str = message.content.split(" ")[0].lower()
        command = find_command(cmd_str[1:])
        if command == None:
            print("Cant find command " + cmd_str[1:])
            return
        else:
            response = command["responses"][random.randint(0, len(command["responses"])-1)]
            await message.channel.send(response)

client.run(token)
