from mocks import get_gvar, load_json


# AVRAE COMMAND
# -------------

def main(args):
    #args = &ARGS&
    
    args[0] = args[0].lower()
    newline = "\n"

    gvar = load_json(get_gvar("a3dec4b0-0c72-4d05-92dd-65bb00517881"))
    if gvar.get(args[0]) is None:
        arcane = newline.join([f'!bastion lookup \\\"{i}\\\"' for i in gvar.keys()])
        return f"""embed -title "!bastion lookup \\\"{args[0]}\\\"" -desc "No such facility, valid options are:```\n{arcane} ```" """

    return f"""embed -title "!bastion lookup \\\"{args[0]}\\\"" -desc "{gvar[args[0]]['desc']}" -f "Gold Price | {gvar[args[0]]['cost']} |inline" -f "Character Level Required | {gvar[args[0]]['level']} |inline" -f "Commands | ```\n{newline.join(gvar[args[0]]['commands'])} ```" """
