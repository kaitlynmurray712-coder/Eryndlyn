embed 
<drac2>
    
char = character()
#--wizardy I dont get--#
a =argparse(&ARGS&)
adv = a.adv(boolwise=True)
reroll_number = char.csettings.get("reroll", None)
inp = "&1&"
location = char.get_cvar("currentLocation")
home = "direshore"

bonus = (''.join(a.get('b', type_=lambda x: "+"+x if x[0] not in "+-" else x))) + ('+1d4' if a.get('guidance') else '')
#--wizardy I dont get--#
desc = ""
encounter = load_json(get_gvar("9a5b820c-3fed-483a-87a4-90d6db7f6ccb"))
encounters = encounter["lumber"]

item1 = load_json(get_gvar("fb427db3-3932-416d-b324-25b7757b6829"))
item = item1["lumber"]

event = load_json(get_gvar("9d85bbc9-7738-46a7-87dc-b4fcf2a0596f"))
events = event["lumber"]

## Choose your Adventure
choose = str(vroll('d6').total)
#d6, 1-nada, 2-event, 3-encounter, 4-6-item
if inp == "1" or inp == "2" and currentLocation == home or inp == "4" and currentLocation == home:
    
    if char.get_cc("Activity Points") >= int(inp):
        char.mod_cc("Activity Points", -int(inp))
        if choose == "1":
            desc = "You have looked and found nothing. Better luck next time!"
        elif choose == "2": ## EVENT
            whichevent = str(vroll('d3').total)
            chosenevent = events[str(inp)][whichevent]
            desc += "**Your party finds themself faced with:** "
            desc += "\n"
            desc += chosenevent['description']
            desc += "\n\n"

            minimum_check = a.last('mc', None, int) or (10 if char.csettings.get("talent", True) and char.skills[chosenevent['check']].prof>=1 else None)
            saveroll = vroll(char.skills[chosenevent['check']].d20(adv, reroll_number, minimum_check, )+bonus)

            desc += "**DC:** "
            desc += " 15"
            desc += "\n\n"
            desc += "**Check:** "
            desc += chosenevent['check'].title()
            desc += "\n"
            desc += "**Roll:** "
            desc += saveroll
            if int(saveroll.total) >= 20:
                desc += " **PASS**"
                desc += "\n\n"
                desc += chosenevent["highpass"]
            elif int(saveroll.total) > 14 and int(saveroll.total) < 20:
                desc += "**LOW PASS**"
                desc += "\n\n"
                desc += chosenevent["midpass"]
            else:
                desc += " **FAIL**"
                desc += "\n\n"
                desc += chosenevent["fail"]
            
            desc += "\n\n"
            desc += "``` Damage and items from this are *NOT* added to your character```"
            

        elif choose == "3": ## ENCOUNTER
            whichencounter = str(vroll('d5').total)
            chosenencounter = encounters[str(inp)][whichencounter]

            desc += chosenencounter["description"]
            desc += "\n\n"
            desc += "Monsters:"
            desc += "\n"
            desc += chosenencounter["encounter"]
            desc += "\n\n"
            desc += "**Stealth:**"

            minimum_check = a.last('mc', None, int) or (10 if char.csettings.get("talent", True) and char.skills['stealth'].prof>=1 else None)
            stealthroll = vroll(char.skills['stealth'].d20(adv, reroll_number, minimum_check, )+bonus)
            dc = int(inp)*3
            desc += stealthroll
            
            if stealthroll.total >= dc:
                desc += " **PASS**"
                desc += "\n"
                desc += "You were able to sneak up on them. Surprise round or disengage and leave?"
            else: 
                desc += " **FAIL**"
                desc += "\n"
                desc += "You were not able to sneak closer. Engage or Disengage?"

        elif choose == "4"  or choose == "5" or choose == "6": ## ITEM
            whichitem = str(vroll('d8').total)
            chosenitem = item[str(inp)][str(whichitem)]

            minimum_check = a.last('mc', None, int) or (10 if char.csettings.get("talent", True) and char.skills['stealth'].prof>=1 else None)
            athleticsroll = vroll(char.skills['survival'].d20(adv, reroll_number, minimum_check, )+bonus)

            desc += "**You found:** "
            desc += chosenitem['name']
            desc += "\n"
            desc += "**DC:** "
            desc += chosenitem['dc']
            desc += "\n\n"
            desc += "**Survival Check:** "
            desc += athleticsroll
            if athleticsroll.total >= chosenitem['dc']:
                desc += " **PASS**"
                qty = vroll(chosenitem['produce']).total

                desc += "\n\n"
                desc += "**Quantity Found:** "
                desc += qty
            
                using(baglib='4119d62e-6a98-4153-bea9-0a99bb36da2c')
                bags = baglib.load_bags()
                baglib.modify_item(bags, item=chosenitem['name'], quantity= qty, bag_name= 'Chopped', create_on_fail=True)
                baglib.save_bags(bags)
            else: 
                desc += " **FAIL**"
            

        else: ## Fuck
            desc = "Ooop! You found an error... let Kait know..."
            desc += "\n\n"
            desc += inp
            desc += "\n"
            desc += choose

        ap = char.get_cc("Activity Points")
        desc += "\n\n"
        desc += "**Activity Points**"
        desc += "\n"
        desc += ap 
        desc += " (-"
        desc += inp
        desc += ")"
    else:
        desc = "You are not currently in the correct location for this action or you have not put in an accurate amount of ap."
        desc += "\n\n"
        desc += "This activity may be done: "
        desc += home.title()
        desc += "\n"
        desc += "You are currecntly: "
        desc += location.title()

</drac2>
-title "Thwack! Thwack! TIMBER! {{char.name}} is cutting down trees!"
-desc "{{desc}}"
-thumb "https://media.discordapp.net/attachments/1242971481584042104/1507954391402025071/aaa601.jpg"
-footer "made by Erndlyn Creative and IT Departments"