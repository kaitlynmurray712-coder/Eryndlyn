from mocks import MockCharacter
from mocks import load_json, get_gvar, dump_json

character = MockCharacter


# AVRAE COMMAND
# -------------
def main(args, level):
    #args = &ARGS&
    
    args[0] = args[0].lower()
    newline = "\n"

    if character().cvars.get("bastion") is None:
        character().set_cvar("bastion","[]")
    if character().cvars.get("bastion_basic") is None:
        character().set_cvar("bastion_basic","[]")

    if level < 5:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You must be level 5 or higher to use this command" """

    # BASTION BASICS - custom prices are doubled
    # ------------------------------------------
    bastion_basic = load_json(character().cvars["bastion_basic"])
    for room_type in ["cramped", "roomy", "vast"]:
        if room_type in args[0]:
            if room_type == "cramped":
                if character().coinpurse.total < 1000:
                    return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You don't have enough gold. **{args[0].title()} Cost**: 1000 gold" """
                else:
                    character().coinpurse.modify_coins(gp=-1000, autoconvert=True)
                    bastion_basic.append(args[0])
                    character().set_cvar("bastion_basic",dump_json(bastion_basic))
                    return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "Added **{args[0].title()}** to your Bastion" """
            if room_type == "roomy":
                if character().coinpurse.total < 2000:
                    return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You don't have enough gold. **{args[0].title()} Cost**: 2000 gold" """
                else:
                    character().coinpurse.modify_coins(gp=-2000, autoconvert=True)
                    bastion_basic.append(args[0])
                    character().set_cvar("bastion_basic",dump_json(bastion_basic))
                    return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "Added **{args[0].title()}** to your Bastion" """
            if room_type == "vast":
                if character().coinpurse.total < 6000:
                    return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You don't have enough gold. **{args[0].title()} Cost**: 6000 gold" """
                else:
                    character().coinpurse.modify_coins(gp=-6000, autoconvert=True)
                    bastion_basic.append(args[0])
                    character().set_cvar("bastion_basic",dump_json(bastion_basic))
                    return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "Added **{args[0].title()}** to your Bastion" """


    gvar = load_json(get_gvar("a3dec4b0-0c72-4d05-92dd-65bb00517881"))
    if gvar.get(args[0]) is None:
        arcane = newline.join([f'!bastion add \\\"{i}\\\"' for i in gvar.keys()])
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "No such facility, valid options are:```\n{arcane} ```" """
    facility = gvar[args[0]]
    bastion = load_json(character().cvars["bastion"])

    if facility["name"] == "arcane study" and character().skills.arcana.prof < 1:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You don't have any arcane knowledge" """
    if facility["name"] == "sanctuary" and (character().skills.religion.prof < 1 and character().skills.nature.prof < 1):
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You don't have any spiritual knowledge in nature or religion" """

    if level < facility["level"]:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You must be level {facility['level']} or higher to add this facility" """

    if len(bastion) >= 6:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You can't have more than 6 facility" """

    if len(bastion) >= 5 and level < 17:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You must be level 17 or higher to add another facility" """

    if len(bastion) >= 4 and level < 13:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You must be level 13 or higher to add another facility" """

    if len(bastion) >= 2 and level < 9:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You must be level 9 or higher to add another facility" """

    if character().coinpurse.total < facility["cost"]:
        return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You don't have enough gold. **{args[0].title()} Cost**: {facility['cost']}" """

    for f in bastion:
        if args[0] == f["name"]:
            return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "You already have a {args[0]}" """

    character().coinpurse.modify_coins(gp=-facility["cost"], autoconvert=True)

    bastion.append({
        "name":args[0],
        "enlarge":False,
        "events":[]
    })

    character().set_cvar("bastion",dump_json(bastion))

    return f"""embed -title "!bastion add \\\"{args[0]}\\\"" -desc "Added {args[0]}" """