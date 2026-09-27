embed
<drac2>
inp1 = "&1&"
inp2 = "&2&"
inp3 = "&3&"
inp4 = "&4&"
ch = character()

if inp1.lower() == "help":
    titles = "Alias Help"
    descript = "```language, skill, tool, armor, weapon, feat```"
    descript += "\n\n"
    descript += "Run `!train <option> help` to see all their options"
elif inp1.lower() == "language" or inp1.lower() == "skill" or inp1.lower() == "armor" or inp1.lower() == "feat"  or inp1.lower() == "tool" or inp1.lower() == "weapon":
    temp= load_json(get_gvar("b210145a-4766-4301-ab70-c2dd77ea70e9"))
    if inp2.lower() =="help":
        if inp1.lower() == "language":
            titles = "Language Options"
            descript = temp[inp1.lower()]
        elif inp1.lower() == "skill":
            titles = "Skill Options"
            descript = temp[inp1.lower()]
        elif inp1.lower() == "tool":
            titles = "Tool Options"
            descript = temp[inp1.lower()]
        elif inp1.lower() == "armor":
            titles = "Armor Options"
            descript = temp[inp1.lower()]
        elif inp1.lower() == "weapon":
            titles = "Weapon Options"
            descript = temp[inp1.lower()]
        elif inp1.lower() == "feat":
            titles = "Feat Options"
            descript = temp[inp1.lower()]
    else:
        x= load_json(get_gvar("d442d2b2-0504-4e5d-b644-f01f244470a8"))
        y = x[inp1][inp2]["name"]
        z = x[inp1][inp2]["modifier"]
        mod=0
        if z == "intelligenceMod":
            mod= intelligenceMod
        elif z == "wisdomMod":
            mod= wisdomMod
        elif z == "charismaMod":
            mod= charismaMod
        elif z == "strengthMod":
            mod= strengthMod
        elif z == "dexterityMod":
            mod= dexterityMod
        elif z == "constitutionMod":
            mod = constitutionMod


        if inp3 == "adv" or inp4 == "adv":
            di = "2d20kh1"
        elif inp3 == "dis" or inp4 == "dis":
            di = "2d20kl1"
        else:
            di = "1d20"
            
        
        a = vroll(di)
        holder = a.total
        
        if inp3 == "rt" and holder < 9:
            a=10
        b = holder + mod
        timesTrain = 20-mod


        # LOGIC!!!
        if b >= 10 and ch.cc_exists(y): #if pass and have counter
            ch.mod_cc(y, 1)
            total = ch.get_cc(y)
            pf = "Success!"

        elif b < 10 and ch.cc_exists(y): #if fail and have counter
            total = ch.get_cc(y)
            pf = "Fail!"

        elif b >= 10: #if pass and dont have counter
            ch.create_cc(y, 0, timesTrain,'none', None, 0)
            ch.mod_cc(y, 1)
            total = ch.get_cc(y)
            pf = "Success!"

        else: #if you fail
            ch.create_cc(y, 0, timesTrain,'none', None, 0)
            total = ch.get_cc(y)
            pf = "Fail!"
        desc = "{{y}}"
        descript = "Lets get down to business!"
        descript += "\n"
        descript += "You're training **"
        descript += y
        descript += "**."
        descript += "\n\n"
        descript += "**Check:**"
        descript += a
        descript += " + "
        descript += mod
        descript += " = "
        descript += b
        descript += "  "
        descript += pf
        descript += "\n\n"
        descript += "You've succeeded "
        descript += total
        descript += "/"
        descript += timesTrain
        titles = y
else: 
    titles = "Alias Help"
    descript = "```language, skill, tool, armor, weapon, feat```"
    descript += "\n\n"
    descript += "Run `!train <option> help` to see all their options"


</drac2>
-title "{{titles}}"
-desc "{{descript}}"
-footer "made by kait296 | !train help"
-thumb <image>