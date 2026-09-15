<drac2> 

using(emb='72fea181-ba03-4cb4-8edf-1f3bc5a49578')
loaded = load_json(get_gvar("8f90e6ce-ba2d-4fde-8e24-c9727cbbdf08"))
using(toolthings="6251e20c-7545-4c63-92af-31e0745f2b0c") # loads shit
tools= load_json(get_gvar("20d9ca50-b215-45bb-beae-c6e558c3eebb")) #loads more shit
char = character()

#--Input--#
inp = "&1&"

#load bag info
using(baglib='4119d62e-6a98-4153-bea9-0a99bb36da2c')
bags = baglib.load_bags()
#!----!

#--wizardy I dont get--#
a =argparse(&ARGS&)
adv = a.adv(boolwise=True)
reroll_number = char.csettings.get("reroll", None)
minimum_check = a.last('mc', None, int) or (10 if char.csettings.get("talent", False) and char.skills[tool].prof>=1 else None)
bonus = (''.join(a.get('b', type_=lambda x: "+"+x if x[0] not in "+-" else x))) + ('+1d4' if a.get('guidance') else '')
#--wizardy I dont get--#

for x in loaded['drink']:
    if str(inp) in x:
        finalinp = x
        break

drink = loaded['drink'][finalinp]['name']
hpt = loaded['drink'][finalinp]['bonus']
drinkdc = loaded['drink'][finalinp]['dc']
desc = "You have a craving for "
desc += drink
desc += "!"
desc += "\n\n"
if baglib.find_bag_with_item(bags, item=drink):
    baglib.modify_item(bags, item=drink, quantity= -1, create_on_fail=False)
    baglib.save_bags(bags)
    char.set_temp_hp(hpt)
    desc += "You consumed a(n) "
    desc += drink
    desc += "."
    desc += "\n"

    minimum_check = a.last('mc', None, int) or (10 if char.csettings.get("talent", True) and char.skills['athletics'].prof>=1 else None)
    consave = vroll(character().saves.get("con").d20(adv, reroll_number, minimum_check,))

    desc += "**Consitution Save:** "
    desc += consave
    desc += " **"
     
    if int(consave.total) >= int(drinkdc):
        desc += "PASS**"
        desc += "\n\n"
        desc += "You gained "
        desc += hpt
        desc += "thp."
    else:
        desc += "FAIL**"
        if char.cc_exists("Drunkeness"):
            char.mod_cc("Drunkeness", 1)
        else:
            char.create_cc_nx("Drunkeness", 0, 6, "long", "bubble", 0, None,"Drunkeness")
            char.mod_cc("Drunkeness", 1)
        drunklvl = char.cc("Drunkeness")
        desc +=  "\n\n"
        desc +=  "**__Drunkeness Level__**"
        desc +=  "\n"
        desc +=  drunklvl
        drunktotal = char.get_cc(("Drunkeness"))
        if drunktotal == 1:
            desc += "\n"
            desc += "You are **tipsy**! Gain Advantage on Charisma based checks and saving throws."
        elif drunktotal == 2:
            desc += "\n"
            desc += "You are **buzzed**! Take Disadvantage on all Dexterity based checks and saving throws. Gain Advantage on all Strength based checks and saving throws."
        elif drunktotal == 3: 
            desc += "\n"
            desc += "You are **drunk**! Gain the Poisoned condition."
        elif drunktotal == 4: 
            desc += "\n"
            desc += "You are **black out drunk**! No memory of events during this phase."
        elif drunktotal == 5: 
            desc += "\n"
            desc += "You are **pass out drunk**! Roll a d4, evens you are still standing, odds you pass out."
        elif drunktotal == 6: 
            desc += "\n"
            desc += "Please roll death saves."
        desc +=  "\n"
        desc +=  "-# Get to drunkeness level 6 and start rolling death saves!"
else:
    desc += "You do not have that in your bag."



out = {
    "title": "Drink up!",
    "footer":"Made by Kait296 | !drink <recipe>",
    "desc": desc
    }
return emb.get_output(out)

</drac2>