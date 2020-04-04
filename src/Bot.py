import discord
import asyncio
from User import User
from Items import Items
import sys
import os
from random import seed
from random import randint
from datetime import datetime
from datetime import timedelta

# change before pushing
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

    increment(author)

    if (message.content).lower() == 'f':
        await client.send_message(message.channel, "F")


    elif (message.content).lower() == 'no u' or (message.content).lower() == 'no you':
        await client.send_message(message.channel, "No u")

    elif (message.content).lower().startswith('fuck'):
        shit = message.content.split()
        msg = ' '.join(shit[1:]) + ' is coming :eyes:'
        await client.send_message(message.channel, msg)

    elif single_command(author, 'invite', message.content):
        embed = discord.Embed(title='BLOB REAPER INVITE LINK',
                       url='https://discordapp.com/api/oauth2/authorize?client_id=687476783297462312&permissions=8&scope=bot',
                       description='DM an admin for premium!')
        embed.set_image(url='https://i.ibb.co/YLn9RRL/Blob-Reaper-copy2.png')
        await client.send_message(message.channel, embed=embed)

    elif single_command(author, 'hello', message.content):
        msg = 'Sup {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    elif single_command(author, 'souls', message.content):
        if len(message.content) <= len(prefix) + 5:
            msg = 'Pocket: ``' + str(user_data[author].souls[0]) + '`` soul stones\n'
            msg += 'Sack: ``' + str(user_data[author].souls[1]) + '``/``' + \
                str(user_data[author].souls[2]) + '`` soul stones.'
            title = "Your Wealth"
            embed = discord.Embed(title=title, description=msg, color=0xffd700)
            await client.send_message(message.channel, embed=embed)
        else:
            tagger = str(message.content[len(prefix) + 9:-1])
            if id_validator(tagger):
                msg = 'Pocket: ``' + str(user_data[tagger].souls[0]) + '`` soul stones\n'
                msg += 'Sack: ``' + str(user_data[tagger].souls[1]) + '``/``' + \
                    str(user_data[tagger].souls[2]) + '`` soul stones.'
                title = "Their Wealth"
                embed = discord.Embed(title=title, description=msg, color=0xffd700)
                await client.send_message(message.channel, embed=embed)
            else:
                msg = 'Gimme a real user id gdi.'
                await client.send_message(message.channel, msg)

    elif single_command(author, 'stash', message.content):
        # ;dep 1000
        shit = message.content.split()
        shit.append(".")
        amt = shit[1]
        msg = ""
        if not amt.isdigit() and amt != 'max':
            msg = 'Smh. Enter either a number or `max`.'
        else:
            max = user_data[author].souls[2] - user_data[author].souls[1]
            if amt == 'max':
                amt = min(max, user_data[author].souls[0])
            amt = int(amt)
            if amt > max:
                msg = 'Bruh you cant stash that much your sac is too small :eyes:'
            elif amt > user_data[author].souls[0]:
                msg = 'Stop cheating you cant stash more than you have lmao'
            else:
                user_data[author].souls[1] += amt
                user_data[author].souls[0] -= amt
                msg = 'You have stashed ' + str(amt) + ' soul stones.'
        await client.send_message(message.channel, msg)

    elif single_command(author, 'with', message.content):
        # ;with 1000
        shit = message.content.split()
        shit.append(".")
        amt = shit[1]
        msg = ""
        if not amt.isdigit() and amt != 'max':
            msg = 'Smh. Enter either a number or `max`.'
        else:
            max = user_data[author].souls[1]
            if amt == 'max':
                amt = max
            amt = int(amt)
            if amt > max:
                msg = 'Bruh you dont have that much >:('
            else:
                user_data[author].souls[1] -= amt
                user_data[author].souls[0] += amt
                msg = 'You have withdrawn ' + str(amt) + ' soul stones.'
        await client.send_message(message.channel, msg)

    elif single_command(author, 'cloth', message.content):
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

    elif single_command(author, 'inv', message.content):
        if len(message.content) <= len(prefix) + 7:
            title = "Your Stuff"
            msg = user_data[author].listinv()
            embed = discord.Embed(title=title, description=msg, color=0x6a0dad)
            await client.send_message(message.channel, embed=embed)
        else:
            bfs = message.content.split()
            tagger = str(bfs[1][3:-1])
            if id_validator(tagger):
                title = "Their Stuff"
                msg = user_data[tagger].listinv()
                embed = discord.Embed(title=title, description=msg, color=0x6a0dad)
                await client.send_message(message.channel, embed=embed)
            else:
                msg = 'Gimme a real user id gdi.'
                await client.send_message(message.channel, msg)

    elif single_command(author, 'shop', message.content):
        shit = message.content.split()
        if len(shit) == 1:
            # display shop
            store = open("resources/shop.txt", "r")
            lines = store.readlines()
            msg = "".join(lines)
            embed = discord.Embed(title="Reaper Shop", description=msg, color=0x7fffd4)
            await client.send_message(message.channel, embed=embed)
        elif len(shit) == 2:
            item = shit[1]
            if item in Items.store_dets.keys():
                msg = Items.store_dets[item]
                embed = discord.Embed(title=item+" details", description=msg, color=0x7fffd4)
                await client.send_message(message.channel, embed=embed)
            else:
                msg = 'You dumbass that item doesnt exist'
                await client.send_message(message.channel, msg)

    elif single_command(author, 'buy', message.content):
        shit = message.content.split()
        if len(shit) == 1:
            msg = 'Specify something to buy u dumbass'
        elif len(shit) == 2:
            msg = user_data[author].buy(shit[1:])
        await client.send_message(message.channel, msg)

    elif single_command(author, 'upgrade', message.content):
        shit = message.content.split()
        if len(shit) == 1:
            msg = 'Specify something to upgrade u dumbass'
        elif len(shit) == 2:
            msg = user_data[author].upgrade(shit[1:])
        await client.send_message(message.channel, msg)

    elif single_command(author, 'search', message.content):
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

    elif double_command(author, 'sacrifice', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].sacrifice == "|" or user_comm[author] == 'sacrifice':
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].sacrifice, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 120:
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
                    add = ""
                    shrinesouls = Items.eshrine[user_data[author].inv[1]]
                    if shrinesouls != 0:
                        add = ' + ' + str(shrinesouls)
                    msg = 'Correct! You  have earned `' + str(rint) + add + '` soul stones.'
                    user_data[author].souls[0] += (rint + shrinesouls)
                else:
                    msg = 'Incorrect! :rage: You have eaned NOOO soul stones.'
                user_comm[author] = ''
                global_temp[author] = ""
        else:
            msg = "You have to wait a little before sacrificing\n" + \
                str((120 - int(diff)) // 60) + " minutes " + str(int(120 - diff) % 60) + \
                " seconds until you can kill again"
        await client.send_message(message.channel, msg)

    elif single_command(author, 'gamble', message.content):
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
                        (user_data[author].souls)[0] += amt
                        color = 0x00FF00
                    else:
                        msg = 'Sucks to be you. \n You rolled a `' + str(rint) + \
                            '` and BR rolled a `' + str(rint2) + \
                                '`\nYou just lost everything you gambled.'
                        (user_data[author].souls)[0] -= amt
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

    elif single_command(author, 'weekly', message.content):
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

    elif single_command(author, 'daily', message.content):
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

    elif single_command(author, 'snatch', message.content):
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

    elif single_command(author, 'help', message.content):
        shit = message.content.split()
        if len(shit) == 1:
            msg = "`;help mod` - help with moderation commands\n" \
            "`;help fun` - help with game commands"
        elif len(shit) == 2:
            if shit[1] == 'mod':
                sentences = open("resources/helpmod.txt", "r")
            elif shit[1] == 'fun':
                sentences = open("resources/helpfun.txt", "r")
            lines = sentences.readlines()
            msg = "".join(lines)
        embed = discord.Embed(title="Blob Reaper Help", description=msg, color=0x000000)
        await client.send_message(message.channel, embed=embed)

    elif single_command(author, 'share', message.content):
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

    elif single_command(author, 'use', message.content):
        shit = message.content.split()
        # ;use cloth 10
        shit = message.content.split()
        msg = user_data[author].use(shit[1:])
        await client.send_message(message.channel, msg)

    # occurs when owner stops bot (testing purposes)
    elif message.content == ';end':
        if str(message.author).startswith('nzwl'):
            save_data()
            await client.send_message(message.channel, "The bot is now closed.")
            sys.exit(1)
        else:
            await client.send_message(message.channel, "You don't have that permission!")

# important helper functions
def id_validator(id):
    return id in user_data.keys()

def increment(author):
    nowtime = datetime.now().replace(microsecond=0)
    ok = diff = lasttime = 0
    if user_data[author].lastcomm == "|":
        ok = 2
    else:
        lasttime = datetime.strptime(user_data[author].lastcomm, '%Y-%m-%d/%H:%M:%S')
        diff = int((nowtime - lasttime).total_seconds())
        if diff >= 3600:
            ok = 1
        else:
            ok = 0
    if ok > 0:
        if ok == 2:
            mult = 1
            lasttime = nowtime
        if ok == 1:
            mult = diff // 3600
            lasttime += timedelta(seconds=3600 * mult)
        user_data[author].lastcomm = str(lasttime.strftime("%Y-%m-%d/%H:%M:%S"))
        forgelvl = user_data[author].inv[2]
        user_data[author].souls[0] += Items.eforge[forgelvl] * mult

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
        vals.append(['0', '0', '0']) #to either 0 or |
        ###################################

        user_data[vals[0]] = User(eval(vals[1]), vals[2], vals[3], vals[4], \
            vals[5], vals[6], vals[7], vals[8], int(vals[9]), eval(vals[10]))
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
    await client.change_presence(game=discord.Game(name='with nzwl | ;help'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(initialize())
client.run(TOKEN)
