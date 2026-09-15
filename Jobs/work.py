embed
<drac2>
using(toolthings="6251e20c-7545-4c63-92af-31e0745f2b0c") # loads shit
tools= load_json(get_gvar("20d9ca50-b215-45bb-beae-c6e558c3eebb")) #loads more shit

inp1 = "&1&" #check/tool
char = character() #self explanitory
wage = 2

#--wizardy I dont get--#
a =argparse(&ARGS&)
adv = a.adv(boolwise=True)
reroll_number = char.csettings.get("reroll", None)
minimum_check = a.last('mc', None, int) or (10 if char.csettings.get("talent", False) and char.skills[abi].prof>=1 else None)
bonus = (''.join(a.get('b', type_=lambda x: "+"+x if x[0] not in "+-" else x))) + ('+1d4' if a.get('guidance') else '')
#--wizardy I dont get--#
# --- SKILLS --- #
options = { 
        "acrobatics":"acrobatics",
        "animal handling":"animalHandling",
        "arcana":"arcana",
        "athletics":"athletics",
        "deception":"deception",
        "history":"history",
        "insight":"insight",
        "intimidation":"intimidation",
        "investigation":"investigation",
        "medicine":"medicine",
        "nature":"nature",
        "perception":"perception",
        "performance":"performance",
        "persuasion":"persuasion",
        "religion":"religion",
        "sleight of hand":"sleightOfHand",
        "stealth":"stealth",
        "survival":"survival"
    }
# Tool or skill?
#inputList = inp1
if char.get_cc("Activity Points") >= 8:
    char.mod_cc("Activity Points", -8)
    if inp1.lower() in options.values():
        abi = inp1.lower()
        profi = 0
        skilltext = abi
    elif inp1.lower() == "help":
        desc = "Oh hello! You need help. For `!work` to function, you must either choose a skill or alternitively a tool in which you are proficient in."
        desc += "\n\n"
        desc += "`!work <skill/tool>`"
    else:
        temp = str(toolthings.matching_tools(inp1)) #sees if a tool is in the tool directory
        toolKey = temp.strip("[]'") #removes unnecessary shit
        temp = tools[toolKey]['modifier'] #gets the ability
        abi = temp.rstrip("Mod") #strips Mod from ability
        if inp1.lower() in char.get_cvar('pTools').lower():
            profi = char.stats.prof_bonus
        elif inp1.lower() in char.get_cvar('eTools').lower():
            profi = char.stats.prof_bonus*2
        else:
            profi = 0
        skilltext = str(toolthings.tool_name_for(toolKey))

    #-- Rolling dice etc--#
    rolled = vroll(char.skills[abi].d20(adv, reroll_number, minimum_check,)+bonus)  #rolls the dice
    total = rolled.total + profi  #adds prof
    desc = "You're working hard!"
    desc += "\n"
    desc += "You're using "
    desc += skilltext
    desc += " for your wages."
    desc += "\n"
    gold = total*wage
    desc += "__Income__: "
    desc += gold
    desc += "gp"
    char.coinpurse.modify_coins(gp=gold)
    coinpouch = char.coinpurse.total
    desc += "\n\n"
    desc += "**__Your Total Coins__**: "
    desc += coinpouch
    desc += "gp"
    ap = char.cc("Activity Points")
    desc += "\n\n"
    desc += "Activity Points"
    desc += "\n"
    desc += ap
else:
    desc = "You do not have enough AP for this activity! Go rest."
</drac2>
-desc "{{desc}}
"
-title "__Working Wage__"
-footer "Made by Kait296, help by hatenull, idea by AdinX | !work <tool/skill>"