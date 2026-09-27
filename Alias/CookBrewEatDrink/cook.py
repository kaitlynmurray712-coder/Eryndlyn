<drac2>
using(emb='72fea181-ba03-4cb4-8edf-1f3bc5a49578')
loaded = load_json(get_gvar("d10e99f5-da1e-4cff-a7b9-240cc30b6641"))
using(toolthings="6251e20c-7545-4c63-92af-31e0745f2b0c") # loads shit
tools= load_json(get_gvar("20d9ca50-b215-45bb-beae-c6e558c3eebb")) #loads more shit
char = character()


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

#-- User input--#
item = "&1&"
qty = "&2&"
#-- end -- #
if char.get_cc("Activity Points") > 1:
    char.mod_cc("Activity Points", -1)
    for x in loaded['food']:
        if str(item) in x:
            finalinp = x
            break
        else: 
            finalinp = "fail"
    if finalinp != "fail":
        temp = 0
        itemname = loaded['food'][finalinp]['name']
        itemingredients = loaded['food'][finalinp]['ingredient']
        itemdc = loaded['food'][finalinp]['dc']
        tool = "Cook's Utensils"

        if tool.lower() in char.get_cvar('pTools').lower():
            profi = char.stats.prof_bonus
        elif tool.lower() in char.get_cvar('eTools').lower():
            profi = char.stats.prof_bonus*2
        else:
            profi = 0


        temp = str(toolthings.matching_tools(tool)) #sees if a tool is in the tool directory
        toolKey = temp.strip("[]'") #removes unnecessary shit
        temp = tools[toolKey]['modifier'] #gets the ability
        abi = temp.rstrip("Mod") #strips Mod from ability


        rolled = vroll(char.skills[abi].d20(adv, reroll_number, minimum_check,)+bonus)  #rolls the dice
        total = rolled.total + profi

        desc = "You want to try your hand at cooking for friends?"
        desc += "\n\n"
        desc += "Cook's Utensils Check: "
        desc += rolled
        desc += "\n"
        desc += "Proficency/Expertise Bonus: "
        desc += profi
        desc += "\n"
        desc += "Total: "
        desc += total 
        if total >= itemdc:
            desc += " **PASS**"
            desc += "\n\n"
            desc += "__Ingredients__:"
            desc += "\n"
            for x in loaded['food'][finalinp]['ingredient']:
                if baglib.find_bag_with_item(bags, item=x):
                    baglib.modify_item(bags, item=x, quantity= -int(qty), create_on_fail=False)
                    baglib.save_bags(bags)
                    temp1 = temp
                    temp = temp1 + 1
                    desc += x
                    desc += "\n"
                else:
                    break
            desc += "\n\n"
            desc += "You successfully made "
            desc += qty
            desc += " "
            desc += itemname
            desc += "!"
            if temp == 2:
                baglib.modify_item(bags, item=itemname, quantity= int(qty),bag_name= 'Food and Drink', create_on_fail=False)
                baglib.save_bags(bags)
        else:
            desc += " **FAIL**"
            desc += " \n\n"
            desc += "You were unsuccessful in making the check and burnt the food."
    else:
        desc = "You have entered and invalid input."
    ap = char.cc("Activity Points")
    desc += "\n\n"
    desc += "Activity Points"
    desc += "\n"
    desc += ap
else:
    desc = "You do not have enough AP for this activity! Go rest."

out = {
    "title": "Cooking!",
    "footer":"Made by Kait296 | !cook <recipe> <qty>",
    "fields": [
    {
        "body": desc,
        "inline": True
    }
    ]

    }
return emb.get_output(out)
</drac2>