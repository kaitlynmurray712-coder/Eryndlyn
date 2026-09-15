<drac2>
using(emb='72fea181-ba03-4cb4-8edf-1f3bc5a49578')
loaded = load_json(get_gvar("8f90e6ce-ba2d-4fde-8e24-c9727cbbdf08"))

desc = "Items Available: "
desc += "\n\n"
desc += "__Swordsman__"
desc += "\n"
for x in loaded['swordsman']:
    desc += "Name: "
    desc += loaded['swordsman'][x]['name']
    desc += "\n"
    desc += "Price: "
    desc += loaded['swordsman'][x]['price']
    desc += " sp"
    desc += "\n"
desc += "\n"
desc += "__Rook__"
desc += "\n"
for x in loaded['rook']:
    desc += "Name: "
    desc += loaded['rook'][x]['name']
    desc += "\n"
    desc += "Price: "
    desc += loaded['rook'][x]['price']
    desc += " sp"
    desc += "\n"
desc += "\n"
desc += "__Sleeping__"
desc += "\n"
for x in loaded['sleeping']:
    desc += "Name: "
    desc += loaded['sleeping'][x]['name']
    desc += "\n"
    desc += "Price: "
    desc += loaded['sleeping'][x]['price']
    desc += " sp"
    desc += "\n"
desc += "\n"
desc += "__Horseshoe__"
desc += "\n"
for x in loaded['horseshoe']:
    desc += "Name: "
    desc += loaded['horseshoe'][x]['name']
    desc += "\n"
    desc += "Price: "
    desc += loaded['horseshoe'][x]['price']
    desc += " sp"
    desc += "\n"
desc += "\n"
desc += "__Drinks__"
desc += "\n"
for x in loaded['drink']:
    desc += "Name: "
    desc += loaded['drink'][x]['name']
    desc += "\n"
    desc += "Price: "
    desc += loaded['drink'][x]['price']
    desc += " sp"
    desc += "\n"
desc += "\n"

out = {
    "title": "Order List!",
    "footer":"Made by Kait296 | !order <recipe>",
    "fields": [
    {
        "body": desc,
        "inline": True
    }
    ]

    }
return emb.get_output(out)
</drac2>