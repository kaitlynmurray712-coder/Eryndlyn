<drac2>
using(emb='72fea181-ba03-4cb4-8edf-1f3bc5a49578')
loaded = load_json(get_gvar("d10e99f5-da1e-4cff-a7b9-240cc30b6641"))

desc = "Recipes available: "
desc += "\n\n"

for x in loaded['food']:
    desc += "Name: "
    desc += loaded['food'][x]['name']
    desc += "\n"
    desc += "Ingredients: "
    for y in loaded['food'][x]['ingredient']:
        desc += y
        desc += ", "
    desc += "\n\n"

out = {
    "title": "Cooking List!",
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