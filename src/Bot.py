import discord
import asyncio
from User import User
import sys
import os
from random import seed
from random import randint
from datetime import datetime

# change before pushing!!!
TOKEN = ''

client = discord.Client()

seed()
prefix = ';'
user_data = {}      # check notes.txt for info
user_comm = {}      # last user command that needs to be remembered
global_temp = {}    # any extraneous vars that might be used in next iteration
rand_names = []

@client.event
async def on_message(message):

    await client.wait_until_ready()

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # simplicity
    author = message.author.id

    if single_command(author, 'hello', message.content):
        msg = 'Sup {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if single_command(author, 'souls', message.content):
        if len(message.content) <= len(prefix) + 5:
            msg = 'Pocket: ``' + str(user_data[author].souls[0]) + '`` soul stones\n'
            msg += 'Sack: ``' + str(user_data[author].souls[1]) + '``/``' + \
                str(user_data[author].souls[2]) + '`` soul stones.'
            title = "Your Wealth"
            embed = discord.Embed(title=title, description=msg, color=0x7fffd4)
            await client.send_message(message.channel, embed=embed)
        else:
            tagger = str(message.content[len(prefix) + 9:-1])
            if id_validator(tagger):
                msg = 'Pocket: ``' + str(user_data[tagger].souls[0]) + '`` soul stones\n'
                msg += 'Sack: ``' + str(user_data[tagger].souls[1]) + '``/``' + \
                    str(user_data[tagger].souls[2]) + '`` soul stones.'
                title = "Their Wealth"
                embed = discord.Embed(title=title, description=msg, color=0x7fffd4)
                await client.send_message(message.channel, embed=embed)
            else:
                msg = 'Gimme a real user id gdi.'
                await client.send_message(message.channel, msg=msg)

    if single_command(author, 'cloth', message.content):
        # ;cloth <@!asldfjalskdfj>
        if len(message.content) <= len(prefix) + 5:
            msg = 'You have ' + str(user_data[author].cloth) + ' pieces of cloth.'
        else:
            bfs = message.content.split()
            tagger = str(bfs[1][3:-1])
            if id_validator(tagger):
                msg = 'They have ' + str(user_data[tagger].cloth) + ' pieces of cloth.'
            else:
                msg = 'Gimme a real user id gdi.'
        await client.send_message(message.channel, msg)

    if single_command(author, 'search', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].search == "|":
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].search, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 30:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            user_data[author].search = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            earn = randint(0, 4)
            if earn == 0:
                msg = 'No. Just...no.'
            else:
                x = randint(0, len(rand_names) - 1)
                y = randint(20, 40)
                user_data[author].cloth += y
                msg = rand_names[x].rstrip('\n') + ' has given you ' + str(y) + ' cloth.'
        else:
            msg = "You get tired of searching so much. You need to wait " + \
                str(30 - int(diff)) + " more seconds before you can search again."
        await client.send_message(message.channel, msg)

    if double_command(author, 'sacrifice', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].sacrifice == "|" or user_comm[author] == 'sacrifice':
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].sacrifice, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 600:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            if user_comm[author] == '':
                # uses randomized sentence from file
                sentences = open("resources/sentences.txt", "r")
                lines = sentences.readlines()
                sentences.close()
                rint = randint(0, len(lines) - 1)
                global_temp[author] = lines[rint].rstrip('\n')
                msg = 'Retype the following line: `' + global_temp[author] + '`'
                user_comm[author] = 'sacrifice'
            else:
                user_data[author].sacrifice = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
                if message.content[1:] == global_temp[author].lower()[1:]:
                    rint = randint(100, 200)
                    msg = 'Correct! You  have earned `' + str(rint) + '` soul stones.'
                    user_data[author].souls[0] += rint
                else:
                    msg = 'Incorrect! :rage: You have eaned NOOO soul stones.'
                user_comm[author] = ''
                global_temp[author] = ""
        else:
            msg = "You have to wait a little before sacrificing\n" + \
                str((600 - int(diff)) // 60) + " minutes " + str(int(600 - diff) % 60) + \
                " seconds until you can kill again"
        await client.send_message(message.channel, msg)

    if single_command(author, 'gamble', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].gamble == "|":
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].gamble, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 5:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            user_data[author].gamble = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            amt = message.content[len(prefix) + 7:]
            color=0x301934
            if not amt.isdigit() and amt != 'all':
                msg = 'Bruh. Enter a freaking value gdi.'
            else:
                if amt == 'all':
                    amt = user_data[author].souls[0]
                else:
                    amt = int(amt)
                if user_data[author].souls[0] >= amt:
                    rint = randint(0, 14)
                    rint2 = randint(0, 14)
                    if rint > rint2:
                        rint3 = randint(20, 150)
                        amt = int(amt * rint3 / 100) + 1
                        msg = 'Nice!\nYou rolled a `' + str(rint) + '` and BR rolled a `' \
                            + str(rint2) + '`.\nYou have earned `' + str(rint3) + \
                                '%` of your bet.\n`' + str(amt) + '` soul stones for you!'
                        user_data[author].souls[0] += amt
                        color = 0x00FF00
                    else:
                        msg = 'Sucks to be you. \n You rolled a `' + str(rint) + \
                            '` and BR rolled a `' + str(rint2) + \
                                '`\nYou just lost everything you gambled.'
                        user_data[author].souls[0] -= amt
                        color = 0xFF0000
                else:
                    msg = "Wtaf is wrong with your math. You can't bet more " \
                        "than you have."
            embed = discord.Embed(title="Gambling Arena", description=msg, color=color)
            await client.send_message(message.channel, embed=embed)
        else:
            msg = "Dont gamble too fast lmao \n" + str(5 - int(diff)) + \
                " more seconds until you can gamble again"
            await client.send_message(message.channel, msg)

    if single_command(author, 'weekly', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].weekly == "|":
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].weekly, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 604800:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            user_data[author].weekly = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            msg = "Here are your weekly 2500 soul stones!"
            user_data[author].souls[0] += 2500
        else:
            rsec = 604800 - int(diff)
            rmin = (rsec // 60) % 60
            rhr = (rsec // 3600) % 24
            rday = (rsec // 86400)
            rsec = rsec % 60
            msg = "Hasnt been a week yet :/ \n" + str(rday) + " days, " + str(rhr) + \
                " hrs, " + str(rmin) + " mins, " + str(rsec) + \
                " seconds until you can get your weekly soul stones again"
        await client.send_message(message.channel, msg)

    if single_command(author, 'daily', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].daily == "|":
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].daily, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 86400:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            user_data[author].daily = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            msg = "Here are your daily 500 soul stones!"
            user_data[author].souls[0] += 500
        else:
            rsec = 86400 - int(diff)
            rmin = (rsec // 60) % 60
            rhr = (rsec // 3600)
            rsec = rsec % 60
            msg = "Hasnt been a day yet :/ \n" + str(rhr) + " hrs, " + str(rmin) + \
                " mins, " + str(rsec) + " seconds until you can get your daily soul stones again"
        await client.send_message(message.channel, msg)

    if single_command(author, 'snatch', message.content):
        tagger = str(message.content[len(prefix) + 10:-1])
        if id_validator(tagger):
            if user_data[author].souls[0] < 150:
                msg = 'Yo, u need at least 150 waffles to snatch!\n' \
                    'How tf r u gunna pay off the fine if ur unsuccessful :/'
            elif user_data[tagger].souls[0] < 100:
                msg = 'Nah, your target only has 100 waffles. :disappointed: ' \
                    'No need to steal from such a poor noob.'
            else:
                rint = randint(0, 99)
                if rint < 40:
                    rint = randint(5, 15)
                    amt = int(rint / 100 * user_data[tagger].souls[0])
                    user_data[tagger].souls[0] -= amt
                    user_data[author].souls[0] += amt
                    msg = 'Lit. Your hands are fast asf. Youve snatched ' + \
                        str(amt) + ' waffles. :waffle:'
                else:
                    msg = 'Sucks to be slo. Youv lost 350 waffles to your ' \
                        'target as a result. :smiling_imp:'
                    user_data[author].souls[0] -= 350
                    user_data[tagger].souls[0] += 350
        else:
            msg = 'I stg. R u stupid. U cant rob someone if they dont exist :/' \
                '\nTag someone real smh.'
        await client.send_message(message.channel, msg)

    if single_command(author, 'help', message.content):
        sentences = open("resources/help.txt", "r")
        lines = sentences.readlines()
        msg = "".join(lines)
        embed = discord.Embed(title="Blob Reaper Help", description=msg, color=0x000000)
        await client.send_message(message.channel, embed=embed)

    if single_command(author, 'share', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].share == "|":
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].share, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 60:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            user_data[author].share = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            # ;share @eddie 1000
            terms = message.content.split()
            val = terms[2]
            tagger = (terms[1])[3:-1]
            if id_validator(tagger):
                if not val.isdigit():
                    msg = 'Bruh. Enter a freaking value gdi.'
                else:
                    val = int(val)
                    if user_data[author].souls[0] < val:
                        msg = 'Ur actually so dumb. You cant share more than you have.'
                    else:
                        user_data[author].souls[0] -= val
                        user_data[tagger].souls[0] += val
                        msg = 'You have shared ' + str(val) + ' souls with them'
            else:
                msg = 'Gimme a real user id gdi.'
        else:
            msg = "Stop sharing so fast. You need to wait " + \
                str(60 - int(diff)) + " more seconds before you can share again."
        await client.send_message(message.channel, msg)

    if single_command(author, 'use', message.content):
        shit = message.content.split()
        # ;use cloth


    # occurs when owner stops bot (testing purposes)
    if message.content.startswith(';end'):
        if str(message.author).startswith('nzwl702'):
            save_data()
            await client.send_message(message.channel, "The bot is now closed.")
            sys.exit(1)
        else:
            await client.send_message(message.channel, "You don't have that permission!")

# important helper functions
def id_validator(id):
    return id in user_data.keys()

def no_command(author, keyword):
    return user_comm[author] == keyword

def single_command(author, keyword, message):
    if author not in user_comm.keys():
        return False
    return (user_comm[author] == keyword or user_comm[author] == '') \
        and message.lower().startswith(prefix + keyword)

def double_command(author, keyword, message):
    if author not in user_comm.keys():
        return False
    return user_comm[author] == '' and message.lower().startswith(prefix + keyword) \
        or user_comm[author] == keyword

# useless helper functions
def memeString(s):
    res = ""
    for idx in range(len(s)):
        if not idx % 2 :
           res = res + s[idx].upper()
        else:
           res = res + s[idx].lower()
    return res

# initializer
async def initialize():
    sys.path.insert(0, 'resources')

    global user_comm
    await client.wait_until_ready()
    print('loading initial data...')
    # read in resource values
    data = open("resources/users.txt", "r")
    lines = data.readlines()
    for line in lines:
        vals = line.split(';')

        # CHANGE THIS WHEN ADDING NEW ITEMS
        vals.extend(['0']) #to either 0 or |
        ###################################

        user_data[vals[0]] = User(eval(vals[1]), vals[2], vals[3], vals[4], \
            vals[5], vals[6], vals[7], vals[8], int(vals[9]))
    data.close()

    # create all user-specific vars: user_comm{str:str}, balance{str:int}
    for server in client.servers:
        for m in server.members:
            user_comm[m.id] = ""                        # initializes user_comm
            if m.id not in user_data.keys():
                user_data[m.id] = User()

    # initialize global data vars
    names = open("resources/names.txt", "r")
    lines = names.readlines()
    for line in lines:
        rand_names.append(line)
    names.close()

    print('initialization complete\n-------\n')

def save_data():
    # save all balances to bank
    data = open("resources/users.txt", 'w')
    for key in user_data:
        data.write(str(key) + ";" + str(user_data[key]) + "\n")
    data.close()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(initialize())
client.run(TOKEN)
