embed
<drac2>
char = character()
inp1 = "&1&" #Business, housing
inp2 = "&2&" #type
inp3 = "&3&" #buy/loan/partial
inp4 = "&4&" #partial payment
desc = "You're ready to purchase a "
desc += inp2.lower()
desc += "!"
desc += "\n"
#What type of property?
if inp1.lower() == "business":
    propertyTypes = load_json(get_gvar("323a57a9-300b-4077-9499-063af8669c0d"))
    loantype = "Business Loan"
    paymenttype = "businesspayment"
    if char.get_cvar("income"):
        income = char.get_cvar("income")
        temp = int(income) + int(propertyTypes[inp2.lower()]['payout'])
        char.set_cvar("income",temp)
    else: 
        char.set_cvar("income",propertyTypes[inp2.lower()]['payout'])
    
elif inp1.lower() == "house":
    propertyTypes = load_json(get_gvar("4df294ea-6bf7-4b2a-ba25-6e76ecad8a84"))
    loantype = "Housing Loan"
    paymenttype = "housepayment"
else:
    desc += "You have entered an invalid entry."

#Property info
propertyCost = propertyTypes[inp2.lower()]['cost']
propertyUpkeep = propertyTypes[inp2.lower()]['upkeep']
propertyRent = propertyTypes[inp2.lower()]['rent']

#Updates loan CC
if inp3.lower() == "loan":
    if char.cc_exists(loantype):
        char.mod_cc(loantype,int(propertyCost))
        desc += "\n"
        desc += "The amount "
        desc += propertyCost
        desc += " has been added to your "
        desc += inp1.lower()
        desc += "loan."
        desc += "\n"
        desc += "You now owe "
        desc += char.get_cc(loantype)
        desc += "gp"
        desc += "\n"
    else:
        #make loan
        char.create_cc(name=loantype, initial_value=propertyCost)
        desc += "\n"
        desc += "You have taken out a loan of "
        desc += propertyCost
        desc += "gp"
        desc += "\n"

    if char.get_cvar(paymenttype):
        math = int(char.get_cvar(paymenttype))
        temp = int(propertyRent) + math
        char.set_cvar(paymenttype,temp)
    else:
        char.set_cvar(paymenttype,propertyRent)
    desc += "\n"
    desc += "Your weekly payment will be "
    desc += char.get_cvar("rent")
    desc += "gp"
    desc += "\n"
elif inp3.lower() == "partial":
    char.coinpurse.modify_coins(gp=-int(inp4))
    if char.cc_exists(loantype):
        char.mod_cc(loantype,int(propertyCost))
        char.mod_cc(loantype,-int(inp4))
        desc += "\n"
        desc += "The amount "
        desc += propertyCost
        desc += " has been added to your "
        desc += inp1.lower()
        desc += "loan."
        desc += "\n"
        desc += "You now owe "
        desc += char.get_cc(loantype)
        desc += "gp"
        desc += "\n"
        desc += "You paid "
        desc += inp4
        desc += "gp on your new property"
    else:
        #make loan
        char.create_cc(name=loantype, initial_value=propertyCost)
        char.mod_cc(loantype,-int(inp4))
        desc += "\n"
        desc += "You have taken out a loan of "
        desc += propertyCost
        desc += "gp"
        desc += "\n"
        desc += "You paid "
        desc += inp4
        desc += "gp on your new property"
        desc += "\n"
    if char.get_cvar(paymenttype):
        math = int(char.get_cvar(paymenttype))
        temp = int(propertyRent) + math
        char.set_cvar(paymenttype,temp)
    else:
        char.set_cvar(paymenttype,propertyRent)
else:
    char.coinpurse.modify_coins(gp=-int(propertyCost))
    desc += "You have bought a "
    desc += inp2.lower()
    desc += "!"
    desc += "\n"
    desc += "You do not owe anything on theis property"
    desc += "\n"
    

#Updates variable for types of properties owned
if char.get_cvar(inp1):
    temp = char.get_cvar(inp1)
    temp += ","
    temp += inp2.lower()
    char.set_cvar(inp1, temp)
else:
    char.set_cvar(inp1, inp2.lower())

#Update upkeep
if char.get_cvar("upkeep"):
    temp = int(char.get_cvar("upkeep"))
    math = temp + int(propertyUpkeep)
    char.set_cvar("upkeep", math)
    desc += "\n"
    desc += "Your weekly upkeep for the new property will be "
    desc += propertyUpkeep
    desc += "gp"
    desc += "\n"
    desc += "Your total upkeep is now "
    desc += char.get_cvar("upkeep")
    desc += "gp"
else:
    char.set_cvar("upkeep", propertyUpkeep)
    desc += "\n"
    desc += "Your weekly upkeep for the new property will be "
    desc += propertyUpkeep
    desc += "gp"
    desc += "\n"
    desc += "Your total upkeep is now "
    desc += char.get_cvar("upkeep")
    desc += "gp"



#
</drac2>
-title "__Property Purchase__"
-desc "{{desc}}"
-footer "made by kait296 | !property <business/house> <type> <buy/partial/loan> <amnt for partial>"
-thumb "https://i.pinimg.com/736x/5d/dc/c7/5ddcc7e485c55abb0360e71356d84c57.jpg"


