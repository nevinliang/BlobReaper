from Items import Items

class User:

    items = {'scythe': 0, 'shrine': 1, 'forge': 2}

    def __init__(self, souls=[0, 0, 0], daily='|', weekly='|', search='|', gamble='|', \
        sacrifice='|', snatch='|', share='|', cloth=0, inv=[0, 0, 0]):
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

    def use(self, comms):
        if len(comms) == 1:
            # single commandos like ;use bomb
            pass
        elif len(comms) == 2:
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
            if Item.items[item][1][0] == 'tool':
                if (self.inv)[Items.items[item][0]] != 0:
                    return 'You already have this item. Only 1 allowed.'

        else:
            return "That item doesn't exist dumbass."

    def upgrade(self, item):
        # ;upgrade scythe
        if item in items.keys():
            if Item.items[item][1][0] == 'tool':
                if self.inv[items[item][0]] == 0:
                    return "Lmao stop cheating you don't have this item"
                elif self.inv[items[item][0]] == 5:
                    return "Oops, you've already upgraded this to the max!"
                else:
                    self.inv[items[item]] += 1
                    # pay for the item
                    # HEREEEE
                    return "You have upgraded your " + item + "."
            else:
                return 'That item cannot be upgraded. :('
        else:
            return "That item doesn't exist..."

    def __str__(self):
        return str(self.souls) + ";" + self.daily + ";" + self.weekly + ";" + \
            self.search + ";" + self.gamble + ";" + self.sacrifice + ";" + \
            self.snatch + ";" + self.share + ";" + str(self.cloth) + ";" + \
            str(self.inv)
