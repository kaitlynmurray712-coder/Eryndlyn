embed
<drac2>
using(baglib='4119d62e-6a98-4153-bea9-0a99bb36da2c')

# Load item data
items = load_json(get_gvar("0e282419-c4c3-4956-a859-36fce7b352c3"))

# Load character and bags
char = character()
bags = baglib.load_bags()

# Argument - full item name e.g. "Ration:Beast CR5"
item_name = "&*&"

# Check if item exists in the description data
if item_name not in items:
    title = "Unknown Item"
    desc = "**" + item_name + "** is not a recognized ration."
    desc += "\n"
    desc += "Double check the name and try again."
    desc += "\n\n"
    desc += "Format: `Ration:[Type] CR[number]`"
    desc += "\n"
    desc += "Example: `Ration:Beast CR5`"

# Check if item exists in the bag
elif not baglib.find_bag_with_item(bags, item=item_name):
    title = "Item Not Found"
    desc = "You don't have any **" + item_name + "** in your bags."
    desc += "\n"
    desc += "Make sure it has been cooked and stored first."

# Item found - consume it
else:
    item_data = items[item_name]

    # Remove 1 from bag
    baglib.modify_item(bags, item=item_name, quantity=-1)
    baglib.save_bags(bags)

    # Build output
    title = char.name + " eats: " + item_name

    desc = "***" + item_data["flavor"] + "***"
    desc += "\n\n"
    desc += "**Type:** " + item_data["type"]
    desc += "\n"
    desc += "**CR:** " + item_data["cr"]
    desc += "\n\n"
    desc += "**Effect:** " + item_data["effect"]
</drac2>
-title "{{title}}"
-desc "{{desc}}"
-footer "Use !bag to check your inventory"