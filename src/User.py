from Items import Items

class User:

    items = {'scythe': 0, 'shrine': 1, 'forge': 2}

    def __init__(self, souls=[0, 0, 0], daily='|', weekly='|', search='|', gamble='|', \
        sacrifice='|', snatch='|', share='|', cloth=0, inv=[0, 0, 0], lastcomm='|'):
        # souls value (pocket, sack, maxsack)
        self.souls = souls
        self.cloth = cloth
        self.inv = inv

        # these are all times
        self.daily = daily
        self.weekly = weekly
        self.search = search
        self.gamble = gamble
        self.sacrifice = sacrifice
        self.snatch = snatch
        self.share = share

        self.lastcomm= lastcomm

    def use(self, comms):
        if len(comms) == 1:
            comms.append(1)
        # double commands like ;use cloth 10
        if comms[0] == 'cloth':
            if comms[1].isdigit():
                val = int(comms[1])
                if self.cloth >= val:
                    self.souls[2] += 20 * val
                    self.cloth -= val
                    return "Your sack's capacity has been increased by " + \
                        str(val * 20) + " space."
                else:
                    return "Bruh wtf you don't have that much cloth"
            else:
                return "Dude i stg. Enter a number omg."

    def listinv(self):
        return Items.listinv(self.inv[0], self.inv[1], self.inv[2])

    def buy(self, comms):
        item = comms[0]
        if len(comms) > 1:
            num = comms[1]
        if item in Items.items.keys():
            # if item is a tool
            if Items.items[item][1][0] == 'tool':
                lvl = self.inv[Items.items[item][0]]
                if lvl != 0:
                    return 'You already have this item. Only 1 allowed.'
                else:
                    # pay for this items
                    item_price = Items.items[item][2][lvl]
                    if self.souls[0] >= item_price:
                        self.souls[0] -= item_price
                        self.inv[Items.items[item][0]] += 1
                        return 'You have bought a ' + item
                    else:
                        return 'You poor noob. Get more souls to afford this.'
            # do other types of items later
            # pass
        else:
            return "That item doesn't exist dumbass."

    def upgrade(self, item):
        item = item[0]
        # ;upgrade scythe
        if item in Items.items.keys():
            if Items.items[item][1][0] == 'tool':
                lvl = self.inv[Items.items[item][0]]
                if lvl == 0:
                    return "Lmao stop cheating you don't have this item"
                elif lvl == 5:
                    return "Oops, you've already upgraded this to the max!"
                else:
                    item_price = Items.items[item][2][lvl]
                    if self.souls[0] >= item_price:
                        self.souls[0] -= item_price
                        self.inv[Items.items[item][0]] += 1
                        return 'You have upgraded your ' + item
                    else:
                        return 'You poor noob. Get more souls to afford this.'
            else:
                return 'That item cannot be upgraded. :('
        else:
            return "That item doesn't exist..."

    def __str__(self):
        return str(self.souls) + ";" + self.daily + ";" + self.weekly + ";" + \
            self.search + ";" + self.gamble + ";" + self.sacrifice + ";" + \
            self.snatch + ";" + self.share + ";" + str(self.cloth) + ";" + \
            str(self.inv) + ";" + self.lastcomm
