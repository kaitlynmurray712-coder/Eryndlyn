embed
<drac2>
using(emb='72fea181-ba03-4cb4-8edf-1f3bc5a49578')
loaded = load_json(get_gvar("8f90e6ce-ba2d-4fde-8e24-c9727cbbdf08"))
using(toolthings="6251e20c-7545-4c63-92af-31e0745f2b0c") # loads shit
tools= load_json(get_gvar("20d9ca50-b215-45bb-beae-c6e558c3eebb")) #loads more shit
char = character()


#load bag info
using(baglib='4119d62e-6a98-4153-bea9-0a99bb36da2c')
bags = baglib.load_bags()
#!----!

#-- User input--#
location = "&1&"
item = "&2&"
qty = "&3&"
#-- end -- #

for x in loaded:
    if str(location) in x:
        finallocation = x
        break
    else: 
        finallocation = "no"
for x in loaded[finallocation]:
    if str(item) in x:
        finalitem = x
        break
    else:
        finalitem = "fail"

if finallocation != "no":
    if finalitem != "fail":
        itemname = loaded[finallocation][finalitem]["name"]
        itemprice = loaded[finallocation][finalitem]["price"]
        baglib.modify_item(bags, item=itemname, quantity= int(qty), create_on_fail=True,)
        baglib.save_bags(bags)
        total = int(itemprice)*int(qty)
        char.coinpurse.modify_coins(sp= -int(total))
        desc = "You ordered "
        desc += itemname
        desc += ". A waitor has brought this to you."
        desc += "\n\n"
        desc += "Your total was "
        desc += total
        desc += "sp. You remove the silver from your coinpurse paying the waitor."
    else: 
        desc = "You have entered an incorrect location or menu item."
else:
    desc = "Incorrect place selected."

</drac2>
-title "Oder Food/Drink"
-desc "{{desc}}"
-footer "Made by Kait296 | !order location item qty"

