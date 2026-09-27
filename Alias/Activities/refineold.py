embed
<drac2>
using(toolthings="6251e20c-7545-4c63-92af-31e0745f2b0c") # loads shit
tools= load_json(get_gvar("20d9ca50-b215-45bb-beae-c6e558c3eebb")) #loads more shit

char = character()
inp1 = "&1&"
inp2 = "&2&"
#--wizardy I dont get--#
a =argparse(&ARGS&)
adv = a.adv(boolwise=True)
reroll_number = char.csettings.get("reroll", None)

#--wizardy I dont get--#

loot = {
    "iron":{"name":"Iron","produce":4, "dc":10, "tier":"t1", "worth":150},
    "silver":{"name":"Silver","produce":2, "dc":10, "tier":"t1", "worth":300},
    "amber":{"name":"Amber","produce":1, "dc":10, "tier":"t1", "worth":100},
    "emerald":{"name":"Emerald","produce":2, "dc":10, "tier":"t1", "worth":200},
    "topaz":{"name":"Topaz","produce":2, "dc":10, "tier":"t1", "worth":112},
    "peridot":{"name":"Peridot","produce":2, "dc":10, "tier":"t1", "worth":260},
    "obsidian":{"name":"Obsidian","produce":2, "dc":15, "tier":"t2", "worth":200},
    "mithril":{"name":"Mithril","produce":2, "dc":15, "tier":"t2", "worth":300},
    "sapphire":{"name":"Sapphire","produce":1, "dc":15, "tier":"t2", "worth":250},
    "moonstone":{"name":"Moonstone","produce":2, "dc":15, "tier":"t2", "worth":4250},
    "jade":{"name":"Jade","produce":2, "dc":15, "tier":"t2", "worth":500},
    "amethyst":{"name":"Amethyst","produce":2, "dc":15, "tier":"t2", "worth":350},
    "gold":{"name":"Gold","produce":4, "dc":20, "tier":"t3", "worth":500},        
    "diamond":{"name":"Diamond","produce":1, "dc":25, "tier":"t3", "worth":25000},
    "adamantine":{"name":"Adamantine","produce":1, "dc":20, "tier":"t3", "worth":5000},
    "mizzium":{"name":"Mizzium","produce":2, "dc":20, "tier":"t3", "worth":2500},
    "opal":{"name":"Opal","produce":2, "dc":25, "tier":"t3", "worth":1100},
    "sunstone":{"name":"Sunstone","produce":2, "dc":25, "tier":"t3", "worth":2500},
    "quartz":{"name":"Quartz","produce":2, "dc":12, "tier":"t1","worth":100},
    "copper":{"name":"Copper","produce":4,"dc":16, "tier":"t2","worth":150},
    "platinum":{"name":"Platinum","produce":1,"dc":22, "tier":"t3","worth":1000},
    "onyx":{"name":"Onyx","produce":1,"dc":10, "tier":"t1","worth":100},
    "lead":{"name":"Lead","produce":1,"dc":10, "tier":"t1","worth":100},
    "agate":{"name":"Agate","produce":1, "dc":15, "tier":"t2", "worth":250},
    "jacinth":{"name":"Jacinth","produce":1, "dc":15, "tier":"t2", "worth":250},
    "ruby":{"name":"Ruby","produce":1, "dc":20, "tier":"t3", "worth":1000},
    "mercury":{"name":"Mercury","produce":2, "dc":20, "tier":"t3", "worth":1000}
}
if char.get_cc("Activity Points") >= int(inp2):
    char.mod_cc("Activity Points", -int(inp2))
    if inp1 == "silver" or inp1 == "gold" or inp1 == "mithril"or inp1 == "adamantine" or inp1 == "mizzium" or inp1 == "iron":
        toolNeeded = "smith"
    else:
        toolNeeded = "jeweler"
    temp = str(toolthings.matching_tools(toolNeeded)) #sees if a tool is in the tool directory
    toolKey = temp.strip("[]'") #removes unnecessary shit
    temp = tools[toolKey]['modifier'] #gets the ability
    abi = temp.rstrip("Mod") #strips Mod from ability
    if toolNeeded.lower() in char.get_cvar('pTools').lower():
        profi = char.stats.prof_bonus
        pe = 1
    elif toolNeeded.lower() in char.get_cvar('eTools').lower():
        profi = char.stats.prof_bonus*2
        pe = 2
    else:
        pe = 0
        profi = 0
    minimum_check = a.last('mc', None, int) or (10 if char.csettings.get("talent", True) and char.skills[abi].prof>=1 else None)
    bonus = (''.join(a.get('b', type_=lambda x: "+"+x if x[0] not in "+-" else x))) + ('+1d4' if a.get('guidance') else '')
    checkDC = loot[inp1]['dc']
    qty = randint(loot[inp1]['produce'])+1
    quality = randint(1,loot[inp1]['worth'])
    totalgp = quality*int(inp2)
    rolled = vroll(char.skills[abi].d20(adv, reroll_number, minimum_check,)+bonus)
    total = rolled.total + profi

    desc = "You are refining **"
    desc += loot[inp1]['name']
    desc += "**!"

    desc += "\n\n"
    desc +="**"
    desc += tools[toolKey]['name']
    desc += " Tools Check**: "
    desc += rolled
    total = rolled.total
    if pe == 1:
        desc += "\n"
        desc += "**Proficiency Bonus**:  "
        desc += profi
        total = total + profi
        desc += "\n"
        desc += "**Total**: "
        desc += total
    elif pe == 2:
        desc += "\n"
        desc += "**Expertise Bonus**: "
        desc += profi
        total = total + profi
        desc += "\n"
        desc += "**Total**: "
        desc += total
    else:
        pe = 0

    if total >= loot[inp1]['dc']:
        desc += " **PASS**"
        desc += "\n\n"
        desc += "You refined a total of **"
        desc += inp2
        desc += " "
        desc += loot[inp1]['name']
        desc += "** worth **"
        desc += totalgp
        desc += "gp**!"
    else:
        desc += " **FAIL**"
        desc += "\n\n"
        desc += "You destroyed the "
        desc += loot[inp1]['name']
        desc += "!"
    ap = char.cc("Activity Points")
    desc += "\n\n"
    desc += "Activity Points"
    desc += "\n"
    desc += ap
else:
    desc = "You do not have enough AP for this activity! Go rest."    




</drac2>
-title "Refining your mined goods!"
-desc "{{desc}}"