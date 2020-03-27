class User:
    def __init__(self, money=0, daily='|', weekly='|', beg='|', bet='|', work='|', snatch='|'):
        self.money = money

        # these are all times
        self.daily = daily
        self.weekly = weekly
        self.beg = beg
        self.bet = bet
        self.work = work
        self.snatch = snatch

    def __str__(self):
        return str(self.money) + " " + self.daily + " " + self.weekly + " " + self.beg + " " + self.bet + " " + self.work + " " + self.snatch
