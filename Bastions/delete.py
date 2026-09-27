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
    

    bastion_basic = load_json(character().cvars["bastion_basic"])
    for room_type in ["cramped", "roomy", "vast"]:
        if room_type in args[0]:
            if args[0] in bastion_basic:
                bastion_basic.remove(args[0])
                character().set_cvar("bastion_basic",dump_json(bastion_basic))
                return f"""embed -title "!bastion delete \\\"{args[0]}\\\"" -desc "Deleted" """
            else:
                return f"""embed -title "!bastion delete \\\"{args[0]}\\\"" -desc "You don't have that facility" """

    gvar = load_json(get_gvar("a3dec4b0-0c72-4d05-92dd-65bb00517881"))
    if gvar.get(args[0]) is None:
        arcane = newline.join([f'!bastion delete \\\"{i}\\\"' for i in gvar.keys()])
        return f"""embed -title "!bastion delete \\\"{args[0]}\\\"" -desc "No such facility, valid options are:```\n{arcane} ```" """


    if character().cvars.get("bastion") is None:
        character().set_cvar("bastion","[]")

    bastion = load_json(character().cvars["bastion"])

    for i in bastion:
        if i["name"] == args[0]:
            bastion.remove(i)
            character().set_cvar("bastion",dump_json(bastion))
            return f"""embed -title "!bastion delete \\\"{args[0]}\\\"" -desc "Deleted" """
        
    return f"""embed -title "!bastion delete \\\"{args[0]}\\\"" -desc "You don't have that facility" """