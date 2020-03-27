import discord
import asyncio
from User import User
import sys
import os
from random import seed
from random import randint
from datetime import datetime

TOKEN = 'Njg3NDc2NzgzMjk3NDYyMzEy.XnvjJQ.lBRtf5VMd5ehgSKmyEk1fqJzKEc'

client = discord.Client()

seed()
prefix = ';'
user_data = {}      # check notes.txt for info
user_comm = {}      # last user command that needs to be remembered
global_temp = {}    # any extraneous vars that might be used in next iteration
rand_names = []

@client.event
async def on_message(message):

    # defining global vars
    # global user_comm
    # global global_temp
    # global balance

    await client.wait_until_ready()

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # simplicity
    author = message.author.id

    if single_command(author, 'hello', message.content):
        msg = 'Sup {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if single_command(author, 'waffles', message.content):
        if len(message.content) <= len(prefix) + 8:
            msg = 'Ur balance is ' + str(user_data[author].money) + ' waffles. :waffle:'
        else:
            tagger = str(message.content[len(prefix) + 11:-1])
            if id_validator(tagger):
                msg = 'Their balance is ' + str(user_data[tagger].money) + ' waffles. :waffle:'
            else:
                msg = 'Gimme a real user id gdi.'
        await client.send_message(message.channel, msg)

    if single_command(author, 'beg', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].beg == "|":
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].beg, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 30:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            user_data[author].beg = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            earn = randint(0, 4)
            if earn == 0:
                msg = 'No. Just...no.'
            else:
                x = randint(0, len(rand_names) - 1)
                y = randint(20, 40)
                user_data[author].money += y
                msg = rand_names[x].rstrip('\n') + ' has given you ' + str(y) + ' waffles.'

        else:
            msg = "You cant beg that much. Stop begging. You need to wait " + \
                str(30 - int(diff)) + " more seconds"
        await client.send_message(message.channel, msg)

    if double_command(author, 'work', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].work == "|" or user_comm[author] == 'work':
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].work, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 1800:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            if user_comm[author] == '':
                # uses randomized sentence from file
                sentences = open("sentences.txt", "r")
                lines = sentences.readlines()
                rint = randint(0, len(lines) - 1)
                global_temp[author] = memeString(lines[rint].rstrip('\n'))
                msg = 'Retype the following line in lowercase: `' + global_temp[author] + '`'
                user_comm[author] = 'work'
            else:
                user_data[author].work = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
                if message.content == global_temp[author].lower():
                    rint = randint(100, 200)
                    msg = 'Correct! You  have earned `' + str(rint) + '` waffles. :waffle:'
                    user_data[author].money += rint
                else:
                    msg = 'Incorrect! :rage: You have eaned NOOOO WAFFLES.'
                user_comm[author] = ''
                global_temp[author] = ""
        else:
            msg = "You have to wait a little before working\n" + str(int((1800 - diff)/60)) + \
                " more minutes until you can work again"
        await client.send_message(message.channel, msg)

    if single_command(author, 'bet', message.content):
        nowtime = datetime.now().replace(microsecond=0)
        ok = 0
        if user_data[author].bet == "|":
            ok = 1
        else:
            lasttime = datetime.strptime(user_data[author].bet, '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            if diff >= 10:
                ok = 1
            else:
                ok = 0
        if ok == 1:
            user_data[author].bet = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            amt = message.content[len(prefix) + 4:]
            color=0x301934
            if not amt.isdigit() and amt != 'all':
                msg = 'Bruh. Enter a freaking value gdi.'
            else:
                if amt == 'all':
                    amt = user_data[author].money
                else:
                    amt = int(amt)
                if user_data[author].money >= amt:
                    rint = randint(0, 14)
                    rint2 = randint(0, 14)
                    if rint > rint2:
                        rint3 = randint(20, 150)
                        amt = int(amt * rint3 / 100) + 1
                        msg = 'Nice!\nYou rolled a `' + str(rint) + '` and WR rolled a `' \
                            + str(rint2) + '`.\nYou have earned `' + str(rint3) + \
                                '%` of your bet.\n`' + str(amt) + '` waffles for you!'
                        user_data[author].money += amt
                        color = 0x00FF00
                    else:
                        msg = 'Sucks to be you. \n You rolled a `' + str(rint) + \
                            '` and WR rolled a `' + str(rint2) + \
                                '`\nYou just lost everything you bet.'
                        user_data[author].money -= amt
                        color = 0xFF0000
                else:
                    msg = "Wtaf is wrong with your math. You can't bet more " \
                        "than you have."
            embed = discord.Embed(title="Betting Arena", description=msg, color=color)
            await client.send_message(message.channel, embed=embed)
        else:
            msg = "Dont bet too fast lmao \n" + str(10 - int(diff)) + \
                " more seconds until you can bet again"
            await client.send_message(message.channel, msg)


    if single_command(author, 'snatch', message.content):
        tagger = str(message.content[len(prefix) + 10:-1])
        if id_validator(tagger):
            if user_data[author].money < 150:
                msg = 'Yo, u need at least 150 waffles to snatch!\n' \
                    'How tf r u gunna pay off the fine if ur unsuccessful :/'
            elif user_data[tagger].money < 100:
                msg = 'Nah, your target only has 100 waffles. :disappointed: ' \
                    'No need to steal from such a poor noob.'
            else:
                rint = randint(0, 99)
                if rint < 40:
                    rint = randint(5, 15)
                    amt = int(rint / 100 * user_data[tagger].money)
                    user_data[tagger].money -= amt
                    user_data[author].money += amt
                    msg = 'Lit. Your hands are fast asf. Youve snatched ' + \
                        str(amt) + ' waffles. :waffle:'
                else:
                    msg = 'Sucks to be slo. Youv lost 350 waffles to your ' \
                        'target as a result. :smiling_imp:'
                    user_data[author].money -= 350
                    user_data[tagger].money += 350
        else:
            msg = 'I stg. R u stupid. U cant rob someone if they dont exist :/' \
                '\nTag someone real smh.'
        await client.send_message(message.channel, msg)

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
    return (user_comm[author] == keyword or user_comm[author] == '') \
        and message.lower().startswith(prefix + keyword)

def double_command(author, keyword, message):
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
    new_path = os.path.relpath('..\\subfldr1\\testfile.txt', cur_path)

    # HEREEEE
    os.chdir('/foo/bar')
    global user_comm
    await client.wait_until_ready()
    print('loading initial data...')
    # read in money values for balance{str:int}
    data = open("..\\resources\\users.txt", "r")
    lines = data.readlines()
    for line in lines:
        vals = line.split()
        vals.extend(['|'])
        user_data[vals[0]] = User(int(vals[1]), vals[2], vals[3], vals[4], vals[5], vals[6], vals[7])
    data.close()

    # create all user-specific vars: user_comm{str:str}, balance{str:int}
    for server in client.servers:
        for m in server.members:
            user_comm[m.id] = ""                        # initializes user_comm
            if m.id not in user_data.keys():
                user_data[m.id] = User()

    # initialize global data vars
    names = open("..\\resources\\names.txt", "r")
    lines = names.readlines()
    for line in lines:
        rand_names.append(line)
    print('initialization complete\n-------\n')

def save_data():
    # save all balances to bank
    data = open("..\\resources\\users.txt", 'w')
    for key in user_data:
        data.write(str(key) + " " + str(user_data[key]) + "\n")
    data.close()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(initialize())
client.run(TOKEN)