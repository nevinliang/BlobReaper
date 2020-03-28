class User:
    def __init__(self, souls=0, daily='|', weekly='|', search='|', gamble='|', \
        sacrifice='|', snatch='|', share='|', cloth=0):
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


    def __str__(self):
        return str(self.souls) + " " + self.daily + " " + self.weekly + " " + \
            self.search + " " + self.gamble + " " + self.sacrifice + " " + \
            self.snatch + " " + self.share + " " + str(self.cloth)
