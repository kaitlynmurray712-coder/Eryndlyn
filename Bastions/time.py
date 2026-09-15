from mocks import MockCharacter
from mocks import load_json, get_gvar, dump_json

character = MockCharacter


# AVRAE COMMAND
# -------------
def main(args, level):
    #args = &ARGS&
    
    args[0] = int(args[0])
    newline = "\n"

    if character().cvars.get("bastion") is None:
        character().set_cvar("bastion","[]")
    if character().cvars.get("bastion_basic") is None:
        character().set_cvar("bastion_basic","[]")

    if level < 5:
        return f"""embed -title "!bastion time {args[0]}" -desc "You must be level 5 or higher to use this command" """

    bastion = load_json(character().cvars["bastion"])

    all_events = []
    for facility in bastion:
        for event in facility["events"]:
            event["days_complete"] += args[0]
            if event["days_complete"] > event["total_days"]:
                event["days_complete"] = event["total_days"]
            all_events.append(f"- {event['event']} | {event['days_complete']}/{event['total_days']} days left")

    character().set_cvar("bastion",dump_json(bastion))
    
    return f"""embed -title "!bastion time {args[0]}" -desc "{newline.join(all_events)}" """