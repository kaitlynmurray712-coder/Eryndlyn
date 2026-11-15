embed
<drac2>
M=[(1,1,1),(2,2,1.5),(3,6,2),(7,10,2.5),(11,14,3),(15,99,4)]
X={"0":10,"1/8":25,"1/4":50,"1/2":100,"1":200,"2":450,"3":700,"4":1100,"5":1800,"6":2300,"7":2900,"8":3900,"9":5000,"10":5900,"11":7200,"12":8400,"13":10000,"14":11500,"15":13000,"16":15000,"17":18000,"18":20000,"19":22000,"20":25000,"21":33000,"22":41000,"23":50000,"24":62000,"25":75000,"26":90000,"27":105000,"28":120000,"29":135000,"30":155000}
T=[(),(25,50,75,100),(50,100,150,200),(75,150,225,400),(125,250,375,500),(250,500,750,1100),(300,600,900,1400),(350,750,1100,1700),(450,900,1400,2100),(550,1100,1600,2400),(600,1200,1900,2800),(800,1600,2400,3600),(1000,2000,3000,4500),(1100,2200,3400,5100),(1250,2500,3800,5700),(1400,2800,4300,6400),(1600,3200,4800,7200),(2000,3900,5900,8800),(2100,4200,6300,9500),(2400,4900,7300,10900),(2800,5700,8500,12700)]

args=&ARGS&
a=str(&ARGS&)[1:-1].replace("'","").replace(",","")

if len(args)<4:
    return "Usage: !enc <category> <CR page> <easy/medium/hard/deadly> <player levels...>"

typ=str(args[0]).lower()
page=str(args[1])
diff=str(args[2]).lower()

if diff not in ["easy","medium","hard","deadly"]:
    return "Invalid difficulty. Use easy, medium, hard, or deadly."

try:
    P=[int(i) for i in args[3:]]
except:
    return "Player levels must be numbers from 1 to 20."

if not P or any(i<1 or i>20 for i in P):
    return "Enter at least one player level from 1 to 20."

D=load_json(get_gvar("c4023066-52d3-4e4f-9cc5-0846b7d05de6"))

if typ not in D:
    return "Unknown monster category: "+typ

if page not in D[typ]:
    return "No CR page "+page+" exists for category "+typ+"."

pool=[z for z in D[typ][page] if str(z["CR"]) in X]

if not pool:
    return "No monsters with supported CRs found on page "+page+"."

V={"easy":0,"medium":1,"hard":2,"deadly":3}
di=V[diff]
E=sum(T[i][0] for i in P)
md=sum(T[i][1] for i in P)
h=sum(T[i][2] for i in P)
d=sum(T[i][3] for i in P)
goal=[E,md,h,d][di]


# Encounter search
L=[]
xp=0

upper=[md,h,d,None][di]

# Each state contains (base XP, monster list, score)
beam=[(0,[],0)]
bestL=[]
bestxp=0
bestscore=10**12

# Search up to 10 monsters
for count in range(1,11):

    newstates=[]

    for state in beam:
        for z in pool:

            nx=state[0]+X[str(z["CR"])]
            nl=state[1]+[z]

            # Official 2014 multiplier calculation
            m=0
            for j,r in enumerate(M):
                if r[0]<=count<=r[1]:
                    m=j

            if len(P)<3 and m<5:
                m+=1
            elif len(P)>5 and m>0:
                m-=1

            na=int(nx*M[m][2])

            # Score the encounter
            if na>=goal and (upper is None or na<upper):
                score=na-goal
            elif na<goal:
                score=100000+goal-na
            else:
                score=200000+na-upper

            newstates.append((nx,nl,score))

    if not newstates:
        break

    # Find the best combination without sorted()
    validfound=False
    localbest=10**12
    localxp=0
    localL=[]

    for state in newstates:
        nx=state[0]

        # Recalculate multiplier for this monster count
        m=0
        for j,r in enumerate(M):
            if r[0]<=count<=r[1]:
                m=j

        if len(P)<3 and m<5:
            m+=1
        elif len(P)>5 and m>0:
            m-=1

        na=int(nx*M[m][2])

        if na>=goal and (upper is None or na<upper):
            score=na-goal

            if score<localbest:
                localbest=score
                localxp=nx
                localL=state[1]
                validfound=True

        elif not validfound and state[2]<bestscore:
            bestscore=state[2]
            bestxp=nx
            bestL=state[1]

    if validfound:
        bestxp=localxp
        bestL=localL
        break

    # Keep a limited number of promising combinations
    beam=[]
    for state in newstates:
        if len(beam)<12:
            beam.append(state)
        else:
            worst=0
            for i,s in enumerate(beam):
                if s[2]>beam[worst][2]:
                    worst=i

            if state[2]<beam[worst][2]:
                beam[worst]=state


L=bestL
xp=bestxp

# Final official multiplier calculation
count=len(L)
m=0

for j,r in enumerate(M):
    if r[0]<=count<=r[1]:
        m=j

if len(P)<3 and m<5:
    m+=1
elif len(P)>5 and m>0:
    m-=1

adj=int(xp*M[m][2])

R="Trivial"
if adj>=E:R="Easy"
if adj>=md:R="Medium"
if adj>=h:R="Hard"
if adj>=d:R="Deadly"

monsters="\n".join("- "+z["name"]+" (CR "+str(z["CR"])+")" for z in L)
</drac2>
-title "Random Encounter: `!sh_enc {{a}}`"
-desc "**Requested difficulty:** {{diff.title()}}
**Actual difficulty:** {{R}}

**Monsters:**
{{monsters if monsters else 'No monsters selected.'}}

**Adjusted XP:** {{adj}}
**Base XP:** {{xp}}
**Multiplier:** ×{{M[m][2]}}

**Party thresholds**
Easy: {{E}}
Medium: {{md}}
Hard: {{h}}
Deadly: {{d}}"
