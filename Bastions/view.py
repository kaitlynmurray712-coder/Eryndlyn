from mocks import MockCharacter
from mocks import load_json, get_gvar, dump_json

character = MockCharacter


# AVRAE COMMAND
# -------------
def main(args, level):
    
    if level < 5:
        return f"""embed -title "!bastion view" -desc "You must be level 5 or higher to use this command" """
    
    if character().cvars.get("bastion") is None:
        character().set_cvar("bastion","[]")
    if character().cvars.get("bastion_basic") is None:
        character().set_cvar("bastion_basic","[]")

    bastion = load_json(character().cvars["bastion"])
    newline = "\n"

    return f'''embed -title "!bastion view" -desc "**Basic Facilities:** {" ".join([f"{newline}- {i.title()}" for i in load_json(character().cvars["bastion_basic"])])}" {" ".join(
        [
            f'-f "{("Enlarged " if facility["enlarge"] else "")}{facility["name"].title()} | {newline.join([str(i["event"]) + " : " + str(i["days_complete"]) + "/" + str(i["total_days"]) for i in facility["events"]]) if facility["events"] else "N/A"} |inline"'
            for facility in bastion
        ]
    )}'''