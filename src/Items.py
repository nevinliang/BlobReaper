class Items:
    scythe = ['tool', 'Scythe 5%', 'Reinforced Scythe 10%', 'Enhanced Scythe 15%', \
        'Ancient scythe 20%', 'Mysitcal Scythe 40%']
    shrine = ['tool', 'Shrine +10 soul stones', 'Altar +25 soul stones', \
        'Chapel +50 soul stones', 'Temple +100 soul stones', 'Sanctum +500 soul stones']
    forge = ['tool', 'Forge +25 soul stones', 'Workshop +50 soul stones', \
        'Assembly Line +100 soul stones', 'Factory +200 soul stones', \
        'Vortex +1000 soul stones']


    items = {'scythe': (0, scythe), 'shrine': (1, shrine), 'forge': (2, forge)}

    # include detailed shop right Here
    store_dets = {  "scythe": """scythe: increases the percentage stolen from any person by\n
                        - scythe 5%\n
                        - reinforced scythe 10%\n
                        - enhanced scythe 15%\n
                        - ancient scythe 20%\n
                        - mystical scythe 40%""",

                    "shrine": """increases souls you get from sacrificing\n
                        - shrine +10 soul stones\n
                        - altar +25 soul stones\n
                        - chapel +50 soul stones\n
                        - temple +100 soul stones\n
                        - sanctum + 500 soul stones""",

                    "forge": """gives u souls every hour\n
                        - forge +25 soul stones\n
                        - workshop +50 soul stones\n
                        - assembly line +100 soul stones\n
                        - factory +200 soul stones\n
                        - vortex + 1000 soul stones"""}



    def listinv(lscythe, lshrine, lforge):
        ret_str = ""
        if lscythe != 0:
            ret_str += 'Scythe: Level ' + str(lscythe) + ' ' + Items.scythe[lscythe] + '\n'
        if lshrine != 0:
            ret_str += 'Shrine: Level ' + str(lshrine) + ' ' + Items.shrine[lshrine] + '\n'
        if lforge != 0:
            ret_str += 'Forge: Level ' + str(lforge) + ' ' + Items.forge[lforge] + '\n'
        if ret_str == "":
            ret_str += "You're a noob reaper. You have nothing."
        return ret_str
