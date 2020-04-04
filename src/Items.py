class Items:
    scythe = ['tool', 'Scythe 5%', 'Reinforced Scythe 10%', 'Enhanced Scythe 15%', \
        'Ancient scythe 20%', 'Mystical Scythe 40%']
    shrine = ['tool', 'Shrine +10 soul stones', 'Altar +25 soul stones', \
        'Chapel +50 soul stones', 'Temple +100 soul stones', 'Sanctum +500 soul stones']
    forge = ['tool', 'Forge +25 soul stones', 'Workshop +50 soul stones', \
        'Assembly Line +100 soul stones', 'Factory +200 soul stones', \
        'Vortex +1000 soul stones']

    pscythe = [2000, 5000, 10000, 50000, 200000]
    pshrine = [500, 1500, 4000, 8000, 25000]
    pforge = [1500, 4000, 10000, 25000, 150000]

    items = {'scythe': (0, scythe, pscythe), 'shrine': (1, shrine, pshrine), 'forge': (2, forge, pforge)}

    # include detailed shop right Here
    store_dets = {  "scythe": """scythe: increases the percentage stolen from any person by\n
                        - scythe 5%\t\t2K soul stones\n
                        - reinforced scythe 10%\t\t5K soul stones\n
                        - enhanced scythe 15%\t\t10K soul stones\n
                        - ancient scythe 20%\t\t50K soul stones\n
                        - mystical scythe 40%\t\t200K soul stones""",

                    "shrine": """increases souls you get from sacrificing\n
                        - shrine +10 soul stones\t\t500 soul stones\n
                        - altar +25 soul stones\t\t1500 soul stones\n
                        - chapel +50 soul stones\t\t4K soul stones\n
                        - temple +100 soul stones\t\t 8K soul stones\n
                        - sanctum + 500 soul stones\t\t25K soul stones""",

                    "forge": """gives u souls every hour\n
                        - forge +25 soul stones\t\t1500 soul stones\n
                        - workshop +50 soul stones\t\t4K soul stones\n
                        - assembly line +100 soul stones\t\t10K soul stones\n
                        - factory +200 soul stones\t\t25K soul stones\n
                        - vortex + 1000 soul stones\t\t150K soul stones"""}



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
