from Inventory import Inventory

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
        ret_str = ""
        if self.inv[0] != 0:
            ret_str += 'Scythe: Level ' + str(self.inv[0]) + ' ' + Inventory.scythe[self.inv[0]] + '\n'
        if self.inv[1] != 0:
            ret_str += 'Shrine: Level ' + str(self.inv[1]) + ' ' + Inventory.shrine[self.inv[1]] + '\n'
        if self.inv[2] != 0:
            ret_str += 'Forge: Level ' + str(self.inv[2]) + ' ' + Inventory.forge[self.inv[2]] + '\n'
        if ret_str == "":
            ret_str += "You're a noob reaper. You have nothing."
        return ret_str

    def buy(self, comms):
        if comms[0] in items.keys():
            if (self.inv)[items[comms[0]]] != 0:
                return 'You already have this item. Only 1 allowed.'
            else:
                # buy it
                pass
        else:
            return "That item doesn't exist dumbass."

    def upgrade(self, comms):
        if comms in items.keys():
            item = items[comms]
            if self.inv[items[item]] == 0:
                return "Lmao stop cheating you don't have this item"
            elif self.inv[items[item]] == 5:
                return "Oops, you've already upgraded this to the max!"
            else:
                self.inv[items[item]] += 1
                # pay for the item
                return "You have upgraded your " + comms + "."
        else:
            return "That item doesn't exist..."

    def __str__(self):
        return str(self.souls) + ";" + self.daily + ";" + self.weekly + ";" + \
            self.search + ";" + self.gamble + ";" + self.sacrifice + ";" + \
            self.snatch + ";" + self.share + ";" + str(self.cloth) + ";" + \
            str(self.inv)
