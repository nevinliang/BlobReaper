class User:
    def __init__(self, souls=[0, 0, 0], daily='|', weekly='|', search='|', gamble='|', \
        sacrifice='|', snatch='|', share='|', cloth=0):

        # souls value (pocket, sack, maxsack)
        self.souls = souls
        self.cloth = cloth

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


    def __str__(self):
        return str(self.souls) + ";" + self.daily + ";" + self.weekly + ";" + \
            self.search + ";" + self.gamble + ";" + self.sacrifice + ";" + \
            self.snatch + ";" + self.share + ";" + str(self.cloth)
