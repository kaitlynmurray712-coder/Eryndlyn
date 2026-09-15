embed 
<drac2>
#Base Variables
food = {
    "swordsman": {
        "No favorite yet!":{"name":"No favorite yet!","price":"0"},
        "No hated food yet!":{"name":"No hated food yet!","price":"0"},
        "oatmeal":{"name":"Spiced Oatmeal","price":"5"},
        "eggs":{"name":"Eggs and Rothe Bacon","price":"7"},
        "pancakes":{"name":"Rowan's Pancakes","price":"6"},
        "dip":{"name":"Direshore Crab Dip","price":"10"},
        "fish":{"name":"Fish Fry and Chips","price":"20"},
        "mutton":{"name":"Mutton Shepherds Pie","price":"15"},
        "elk":{"name":"Elk Steak and Twice Baked Potatoes","price":"50"},
        "salmon":{"name":"Cedar Plank Salmon","price":"80"},
        "boil":{"name":"Crab Boil","price":"30"},
        "cheesecake":{"name":"Wild Blueberry Cheesecake","price":"20"},
        "cake":{"name":"Spiced Coffee Cake","price":"5"},
        "scone":{"name":"Scones with Clotted Cream and Jam","price":"7"},
        "cookie":{"name":"Theran's Favorite Chocolate Chip Cookie","price":"3"}
    },
    "rook": {
        "No favorite yet!":{"name":"No favorite yet!","price":"0"},
        "No hated food yet!":{"name":"No hated food yet!","price":"0"},
        "frenchtoast":{"name":"Bluebread French Toast","price":"6"},
        "biscuits":{"name":"Biscuits and Deep Rothe Gravy","price":"5"},
        "snakebites":{"name":"Snakebites","price":"10"},
        "batwings":{"name":"Valyzr's Special Batwings","price":"20"},
        "firebeetle":{"name":"Roasted Firebeetle seasoned with Firelichen","price":"40"},
        "spider":{"name":"Spider King Legs","price":"50"},
        "steak":{"name":"Deep Rothe Steak with Sauteed Mushrooms","price":"50"},
        "clamari":{"name":"Rocktopus Calamari","price":"100"},
        "icecream":{"name":"Eilsurden Family Favorite Ice Cream","price":"10"},
        "moonworms":{"name":"Honeyed Moon Worms","price":"120"}
    },
    "horseshoe":{
        "No favorite yet!":{"name":"No favorite yet!","price":"0"},
        "No hated food yet!":{"name":"No hated food yet!","price":"0"},
        "eclairs":{"name":"Crustacien Eclairs", "price":"5"},
        "pearls":{"name":"Sea Pearls with Ocean Sauce", "price":"10"},
        "steak":{"name":"Shark Steak with Jellyfish Relish", "price":"20"},
        "stew":{"name":"Sea Captain's Stew", "price":"15"},
        "grill":{"name":"Grilled Octopus and Seabird", "price":"35"},
        "king":{"name":"King's Feast", "price":"500"},
        "gumbo":{"name":"Chowder Gumbo", "price":"120"},
        "candy":{"name":"Coral Candy Clusters", "price":"10"}
    },
    "sleeping":{
        #nothing yet
    },
    "drink":{
        "No favorite yet!":{"name":"No favorite drink yet!","price":"0","dc":"0"},
        "No hated food yet!":{"name":"No hated drink yet!","price":"0","dc":"0"},
        "water":{"name":"Water", "price":"0","dc":"0"},
        "green":{"name":"Green Tea","price":"2","dc":"0"},
        "breakfast":{"name":"Breakfast Tea","price":"2","dc":"0"},
        "coffee":{"name":"Coffee","price":"2","dc":"0"},
        "wine":{"name":"House Wine","price":"15","dc":"10"},
        "ale":{"name":"House Ale","price":"10","dc":"10"},
        "whiskey":{"name":"House Whiskey","price":"15","dc":"15"},
        "gin":{"name":"House Gin","price":"20","dc":"15"},
        "vot":{"name":"Vot's *SPECIAL* Rum","price":"12","dc":"15"},
        "direshore":{"name":"Direshore Hair of the Dog Mead","price":"30","dc":"20"},
        "abbil":{"name":"Abbil Darklake Stout","price":"45","dc":"20"},
        "samsar":{"name":"Samsar Cactus Flower Rum","price":"25","dc":"20"},
        "atlatis":{"name":"Atlantis Trident Spirits","price":"40","dc":"20"}
    }
}
howdrunk = {"0" : "Don't forget to hydrate!","1" : "You're getting that nice warm and fuzzy feeling. You now have ADV on Persuasion.", "2" : "You are officially tipsy! DIS on Perception, but have ADV on Intimidation.", "3" : "Things are starting to get a little fuzzy. DIS on Perception and Insight, but ADV on Intimidation.", "4" : "You're really starting to feel it. You are struggling to walk in a straight line at this point. DIS on Perception, Insight, and all DEX based checks", "5" : "Walking is almost impossible. You are almost ready to black out. DIS on Perception, Insight, DEX based checks, and DEATH SAVES", "6" : "You have died. Please place your character in the graveyard."}
city = "&1&" ## City
order = "&2&" ## what ordering

