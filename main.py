import requests as r
from multiprocessing import Process as p 
import tqdm as tqdm
import os
tokens = open("tokens.txt", "r").readlines()
valid = open("valids.txt", 'r').readlines()
bad = open("bad.txt", "r").readlines()
logo = '''
███████╗██╗      ██████╗  ██████╗ ██████╗  ██████╗  █████╗ ████████╗███████╗
█║  ██║███████║   ██║   █████╗  
██╔══╝  ██║     ██║║██║   ██║██╔══██║   ██║   ██╔══╝  
██║     ███████╗╚██╝╚█████████╗
╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝'''
def joiner(invite):
    good = 0
    bad = 0
    for token in tokens:
      try:
        r.post("https://discordapp.com/api/invites/" + invite, headers={"authorization": token})
        print(token + ": joined")
        good += 1
      except:
        bad += 1
    os.system("clear")
    print(logo)
    print(f"{good}/{bad} joined")
def spam(channel, message, am):
    for i in range(am):
        for token in tokens:
            r.post(f"https://discordapp.com/api/channels/{channel}/messages", headers={"authorization": token}, json={"content": message})
            print(f"{token} : sent")

def leaver(guild_id):
    for token in tokens:
        r.delete(f"https://discordapp.com/api/users/@me/guilds/{guild_id}", headers={"authorization": token})
        print(f"{token} : left")

def checker():
    for token in tokens:
        try:
            userdata = r.get("https://discordapp.com/api/users/@me", headers={"authorization": token}).json()
            print(f"User: {userdata['username']}#{userdata['discriminator']} ({userdata['id']})'s token i/s {token} : valid")
            valid.append(token)
        except:
            open("bad.txt", "a").write(f"{token}\n")
    print(f"Valid tokens: {len(valid)}")
    open("valid.txt", "w").writelines(valid)
print(logo)
print(f"""
    Tokens: {len(tokens)}
    Valids: {len(valid)}
    Bads: {len(bad)}
    1. Joiner
    2. Spammer
    3. Leaver
    4. Checker
    \n
""")

option = input("Option: ")
if option == "1":
    invite = input("Invite: ")
    joiner(invite=invite)
if option == "2":
    channel = input("Channel id: ")
    message = input("Message: ")
    am = input("Amount")
    p(target=spam, args=(channel, message)).start()
if option == "3":
    guild_id = input("Guild id: ")
    leaver(guild_id=guild_id)
if option == "4":
    checker()
