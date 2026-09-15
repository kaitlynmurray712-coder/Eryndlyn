from mocks import MockCharacter
from mocks import load_json, get_gvar, dump_json, vroll

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

    gvar = load_json(get_gvar("a3dec4b0-0c72-4d05-92dd-65bb00517881"))

    if gvar.get(args[0]) is None:
        arcane = newline.join([f'!bastion facility \\\"{i}\\\"' for i in gvar.keys()])
        return f"""embed -title "!bastion facility \\\"{args[0]}\\\"" -desc "No such facility, valid options are:```\n{arcane} ```" """

    bastion = load_json(character().cvars["bastion"])

    active_facility = None
    facility_index = 0
    for index, facility in enumerate(bastion):
        if facility["name"] == args[0]:
            active_facility = facility
            facility_index = index
            break

    if active_facility is None:
        return f"""embed -title "!bastion facility \\\"{args[0]}\\\"" -desc "You don't have that facility" """

    # NOW THE CODE...
    facility_gvar = load_json(get_gvar("9f6dd669-4a94-4581-982b-a72108c78df8"))

    # Arcane Study
    # ------------
    if active_facility["name"] == "arcane study":
        args[1] = args[1].lower()

        # all lvls
        if args[1] in ["focus", "book"]:
            event = [{"event":f"Crafting: {args[1]}", "days_complete":0, "total_days":facility_gvar["arcane study"][args[1]]["days"]}]

            if character().coinpurse.total < facility_gvar["arcane study"][args[1]]["cost"]:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs {facility_gvar["arcane study"][args[1]]["cost"]} gold" """

            character().coinpurse.modify_coins(gp=-facility_gvar["arcane study"][args[1]]["cost"], autoconvert=True)
            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started {args[1]}. Fee: {facility_gvar["arcane study"][args[1]]["cost"]} gold" """

        # lvls 9 up
        if level < 9:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You must be level 9 or higher to use this command" """

        for items in facility_gvar["arcane study"]:
            if items in args[1]:
                event = [{"event":f"Crafting: {items}", "days_complete":0, "total_days":facility_gvar["arcane study"][items]["days"]}]

                if character().coinpurse.total < facility_gvar["arcane study"][items]["cost"]:
                    return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs {facility_gvar["arcane study"][items]["cost"]} gold" """

                character().coinpurse.modify_coins(gp=-facility_gvar["arcane study"][args[1]]["cost"], autoconvert=True)
                bastion[facility_index]["events"] = event
                character().set_cvar("bastion",dump_json(bastion))

                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started {items}. Fee: {facility_gvar["arcane study"][items]["cost"]} gold" """

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "No such item found. Please try a lowercased name of an item found here: https://www.dndbeyond.com/sources/dnd/dmg-2024/random-magic-items#ArcanaCommon or type 'common magic item' / 'uncommon magic item' for a generic solution." """

    # Armory
    # ------
    if active_facility["name"] == "armory":
        if character().coinpurse.total < 100:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" " -desc "You don't have enough gold. Costs 100 gold" """

        character().coinpurse.modify_coins(gp=-100, autoconvert=True)
        return f"""embed -title "!bastion facility \\\"{args[0]}\\\"" -desc "Trade with the Armory. Fee: 100 gold" """

    # Garden
    # ------
    if active_facility["name"] == "garden":
        args[1] = args[1].lower()
        args[2] = int(args[2]) - 1

        if (args[2] < 0) or (args[2] > 2):
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]+1}" -desc "You must choose between 1-3" """

        if (args[2] > 0) and not active_facility["enlarge"]:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]+1}" -desc "That facility is not fully upgraded, enlarge it first to unlock slots 2 and 3" """

        if args[1] not in ["decorative", "food", "herb", "poison"]:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]+1}" -desc "You must choose between decorative, food, herb, or poison" """

        event = {"event":"Gardening: " + args[1], "days_complete":0, "total_days":21}

        if len(bastion[facility_index]["events"]) <= args[2]:
            bastion[facility_index]["events"].append(event)
        else:
            bastion[facility_index]["events"][args[2]] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]+1}" -desc "Started Gardening {args[1]}" """

    # library
    # -------
    if active_facility["name"] == "library":
        event = [{"event":"Researching: " + args[1], "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Researching {args[1]}" """

    # sanctuary
    # ---------
    if active_facility["name"] == "sanctuary":
        event = [{"event":"Crafting: focus", "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" " -desc "Started Crafting focus" """

    # smithy
    # ------
    if active_facility["name"] == "smithy":
        args[1] = args[1].lower()

        # all lvls
        if args[1] == "equipment":
            args[3] = int(args[3])

            if character().coinpurse.total < args[3]//2:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]} {args[3]}" -desc "You don't have enough gold. Costs {args[3]//2} gold" """

            event = [{"event":"Crafting: " + args[2], "days_complete":0, "total_days":args[3]//10 if args[3]//10 > 0 else 1}]
            character().coinpurse.modify_coins(gp=-(args[3]//2), autoconvert=True)

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]} {args[3]}" -desc "Started crafting {args[2]}. Fee: {args[3]//2} gold" """

        # lvls 9 up
        if level < 9:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You must be level 9 or higher to use this command" """

        for items in facility_gvar["smithy"]:
            if items in args[1]:
                event = [{"event":f"Crafting: {items}", "days_complete":0, "total_days":facility_gvar["smithy"][items]["days"]}]

                if character().coinpurse.total < facility_gvar["smithy"][items]["cost"]:
                    return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs {facility_gvar["smithy"][items]["cost"]} gold" """

                character().coinpurse.modify_coins(gp=-facility_gvar["smithy"][args[1]]["cost"], autoconvert=True)
                bastion[facility_index]["events"] = event
                character().set_cvar("bastion",dump_json(bastion))

                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started crafting {items}. Fee: {facility_gvar["smithy"][items]["cost"]} gold" """

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "No such item found. Please try a lowercased name of an item found here: https://www.dndbeyond.com/sources/dnd/dmg-2024/random-magic-items#ArcanaCommon or type 'common magic item' / 'uncommon magic item' for a generic solution." """

    # storehouse
    # ----------
    if active_facility["name"] == "storehouse":
        char_level_pricing = {
            0: 500,
            9: 2000,
            13: 5000,
        }
        char_profit = {
            0: 1.1,
            9: 1.2,
            13: 1.5,
            17: 2
        }
        char_level_pricing_value = 0 if level < 9 else 9 if level < 13 else 13
        char_profit_value = 0 if level < 9 else 9 if level < 13 else 13 if level < 17 else 17

        if character().coinpurse.total < char_level_pricing[char_level_pricing_value]:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" " -desc "You don't have enough gold. Costs {char_level_pricing[char_level_pricing_value]} gold" """

        event = [{"event":f"Trading for {char_level_pricing[char_level_pricing_value]*char_profit[char_profit_value]}", "days_complete":0, "total_days":7}]
        character().coinpurse.modify_coins(gp=-char_level_pricing[char_level_pricing_value], autoconvert=True)

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" " -desc "Started trading for {char_level_pricing[char_level_pricing_value]*char_profit[char_profit_value]}. Fee: {char_level_pricing[level]} gold" """

    # workshop
    # --------
    if active_facility["name"] == "workshop":
        args[1] = args[1].lower()
        
        # all lvls
        if args[1] == "equipment":
            args[3] = int(args[3])
            args[4] = int(args[4]) -1 

            if (args[4] < 0) or (args[4] > 2):
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" \\\"{args[2]}\\\" {args[3]} {args[4]+1}" -desc "You must choose between 1-3" """
    
            if (args[4] > 0) and not active_facility["enlarge"]:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" \\\"{args[2]}\\\" {args[3]} {args[4]+1}" -desc "That facility is not fully upgraded, enlarge it first to unlock slots 2 and 3" """

            if character().coinpurse.total < args[3]//2:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" \\\"{args[2]}\\\" {args[3]} {args[4]+1}" -desc "You don't have enough gold. Costs {args[3]//2} gold" """

            event = {"event":"Crafting: " + args[2], "days_complete":0, "total_days":args[3]//10 if args[3]//10 > 0 else 1}
            if len(bastion[facility_index]["events"]) <= args[4]:
                bastion[facility_index]["events"].append(event)
            else:
                bastion[facility_index]["events"][args[4]] = event

            character().set_cvar("bastion",dump_json(bastion))
            character().coinpurse.modify_coins(gp=-(args[3]//2), autoconvert=True)

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" \\\"{args[2]}\\\" {args[3]} {args[4]+1}" -desc "Started crafting {args[2]}. Fee: {args[3]//2} gold" """

        # lvl 9
        if level < 9:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]}" -desc "You must be level 9 or higher to use this command" """

        if (args[2] < 0) or (args[2] > 2):
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]}" -desc "You must choose between 1-3" """
        if (args[2] > 0) and not active_facility["enlarge"]:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]}" -desc "That facility is not fully upgraded, enlarge it first to unlock slots 2 and 3" """

        for items in facility_gvar["workshop"]:
            if items in args[1]:
                event = {"event":f"Crafting: {items}", "days_complete":0, "total_days":facility_gvar["workshop"][items]["days"]}

                if character().coinpurse.total < facility_gvar["workshop"][items]["cost"]:
                    return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]}" -desc "You don't have enough gold. Costs {facility_gvar["workshop"][items]["cost"]} gold" """

                character().coinpurse.modify_coins(gp=-facility_gvar["workshop"][args[1]]["cost"], autoconvert=True)
                if len(bastion[facility_index]["events"]) <= args[2]:
                    bastion[facility_index]["events"].append(event)
                else:
                    bastion[facility_index]["events"][args[2]] = event
                character().set_cvar("bastion",dump_json(bastion))

                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]}" -desc "Started crafting {items}. Fee: {facility_gvar["workshop"][items]["cost"]} gold" """

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]}" -desc "No such item found. Please try a lowercased name of an item found here: https://www.dndbeyond.com/sources/dnd/dmg-2024/random-magic-items#ImplementsTables or type 'common magic item' / 'uncommon magic item' for a generic solution." """

    # gaming hall
    # -----------
    if active_facility["name"] == "gaming hall":
        roll = vroll("d100")
        if roll > 95:
            prize = vroll("10d6")
        elif roll > 85:
            prize = vroll("4d6")
        elif roll > 50:
            prize = vroll("2d6")
        else:
            prize = vroll("1d6")

        event = {"event":f"Prize: {prize.total * 10} gold", "days_complete":0, "total_days":7}

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\"" -desc "You'll win {prize.total * 10} gold in 7 days!" -f"Roll | {roll}|inline" -f"Prize | {prize} |inline" """

    # greenhouse
    # ----------
    if active_facility["name"] == "greenhouse":
        args[1] = args[1].lower()
        if args[1] not in ["potion of healing","assassin's blood","malice","pale tincture","truth serum"]:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You must choose one of the following: Potion of Healing, Assassin's Blood, Malice, Pale Tincture, or Truth Serum" """

        event = {"event":f"Harvest: {args[1]}", "days_complete":0, "total_days":7}

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You'll get a {args[1]} in 7 days!" """

    # laboratory
    # ----------
    if active_facility["name"] == "laboratory":
        args[1] = args[1].lower()
        if args[1] == "equipment":
            args[3] = int(args[3])        
            if character().coinpurse.total < args[3]//2:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]} {args[3]}" -desc "You don't have enough gold. Costs {args[3]//2} gold" """

            event = [{"event":"Crafting: " + args[2], "days_complete":0, "total_days":args[3]//10 if args[3]//10 > 0 else 1}]
            character().coinpurse.modify_coins(gp=-(args[3]//2), autoconvert=True)

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\" {args[2]} {args[3]}" -desc "Started crafting {args[2]}. Fee: {args[3]//2} gold" """
        if args[1] == "burnt othur fumes":
            if character().coinpurse.total < 250:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs 250 gold" """

            character().coinpurse.modify_coins(gp=-250, autoconvert=True)
            event = [{"event":"Crafting: Burnt Othur Fumes", "days_complete":0, "total_days":7}]
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started crafting Burnt Othur Fumes. Fee: 250 gold" """
        if args[1] == "essence of ether":
            if character().coinpurse.total < 150:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs 250 gold" """

            character().coinpurse.modify_coins(gp=-150, autoconvert=True)
            event = [{"event":"Crafting: Essence of Ether", "days_complete":0, "total_days":7}]
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started crafting Essence of Ether. Fee: 250 gold" """
        if args[1] == "torpor":
            if character().coinpurse.total < 300:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs 250 gold" """

            character().coinpurse.modify_coins(gp=-300, autoconvert=True)
            event = [{"event":"Crafting: Torpor", "days_complete":0, "total_days":7}]
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started crafting Torpor. Fee: 250 gold" """

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You must choose one of the following: Equipment, Burnt Othur Fumes, Essence of Ether, Torpor" """

    # sacristy
    # --------
    if active_facility["name"] == "sacristy":
        args[1] = args[1].lower()
        if args[1] == "holy water":
            event = [{"event":f"Crafting: {args[1]}", "days_complete":0, "total_days":7}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Crafting Holy Water." """
        for items in facility_gvar["sacristy"]:
            if items in args[1]:
                event = [{"event":f"Crafting: {items}", "days_complete":0, "total_days":facility_gvar["sacristy"][items]["days"]}]

                if character().coinpurse.total < facility_gvar["sacristy"][items]["cost"]:
                    return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs {facility_gvar["sacristy"][items]["cost"]} gold" """

                character().coinpurse.modify_coins(gp=-facility_gvar["sacristy"][args[1]]["cost"], autoconvert=True)
                bastion[facility_index]["events"] = event
                character().set_cvar("bastion",dump_json(bastion))

                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started {items}. Fee: {facility_gvar["sacristy"][items]["cost"]} gold" """

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "No such item found. Please try a lowercased name of an item found here: https://www.dndbeyond.com/sources/dnd/dmg-2024/random-magic-items#RelicsTables or type 'common magic item' / 'uncommon magic item' for a generic solution." """

    # scriptorium
    # -----------
    if active_facility["name"] == "scriptorium":
        args[1] = args[1].lower()
        if args[1] == "book":
            event = [{"event":f"Crafting: {args[1]}", "days_complete":0, "total_days":7}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Crafting Book." """
        if args[1] == "paperwork":
            if character().coinpurse.total < 50:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs 50 gold" """

            character().coinpurse.modify_coins(gp=-50, autoconvert=True)
            event = [{"event":f"Crafting: {args[1]}", "days_complete":0, "total_days":7}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Crafting Paperwork." """
        if args[1] == "spell scroll 1":
            if character().coinpurse.total < 25:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs 25 gold" """

            character().coinpurse.modify_coins(gp=-25, autoconvert=True)
            event = [{"event":f"Crafting: {args[1]}", "days_complete":0, "total_days":1}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Crafting Spell Scroll 1." """
        if args[1] == "spell scroll 2":
            if character().coinpurse.total < 75:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs 75 gold" """

            character().coinpurse.modify_coins(gp=-75, autoconvert=True)
            event = [{"event":f"Crafting: {args[1]}", "days_complete":0, "total_days":3}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Crafting Spell Scroll 2." """
        if args[1] == "spell scroll 3":
            if character().coinpurse.total < 150:
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You don't have enough gold. Costs 150 gold" """

            character().coinpurse.modify_coins(gp=-150, autoconvert=True)
            event = [{"event":f"Crafting: {args[1]}", "days_complete":0, "total_days":5}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Crafting Spell Scroll 3." """

    # training area
    # -------------
    if active_facility["name"] == "training area":
        event = [{"event":f"Training: {args[1]}", "days_complete":0, "total_days":14}]

        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Training {args[1]}. At day 8, you gain the benefit until day 14." """

    # trophy room
    # -----------
    if active_facility["name"] == "trophy room":
        args[1] = args[1].lower()
        if args[1] == "lore":
            event = [{"event":f"Researching {args[2]}", "days_complete":0, "total_days":7}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Collecting Lore." """
        if args[1] == "trinket":
            find_roll = vroll("d2")
            item_roll = vroll("d35")
            item = facility_gvar["trophy room"][item_roll.total]
            if find_roll.total == 1:
                event = [{"event":f"Collecting: nothing", "days_complete":0, "total_days":7}]

                bastion[facility_index]["events"] = event
                character().set_cvar("bastion",dump_json(bastion))
                return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "You found nothing." """
            event = [{"event":f"Collecting: {item}", "days_complete":0, "total_days":7}]

            bastion[facility_index]["events"] = event
            character().set_cvar("bastion",dump_json(bastion))

            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Collecting Trinket. You found {item}." """

    # archive
    # -------
    if active_facility["name"] == "archive":
        event = [{"event":"Researching: " + args[1], "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Researching {args[1]}" """

    # meditation chamber
    # ------------------
    if active_facility["name"] == "meditation chamber":
        roll1 = vroll("d6")
        roll2 = vroll("d6")
        while roll1.total == roll2.total:
            roll2 = vroll("d6")
        roll_map = {
            1:"Strength",
            2:"Dexterity",
            3:"Constitution",
            4:"Intelligence",
            5:"Wisdom",
            6:"Charisma"
        }
        event = [{"event":f"Fortify Self: {roll_map[roll1.total]} & {roll_map[roll2.total]}", "days_complete":0, "total_days":14}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\"" -desc "Started Meditating. At day 8 you gain Advantage on a {roll_map[roll1.total]} & {roll_map[roll2.total]} saving throw until day 14." """

    # menagerie
    # ---------
    if active_facility["name"] == "menagerie":
        cr_mapping ={
            "0": 50,
            "1/8": 50,
            "1/4": 250,
            "1/2":500,
            "1":1000,
            "2":2000,
            "3":3500
        }
        if args[1] not in cr_mapping:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" {args[1]} \\\"{args[2]}\\\"" -desc "Invalid CR" """

        if character().coinpurse.total < cr_mapping[args[1]]:
            return f"""embed -title "!bastion facility \\\"{args[0]}\\\" {args[1]} \\\"{args[2]}\\\"" -desc "You don't have enough gold. Costs {cr_mapping[args[1]]} gold" """

        character().coinpurse.modify_coins(gp=-cr_mapping[args[1]], autoconvert=True)
        event = [{"event":f"Taming: CR {args[1]} {args[2]}", "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" {args[1]} \\\"{args[2]}\\\" " -desc "Started Taming CR {args[1]} {args[2]}." """

    # observatory
    # -----------
    if active_facility["name"] == "observatory":
        event = [{"event":"Empowered", "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\"" -desc "Started Empowered" """

    # pub
    # ---
    if active_facility["name"] == "pub":
        event = [{"event":"Researching: " + args[1], "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" \\\"{args[1]}\\\"" -desc "Started Researching {args[1]}" """

    # reliquary
    # ---------
    if active_facility["name"] == "reliquary":
        event = [{"event":"Crafting: Talisman", "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" " -desc "Started Crafting: Talisman" """

    # demiplane
    # ---------
    if active_facility["name"] == "demiplane":
        event = [{"event":"Empowered", "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" " -desc "Started Empowered" """

    # sanctum
    # -------
    if active_facility["name"] == "sanctum":
        event = [{"event":"Empowered", "days_complete":0, "total_days":7}]
        bastion[facility_index]["events"] = event
        character().set_cvar("bastion",dump_json(bastion))

        return f"""embed -title "!bastion facility \\\"{args[0]}\\\" " -desc "Started Empowered" """
    
    return f"""embed -title "!bastion facility \\\"{args[0]}\\\"" -desc "No such facility" """