if city == "swordsman" or city == "rook" or city == "horseshoe" or city == "sleeping" or city == "drink":
    ch = character() #Pull Char Data
    names = ch.name ##Char Name
    purse = ch.coinpurse.total # Pull Char $
    ordered = food[city][order]["name"] ##full name of order
    cost = food[city][order]["price"] ##pricing
    money = cost.lower()

    ch.coinpurse.modify_coins(sp= -int(money)) ## Remove money

    coin = ch.coinpurse ## New coin

    like = vroll('1d100').total ## Dow we like this?""

    cc1 = "Drunkeness" ## Booze?
    cc2 = "Hydration" ## Thirst?
    cc3 = "Hunger" ## Scott's Always HANGRY
    
    
    #### __________________________________ ####

    ##                Bodily Needs

    drunkdes = " "
    if city == "swordsman" or city == "rook" or city == "horseshoe" or city == "sleeping":
        if ch.cc_exists(cc1): ## Do you have the drunken counter?
            drunk = ch.get_cc(cc1) #Yes? Gimme your status
        else:
            ch.create_cc_nx(cc1, 0, 4, "long", "bubble", 0, None, cc1) # No? Make one.
            drunk = ch.get_cc(cc1) #and then gimme status

        #hydrate!
        if ch.cc_exists(cc2): ## counter exist?
            hydrate = ch.get_cc(cc2) # yes?
        else:
            ch.create_cc_nx(cc2, 0, 4, "long", "bubble", 0, None, cc2)
            hydrate = ch.get_cc(cc2)

        #hunger
        if ch.cc_exists(cc3):
            ch.mod_cc(cc3, 1)
            hung = ch.get_cc(cc3)
        else:
            ch.create_cc_nx(cc3, 0, 4, "long", "bubble", 0, None, cc3)
            ch.mod_cc(cc3, 1)
            hung = ch.get_cc(cc3)

    elif city == "drink":
        if ch.get_cc(cc3) == 3 or ch.get_cc(cc3) == 4:
            d = vroll('2d20kh1')
        else:
            d = vroll('1d20')
        e = d.total+constitutionSave

        savedc = food[city][order]["dc"]
        
        #drunk
        if int(savedc) > int(e):
            passfail = "Oof! That one hit a little hard."
            #drunkeness!
            if ch.cc_exists(cc1): ## Do you have the drunken counter?
                ch.mod_cc(cc1, 1)
                drunk = ch.get_cc(cc1) #Yes? Gimme your status
            else:
                ch.create_cc_nx(cc1, 0, 4, "long", "bubble", 0, None, cc1) # No? Make one.
                ch.mod_cc(cc1, 1)
                drunk = ch.get_cc(cc1) #and then gimme status

        elif int(savedc) <= int(e):
            passfail = "Keeping hydrated has it's benefits!"
            if ch.cc_exists(cc1): ## Do you have the drunken counter?
                drunk = ch.get_cc(cc1) #Yes? Gimme your status
            else:
                ch.create_cc_nx(cc1, 0, 4, "long", "bubble", 0, None, cc1) # No? Make one.
                drunk = ch.get_cc(cc1) #and then gimme status


        #hydrate!
        if ch.cc_exists(cc2): ## counter exist?
            ch.mod_cc(cc2, 1)
            hydrate = ch.get_cc(cc2) # yes?
            
        else:
            ch.create_cc_nx(cc2, 0, 4, "long", "bubble", 0, None, cc2)
            ch.mod_cc(cc2, 1)
            hydrate = ch.get_cc(cc2)

        #hunger
        if ch.cc_exists(cc3):
            hung = ch.get_cc(cc3)
        else:
            ch.create_cc_nx(cc3, 0, 4, "long", "bubble", 0, None, cc3)
            hung = ch.get_cc(cc3)

        
        drunkdes = "\n\n"
        drunkdes += "Woo! That was refreshing"
        drunkdes += "\n"
        drunkdes += ordered
        drunkdes += " Save DC: "
        drunkdes += savedc
        drunkdes += "\n"
        drunkdes += "You Rolled: "
        drunkdes += d 
        drunkdes += " + "
        drunkdes += constitutionSave
        drunkdes += " = "
        drunkdes += e
        drunkdes +=  "\n"
        drunkdes += passfail

    #### __________________________________ ####

    ###               City shit
    if city == "swordsman":
        #do some shit
        fave = "direshorefavefood"
        hate = "direshorehatefood"
        title = "The Swordsman Inn and Tavern"
    elif city == "rook":
        #Do other shit
        fave = "rookfavefood"
        hate = "rookhatefood"
        title = "The Rook Bar and Inn"
    elif city == "horseshoe":
        #more shit
        fave = "horseshoefavefood"
        hate = "horseshoehatefood"
        title = "The Horseshoe Tavern and Inn"
    elif city == "sleeping":
        #MORE shit
        fave = "sleepingfavefood"
        hate = "sleepinghatefood"
        title = "The Sleeping Beauty Inn"
    elif city == "drink":
        fave = "favoritedrink"
        hate = "hateddrink"
        title = "Eryndlyn Drinks Menu"
    else: 
        #I effed up.
        title = "oop?"


    #### __________________________________ ####

    ###                Favorites
    #### LOVE!
    if ch.get_cvar(fave): 
        a = ch.get_cvar(fave)
    else:
        ch.set_cvar(fave,"No favorite yet!")
        a = ch.get_cvar(fave)
    #### HATE!!
    if ch.get_cvar(hate):
        b = ch.get_cvar(hate)
    else:
        ch.set_cvar(hate,"No hated food yet!")
        b = ch.get_cvar(hate)

    # Set love/hate
    if like == "100" and b != order and a == "No favorite yet!": 
        ch.set_cvar(fave,order)
        thoughts = "LOVED this!"
    elif like == "1" and a != order:
        ch.set_cvar(hate,order)
        thoughts = "absolutely HATED this!"
    elif b == order :
        thoughts = "absolutely HATED this!"
    elif a == order:
        thoughts = "LOVED this!"
    else: 
        thoughts = thoughts = "thought this wasn't too bad!"
        

    #### __________________________________ ####

    ##                    THP

    temp = "Eating and drinking give you energy!"
    if ch.get_cc(cc2) == 4 and ch.get_cc(cc3) == 4:
        ch.set_temp_hp('15')
        temp = "You're full and hydrated! You gained 15thp!"
    elif ch.get_cc(cc3) == 4:
        ch.set_temp_hp('10')
        temp = "You're full! You gained 10thp!"
    if ch.get_cc(cc1) > 0 and city == "drink":
        temp += "\n"
        temp += howdrunk[str(drunk)]
    level = ch.get_cc(cc1)
    hyd = ch.get_cc(cc2)

    #### __________________________________ ####

    ###            Description
    des = "**You have ordered:** "
    des += ordered
    des += "\n\n"
    des += "You rolled: "
    des += " "
    des += like
    des += "\n"
    des += names
    des += " "
    des += thoughts
    des += "\n"
    des += temp
    des += "\n\n"
    des += "**"
    des += names
    des += "** is currently:"
    des += "\n"
    des += "__Drunkeness:__ "
    des += drunk
    des += "/6"
    des += "\n"
    des += "__Hydration:__ "
    des += hyd
    des += "/4"
    des += "\n"
    des += "__Hunger:__ "
    des += hung
    des += "/4"
    des += "\n\n"
    des += names
    des += " likes/dislikes from "
    des += title
    des += ":"
    des += "\n"
    des += "Likes: "
    des += food[city][a]["name"]
    des += "\n"
    des += "Dislikes: "
    des += food[city][b]["name"]
    des += drunkdes
    des += "\n\n"
    des += "Your total is: "
    des += cost
    des += "sp"
    des += "\n"
else:
    title = "Oh no! Let me help"
    des = "Please use format `!consume <menu> <order>`"
    coin = "For the full menu use `!menu <menu>`"
</drac2>
-title "{{title}}"
-desc "{{des}}
{{coin}}"
-footer "Kait did a BIG thing... :D"