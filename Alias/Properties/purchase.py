embed
<drac2>

ch=character()
inp1 = "&1&" #property type (home/business)
inp2 = "&2&" #size/type 
inp3 = "&3&" #rent/buy outright

b = "business"
h = "home"

if inp1 == b:
    title = "Purchasing a Business"
    propertyTypes = load_json(get_gvar("323a57a9-300b-4077-9499-063af8669c0d"))
    propertyName = propertyTypes[inp2]['name']
    propertyCost = propertyTypes[inp2]['cost']
    propertyUpkeep = propertyTypes[inp2]['upkeep']
    propertyRent = propertyTypes[inp2]['rent']
    if inp3 == "rent":
        loanName = propertyName
        loanName += " Loan"
        des = "Congrats on starting your "
        des += propertyName
        des += " business."
        des += "\n"
        des += "Rent is paid weekly until your loan is paid in full."
        des +="\n\n"
        des += "Loan Amount: "
        des += propertyCost
        des += "gp"
        des += "\n"
        des += "Rent: "
        des += propertyRent
        des += "gp"
        des += "\n"
        des += "Upkeep: "
        des += propertyUpkeep
        des += "gp"
        des +="\n\n"
        des +="These are paid weekly on **SUNDAY**."
        ch.create_cc(name=loanName, initial_value=propertyCost)
        if ch.get_cvar(b):
            temp = ch.get_cvar(b)
            temp += ","
            temp += inp2
            ch.set_cvar(b, temp)
        else:
            ch.set_cvar(b,inp2)
        

    elif inp3 == "buy":
        ogpurse = ch.coinpurse.total
        ch.coinpurse.modify_coins(gp= -propertyCost)
        if ch.get_cvar(b):
            temp = ch.get_cvar(b)
            temp += ","
            temp += inp2
            ch.set_cvar(b, temp)
        else:
            ch.set_cvar(b,inp2)
        des = "Congrats on starting your "
        des += propertyName
        des += " business."
        des +="\n\n"
        des += "Amount Paid: "
        des += propertyCost
        des += "gp"
        des += "\n"
        des += "Upkeep: "
        des += propertyUpkeep
        des += "gp"
        des +="\n\n"
        des +="Upkeep is paid weekly on **SUNDAY**."
           
    
elif inp1 == h:
    title = "Purchasing a Home"
    propertyTypes = load_json(get_gvar("4df294ea-6bf7-4b2a-ba25-6e76ecad8a84"))
    propertyName = propertyTypes[inp2]['name']
    propertyCost = propertyTypes[inp2]['cost']
    propertyUpkeep = propertyTypes[inp2]['upkeep']
    propertyRent = propertyTypes[inp2]['rent']
    if inp3 == "rent":
        loanName = propertyName
        loanName += " Loan"
        des = "Congrats on purchaing your "
        des += propertyName
        des += "."
        des += "\n"
        des += "Rent is paid weekly until your loan is paid in full."
        des +="\n\n"
        des += "Loan Amount: "
        des += propertyCost
        des += "gp"
        des += "\n"
        des += "Rent: "
        des += propertyRent
        des += "gp"
        des += "\n"
        des += "Upkeep: "
        des += propertyUpkeep
        des += "gp"
        des +="\n\n"
        des +="These are paid weekly on **SUNDAY**."
        ch.create_cc(name=loanName, initial_value=propertyCost)
        if ch.get_cvar(h):
            temp = ch.get_cvar(h)
            temp += ","
            temp += inp2
            ch.set_cvar(h, temp)
        else:
            ch.set_cvar(h,inp2)
    elif inp3 == "buy":
        ogpurse = ch.coinpurse.total
        ch.coinpurse.modify_coins(gp= -propertyCost)
        if ch.get_cvar(h):
            temp = ch.get_cvar(b)
            temp += ","
            temp += inp2
            ch.set_cvar(h, temp)
        else:
            ch.set_cvar(h,inp2)
        des = "Congrats on purchaing your "
        des += propertyName
        des += "."
        des +="\n\n"
        des += "Amount Paid: "
        des += propertyCost
        des += "gp"
        des += "\n"
        des += "Upkeep: "
        des += propertyUpkeep
        des += "gp"
        des +="\n\n"
        des +="Upkeep is paid weekly on **SUNDAY**."
        
elif inp1 == "list":
    title = "Property Types List"
    if inp2 == b:
        propertyTypes = load_json(get_gvar("323a57a9-300b-4077-9499-063af8669c0d"))
    elif inp2 == h:
        propertyTypes = load_json(get_gvar("4df294ea-6bf7-4b2a-ba25-6e76ecad8a84"))
    des = "**Property Types | Cost | Rent | Upkeep**"
    for x in propertyTypes:
        des += "\n"
        des += propertyTypes[x]['name']
        des += " | "
        des += propertyTypes[x]['cost']
        des += "gp | "
        des += propertyTypes[x]['rent']
        des += "gp | "
        des += propertyTypes[x]['upkeep']
        des += "gp"
else: 
    title = "Oops!"  
    des = "Please use format `!purchase <home/business> <property type> <rent/buy>`"
    des += "\n"
    des += "Please use quotation marks for property type."
    des += "\n"
    des += "To list property types `!purchase list <home/business>`"

</drac2>
-title "{{title}}"
-desc "{{des}}"
-footer "made by kait296"