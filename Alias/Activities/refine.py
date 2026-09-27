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

loot = load_json(get_gvar("fb427db3-3932-416d-b324-25b7757b6829"))


if char.get_cc("Activity Points") >= int(inp2):
    char.mod_cc("Activity Points", -int(inp2))
    

    search = inp1.title().strip()
    found = None

    for location, tiers in loot.items():
        for tier, entries in tiers.items():
            for entry, item in entries.items():
                if search in item["name"].title():
                    found = {
                        "location": location,
                        "tier": tier,
                        "entry": entry,
                        "item": item
                    }
                    break
            if found:
                break
        if found:
            break

    if not found:
        desc = f"Could not find `{inp1}` in the loot table."
    else:
        location = found["location"]
        tier = found["tier"]
        entry = found["entry"]
        item = found["item"]


    toolNeeded = loot[location][tier][entry]['tool']
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
    checkDC = loot[location][tier][entry]['dc']
    qty = randint(loot[location][tier][entry]['produce'])+1
    quality = randint(1,loot[location][tier][entry]['worth'])
    totalgp = quality*int(inp2)
    rolled = vroll(char.skills[abi].d20(adv, reroll_number, minimum_check,)+bonus)
    total = rolled.total + profi

    desc = "You are refining **"
    desc += loot[location][tier][entry]['name']
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

    if total >= loot[location][tier][entry]['dc']:
        desc += " **PASS**"
        desc += "\n\n"
        desc += "You refined a total of **"
        desc += inp2
        desc += " "
        desc += loot[location][tier][entry]['refined']
        desc += "** worth **"
        desc += totalgp
        desc += "gp**!"
    else:
        desc += " **FAIL**"
        desc += "\n\n"
        desc += "You destroyed the "
        desc += loot[location][tier][entry]['name']
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