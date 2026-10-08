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
        return f"""embed -title "!bastion enlarge \\\"{args[0]}\\\"" -desc "You must be level 5 or higher to use this command" """

    gvar = load_json(get_gvar("a3dec4b0-0c72-4d05-92dd-65bb00517881"))

    if gvar.get(args[0]) is None:
        arcane = newline.join([f'!bastion enlarge \\\"{i}\\\"' for i in gvar.keys()])
        return f"""embed -title "!bastion enlarge \\\"{args[0]}\\\"" -desc "No such facility, valid options are:```\n{arcane} ```" """
    bastion = load_json(character().cvars["bastion"])

    for i in bastion:
        if i["name"] == args[0]:
            if i["enlarge"]:
                return f"""embed -title "!bastion enlarge \\\"{args[0]}\\\"" -desc "That facility is already fully upgraded" """
            if character().coinpurse.total < 2000:
                return f"""embed -title "!bastion enlarge \\\"{args[0]}\\\"" -desc "You don't have enough gold. Costs 2000 gold" """
            i["enlarge"] = True
            character().coinpurse.modify_coins(gp=-2000, autoconvert=True)
            character().set_cvar("bastion",dump_json(bastion))
            return f"""embed -title "!bastion enlarge \\\"{args[0]}\\\"" -desc "Upgraded" """

    return f"""embed -title "!bastion enlarge \\\"{args[0]}\\\"" -desc "You don't own that facility" """
