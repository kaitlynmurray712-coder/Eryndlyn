<drac2> 

using(emb='72fea181-ba03-4cb4-8edf-1f3bc5a49578')
loaded = load_json(get_gvar("4b8234ad-0069-4d29-8c2e-5f9e69106c61"))
using(toolthings="6251e20c-7545-4c63-92af-31e0745f2b0c") # loads shit
tools= load_json(get_gvar("20d9ca50-b215-45bb-beae-c6e558c3eebb")) #loads more shit
char = character()

#--Input--#
inp = "&1&"

#load bag info
using(baglib='4119d62e-6a98-4153-bea9-0a99bb36da2c')
bags = baglib.load_bags()
#!----!

for x in loaded['food']:
    if str(inp) in x:
        finalinp = x
        break

eat = loaded['food'][finalinp]['name']
hpt = loaded['food'][finalinp]['bonus']
desc = "You have a craving for "
desc += eat
desc += "!"
desc += "\n\n"
if baglib.find_bag_with_item(bags, item=eat):
    baglib.modify_item(bags, item=eat, quantity= -1, create_on_fail=False)
    baglib.save_bags(bags)
    char.modify_hp(hpt, overflow=False)
    desc += "You consumed a(n) "
    desc += eat
    desc += "."
    desc += "\n"
    desc += "You gained "
    desc += hpt
    desc += "hp."
else:
    desc += "You do not have that in your bag."



out = {
    "title": "Eat up!",
    "footer":"Made by Kait296 | !eat <recipe>",
    "desc": desc
    }
return emb.get_output(out)

</drac2>