"""
********************************************************************************
Prototype Cookie Clicker Garden simulator
********************************************************************************
Save valuable time and cookies with this simulator
"""

import sys
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

"""
ToolTip class more or less taken from here:
http://www.voidspace.org.uk/python/weblog/arch_d7_2006_07_01.shtml
and modified a little based on stuff from here:
https://stackoverflow.com/questions/3221956/
"""
class ToolTip(object):

    def __init__(self, widget):
        self.wraplength = 180
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self):
        # Display text in tooltip window
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "9", "normal"),
                      wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def settext(self, text):
        self.text = text

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    toolTip.settext(text)
    def enter(event):
        toolTip.showtip()
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return toolTip

"""
***********************************
STEP 1: SETUP
***********************************
"""

# Set Window items
root = Tk()
root.geometry("440x320")
root.title("Cookie Clicker Garden Simulator")

# Initialize variables
# All plants
PLANTS = [
    "-",    # none or nothing
    "Bak",  # baker's wheat
    "Thm",  # thumbcorn
    "Cro",  # chronerice
    "Gdm",  # gildmillet
    "OCl",  # ordinary clover
    "GCl",  # golden clover
    "Shl",  # shimmerlilly
    "Eld",  # elderwort
    "Ber",  # baker's berry
    "Cho",  # chocoroot
    "WCh",  # white chocoroot
    "Med",  # meddleweed
    "Wsk",  # whiskerbloom
    "Chr",  # chimerose
    "Ntl",  # nursetulip
    "Drf",  # drowsyfern
    "Wdl",  # wardlichen
    "Knm",  # keenmoss
    "Qnb",  # queenbeet
    "JQb",  # juicy queenbeet
    "Dkt",  # duketater
    "Skb",  # shriekbulb
    "Tdg",  # tidygrass
    "Evd",  # everdaisy
    "WMd",  # white mildew
    "BMd",  # brown mold
    "Crs",  # crumbspore
    "Dsm",  # doughshroom
    "Gml",  # glovemorel
    "Chc",  # cheapcap
    "FBl",  # fool's bolete
    "Wkg",  # wrinklegill
    "GnR",  # green rot
    "Icp"   # ichorpuff
]

# Dictionary for full plant names
PLANTNAMES = {
    "-":"Nothing",
    "Bak":"Baker's Wheat",
    "Thm":"Thumbcorn",
    "Cro":"Chronerice",
    "Gdm":"Gildmillet",
    "OCl":"Ordinary Clover",
    "GCl":"Golden Clover",
    "Shl":"Shimmerlilly",
    "Eld":"Elderwort",
    "Ber":"Baker's Berry",
    "Cho":"Chocoroot",
    "WCh":"White Chocoroot",
    "Med":"Meddleweed",
    "Wsk":"Whiskerbloom",
    "Chr":"Chimerose",
    "Ntl":"Nursetulip",
    "Drf":"Drowsyfern",
    "Wdl":"Wardlichen",
    "Knm":"Keenmoss",
    "Qnb":"Queenbeet",
    "JQb":"Juicy Queenbeet",
    "Dkt":"Duketater",
    "Skb":"Shriekbulb",
    "Tdg":"Tidygrass",
    "Evd":"Everdaisy",
    "WMd":"White Mildew",
    "BMd":"Brown Mold",
    "Crs":"Crumbspore",
    "Dsm":"Doughshroom",
    "Gml":"Glovemorel",
    "Chc":"Cheapcap",
    "FBl":"Fool's Bolete",
    "Wkg":"Wrinklegill",
    "GnR":"Green Rot",
    "Icp":"Ichorpuff"
}

# All plant effects
EFFECTS = [
    "",                 # 0
    "CpS",
    "CpC",
    "Cursor CpS",
    "Grandma CpS",
    "Rand Drops",       # 5
    "Milk Effect",
    "Reindeer Gains",
    "Reindeer Freq",
    "Build/Upgrade Cost",
    "GC Gains",         # 10
    "GC Effect Length",
    "GC Freq",
    "GC Duration",
    "WC Gains",
    "WC Freq",          # 15
    "WC Chance",
    "Wrinkler Spawn",
    "Wrinkler Digenstion"
]

# Encoded list of effects per plant
# Each element represents a plant in the PLANTS list, as a list
# first list inside is the effect from EFFECTS list
# second list is the magnitude of each effect, as a %
PLANTEFFECTS = [
    [[],[]],
    [[1],[1]],
    [[2],[2]],
    [[4],[3]],
    [[10,11],[1,0.1]],
    [[12],[1]],
    [[12],[3]],
    [[10,12,5],[1,1,1]],
    [[14,15,4],[1,1,1]],
    [[1],[1]],
    [[1],[1]],
    [[10],[1]],
    [[],[]],
    [[6],[0.2]],
    [[7,8],[1,1]],
    [[1],[-2]],
    [[1,2,12],[3,-5,-10]],
    [[16,17],[-2,-15]],
    [[5],[3]],
    [[11,1],[0.3,-2]],
    [[1],[-10]],
    [[],[]],
    [[1],[-2]],
    [[],[]],
    [[],[]],
    [[1],[1]],
    [[1],[-1]],
    [[],[]],
    [[],[]],
    [[2,3,1],[4,1,-1]],
    [[9],[-0.2]],
    [[12,10,13,11],[2,-5,-2,-2]],
    [[17,18],[2,1]],
    [[13,12,5],[0.5,1,1]],
    [[],[]]
]

# types of soil
SOILS = [
    ("Dirt",1),
    ("Fertilizer",2),
    ("Clay",3),
    ("Pebbles",4),
    ("Wood Chips",5)
]

# soil effects
SOILEFFECTS = [0,1,0.75,1.25,0.25,0.25]
SOILWEEDS = [0,1,1.2,1,0.1,0.1]

soil = IntVar()
soil.set(1)
gardenTiles = [ StringVar() for i in range(36)]
for i in range(36):
    gardenTiles[i].set(PLANTS[0])

gardenFill = StringVar()
gardenFill.set(PLANTS[0])
plotEffects = [1] * 36
plotAging = [1] * 36
plotFungus = [1] * 36

# Initialize functions
def AddBoost(c, s, m, plotEffects):
    # center, size, magnitude
    x = c // 6
    y = c % 6
    for i in range(max(x - s, 0), min(x + s + 1, 6)):
        for j in range(max(y - s, 0), min(y + s + 1, 6)):
            if i!=x or j!=y:
                e = plotEffects[i * 6 + j]
                plotEffects[i * 6 + j] = m * e
    return plotEffects

def NormalizeMult(boost, mult):
    newBoost = boost
    if boost >= 1:
        newBoost = (boost-1)*mult+1
    elif mult >= 1:
        newBoost = 1/((1/boost)*mult)
    else:
        newBoost = 1-(1-boost)*mult
    return newBoost

def RecalcPlotBoost():
    # This is the actual math that is in cookie clicker, its weird
    # do aging in here too, why not
    # and fungicide, live a little
    plotEffects = [1] * 36
    global plotAging
    global plotFungus
    plotAging = [1] * 36
    plotFungus = [1] * 36
    mult = SOILEFFECTS[soil.get()]
    for i in range(36):
        plant = gardenTiles[i].get()
        boost = 1
        aging = 1
        fungus = 1
        radius = 1
        applyEffect = False
        applyAging = False
        applyFungus = False
        if plant == "JQb":
            boost = 0.8
            applyEffect = True
        elif plant == "Ntl":
            boost = 1.2
            applyEffect = True
        elif plant == "Skb":
            boost = 0.95
            applyEffect = True
        elif plant == "Icp":
            boost = 0.5
            aging = 0.5
            applyEffect = True
            applyAging = True
        elif plant == "Eld":
            aging = 1.03
            applyAging = True
        elif plant == "Tdg":
            fungus = 0
            radius = 2
            applyFungus = True
        elif plant == "Evd":
            fungus = 0
            applyFungus = True
        
        boost = NormalizeMult(boost, mult)
        aging = NormalizeMult(aging, mult)

        if applyEffect:
            plotEffects = AddBoost(i,1,boost,plotEffects)
        if applyAging:
            plotAging = AddBoost(i,1,aging, plotAging)
        if applyFungus:
            plotFungus = AddBoost(i, radius, fungus, plotFungus)
    return plotEffects

def EffectToString(effects, weights):
    tmpstr = ""
    for i in range(len(effects)):
        tmpstr += str(round(weights[i], 2))
        tmpstr += "% "
        tmpstr += EFFECTS[effects[i]]
        tmpstr += ", "
    return tmpstr

def RecalcEffects():
    tmpstr = ""
    effects = []
    weights = []
    global plotEffects
    plotEffects = RecalcPlotBoost()
    j = 0
    for plant in gardenTiles:
        idx = PLANTS.index(plant.get())
        numeffects = len(PLANTEFFECTS[idx][0])
        mult = SOILEFFECTS[soil.get()] * plotEffects[j]
        if numeffects > 0:
            for i in range(numeffects):
                if PLANTEFFECTS[idx][0][i] in effects:
                    fxidx = effects.index(PLANTEFFECTS[idx][0][i])
                    weights[fxidx] += PLANTEFFECTS[idx][1][i] * mult
                else:
                    effects.append(PLANTEFFECTS[idx][0][i])
                    weights.append(PLANTEFFECTS[idx][1][i] * mult)
        j += 1
    return EffectToString(effects, weights)

def MutationToString(muts, poss):
    retStr = ""
    for i in range(len(muts)):
        retStr += "\n"
        retStr += PLANTNAMES[muts[i]] + " ("
        retStr += str(round(100 * poss[i], 2)) + "%)"
    return retStr

def AddMutation(muts, poss, plant, chance):
    if plant in muts:
        idx = muts.index(plant)
        poss[idx] += chance
    else:
        muts.append(plant)
        poss.append(chance)

def WoodchipRecalc(poss):
    # I don't know probability and statistics that well, hope this is close
    for i in range(2):
        total = 0
        for chance in poss:
            total += chance
        if total >= 1:
            return
        for j in range(len(poss)):
            poss[j] += (1 - total) * poss[j]

def GetMuts(i):
    possMuts = []
    mutChance = []
    
    if (gardenTiles[i].get() != "-"):
        if (gardenTiles[i].get() == "Eld" or gardenTiles[i].get() == "Qnb" or
            gardenTiles[i].get() == "JQb" or gardenTiles[i].get() == "Dkt" or
            gardenTiles[i].get() == "Skb" or gardenTiles[i].get() == "Tdg" or
            gardenTiles[i].get() == "Evd" or plotFungus[i] != 1):
            return ""
            
        neighbors = {}
        x = i // 6
        y = i % 6
        for j in range(max(x - 1, 0), min(x + 2, 6)):
            for k in range(max(y - 1, 0), min(y + 2, 6)):
                if (j==x) != (k==y):
                    aPlant = gardenTiles[j * 6 + k].get()
                    if aPlant in neighbors:
                        neighbors[aPlant] += 1
                    else:
                        neighbors[aPlant] = 1
        if "Med" in neighbors:
            possMuts.append("Med")
            mutChance.append(0.05)
        if "Dsm" in neighbors:
            possMuts.append("Dsm")
            mutChance.append(0.03)
        if "Crs" in neighbors:
            possMuts.append("Crs")
            mutChance.append(0.03)
    else:
        neighbors = {}
        x = i // 6
        y = i % 6
        numNeighs = 0
        for j in range(max(x - 1, 0), min(x + 2, 6)):
            for k in range(max(y - 1, 0), min(y + 2, 6)):
                if j!=x or k!=y:
                    numNeighs += 1
                    aPlant = gardenTiles[j * 6 + k].get()
                    if aPlant in neighbors:
                        neighbors[aPlant] += 1
                    else:
                        neighbors[aPlant] = 1
        # because its easier than checking if it exists everytime
        for plant in PLANTS:
            if plant not in neighbors:
                neighbors[plant] = 0
        # whether fungus/weeds can grow, weed multipliers
        bFung = plotFungus[i] == 1
        wm = SOILWEEDS[soil.get()]
        cwm = min(wm, 1)
        # ALLLL the possibilities
        if neighbors["Bak"] >= 2:
            AddMutation(possMuts, mutChance, "Bak", 0.2)
            AddMutation(possMuts, mutChance, "Thm", 0.05)
            AddMutation(possMuts, mutChance, "Ber", 0.001)
        if neighbors["Bak"] >= 1 and neighbors["Thm"] >= 1:
            AddMutation(possMuts, mutChance, "Cro", 0.01)
        if neighbors["Thm"] >= 2:
            AddMutation(possMuts, mutChance, "Thm", 0.1)
            AddMutation(possMuts, mutChance, "Bak", 0.05)
        if neighbors["Cro"] >= 1 and neighbors["Thm"] >= 1:
            AddMutation(possMuts, mutChance, "Gdm", 0.03)
        if neighbors["Cro"] >= 2:
            AddMutation(possMuts, mutChance, "Thm", 0.02)
        if neighbors["Bak"] >= 1 and neighbors["Gdm"] >= 1:
            AddMutation(possMuts, mutChance, "OCl", 0.03)
            AddMutation(possMuts, mutChance, "GCl", 0.0007)
        if neighbors["OCl"] >= 1 and neighbors["Gdm"] >= 1:
            AddMutation(possMuts, mutChance, "Shl", 0.02)
        if neighbors["OCl"] >= 2 and neighbors["OCl"] < 5:
            AddMutation(possMuts, mutChance, "OCl", 0.007)
            AddMutation(possMuts, mutChance, "GCl", 0.0001)
        if neighbors["OCl"] >= 4:
            AddMutation(possMuts, mutChance, "GCl", 0.0007)
        if neighbors["Shl"] >= 1 and neighbors["Cro"] >= 1:
            AddMutation(possMuts, mutChance, "Eld", 0.01)
        if neighbors["Wkg"] >= 1 and neighbors["Cro"] >= 1:
            AddMutation(possMuts, mutChance, "Eld", 0.002)
        if neighbors["Bak"] >= 1 and neighbors["BMd"] >= 1:
            AddMutation(possMuts, mutChance, "Cho", 0.1)
        if neighbors["Cho"] >= 1 and neighbors["WMd"] >= 1:
            AddMutation(possMuts, mutChance, "WCh", 0.1)
        if neighbors["WMd"] >= 1 and neighbors["BMd"] <= 1 and bFung:
            AddMutation(possMuts, mutChance, "BMd", 0.5)
        if neighbors["BMd"] >= 1 and neighbors["WMd"] <= 1 and bFung:
            AddMutation(possMuts, mutChance, "WMd", 0.5)
        if neighbors["Med"] >= 1 and neighbors["Med"] <= 3 and bFung:
            AddMutation(possMuts, mutChance, "Med", (0.15 * cwm))
        if neighbors["Shl"] >= 1 and neighbors["WCh"] >= 1:
            AddMutation(possMuts, mutChance, "Wsk", 0.01)
        if neighbors["Shl"] >= 1 and neighbors["Wsk"] >= 1:
            AddMutation(possMuts, mutChance, "Chr", 0.05)
        if neighbors["Chr"] >= 2:
            AddMutation(possMuts, mutChance, "Chr", 0.005)
        if neighbors["Wsk"] >= 2:
            AddMutation(possMuts, mutChance, "Ntl", 0.05)
        if neighbors["Cho"] >= 1 and neighbors["Knm"] >= 1:
            AddMutation(possMuts, mutChance, "Drf", 0.005)
        if ((neighbors["Cro"] >= 1 and neighbors["Knm"] >= 1) or
            (neighbors["Cro"] >= 1 and neighbors["WMd"] >= 1)):
            AddMutation(possMuts, mutChance, "Wdl", 0.005)
        if neighbors["Wdl"] == 1:
            AddMutation(possMuts, mutChance, "Wdl", 0.05)
        if neighbors["GnR"] >= 1 and neighbors["BMd"] >= 1:
            AddMutation(possMuts, mutChance, "Knm", 0.1)
        if neighbors["Knm"] == 1:
            AddMutation(possMuts, mutChance, "Knm", 0.05)
        if neighbors["Cho"] >= 1 and neighbors["Ber"] >= 1:
            AddMutation(possMuts, mutChance, "Qnb", 0.01)
        if neighbors["Qnb"] >= 8:
            AddMutation(possMuts, mutChance, "JQb", 0.001)
        if neighbors["Qnb"] >= 2:
            AddMutation(possMuts, mutChance, "Dkt", 0.001)
        if neighbors["Crs"] == 1 and bFung:
            AddMutation(possMuts, mutChance, "Crs", 0.07)
        if neighbors["Crs"] >= 1 and neighbors["Thm"] >= 1 and bFung:
            AddMutation(possMuts, mutChance, "Gml", 0.02)
        if neighbors["Crs"] >= 1 and neighbors["Shl"] >= 1 and bFung:
            AddMutation(possMuts, mutChance, "Chc", 0.04)
        if neighbors["Dsm"] >= 1 and neighbors["GnR"] >= 1 and bFung:
            AddMutation(possMuts, mutChance, "FBl", 0.04)
        if neighbors["Crs"] >= 2 and bFung:
            AddMutation(possMuts, mutChance, "Dsm", 0.005)
        if neighbors["Dsm"] == 1 and bFung:
            AddMutation(possMuts, mutChance, "Dsm", 0.07)
        if neighbors["Dsm"] >= 2 and bFung:
            AddMutation(possMuts, mutChance, "Crs", 0.005)
        if neighbors["Dsm"] >= 1 and neighbors["BMd"] and bFung:
            AddMutation(possMuts, mutChance, "Wkg", 0.06)
        if neighbors["WMd"] >= 1 and neighbors["OCl"] >= 1 and bFung:
            AddMutation(possMuts, mutChance, "GnR", 0.05)
        if neighbors["Wkg"] >= 1 and neighbors["Eld"] >= 1:
            AddMutation(possMuts, mutChance, "Skb", 0.001)
        if neighbors["Eld"] >= 5:
            AddMutation(possMuts, mutChance, "Skb", 0.001)
        if neighbors["Dkt"] >= 3:
            AddMutation(possMuts, mutChance, "Skb", 0.005)
        if neighbors["Dsm"] >= 4:
            AddMutation(possMuts, mutChance, "Skb", 0.002)
        if neighbors["Qnb"] >= 5:
            AddMutation(possMuts, mutChance, "Skb", 0.001)
        if neighbors["Skb"] == 1:
            AddMutation(possMuts, mutChance, "Skb", 0.005)
        if neighbors["Bak"] >= 1 and neighbors["WCh"] >= 1:
            AddMutation(possMuts, mutChance, "Tdg", 0.002)
        if neighbors["Tdg"] >= 3 and neighbors["Eld"] >= 3:
            AddMutation(possMuts, mutChance, "Evd", 0.002)
        if neighbors["Eld"] >= 1 and neighbors["Crs"] >= 1 and bFung:
            AddMutation(possMuts, mutChance, "Icp", 0.002)
        # apply woodchip effects to chances
        if soil.get() == 5:
            WoodchipRecalc(mutChance)

        # if no neighbors, get weed spawn chance
        if neighbors["-"] == numNeighs and bFung:
            AddMutation(possMuts, mutChance, "Med", (0.002 * wm))
    return MutationToString(possMuts, mutChance)

def GetNewInfo(i):
    global plotEffects
    global plotAging
    global plotFungus
    retStr = "Planted: "
    retStr += PLANTNAMES[gardenTiles[i].get()]
    idx = PLANTS.index(gardenTiles[i].get())
    if len(PLANTEFFECTS[idx][0]) > 0:
        retStr += "\nEffects: "
        retStr += EffectToString(PLANTEFFECTS[idx][0], PLANTEFFECTS[idx][1])
    mult = SOILEFFECTS[soil.get()] * plotEffects[i]
    if plotEffects[i] != 1:
        retStr += "\nEffect Multiplier: "
        retStr += str(round(plotEffects[i], 2))
    if plotAging[i] != 1:
        retStr += "\nAging Multiplier: "
        retStr += str(round(plotAging[i], 2))
    if plotFungus[i] != 1:
        retStr += "\nWeed/Fungus Repellent: 100%"
    mutStr = GetMuts(i)
    if mutStr != "":
        retStr += "\nPossible Mutations:" + mutStr
    return retStr


"""
***********************************
STEP 2: BUILD
***********************************
"""
# Main garden tiles
gardenBtns = []
gardenTtps = []
for i in range(36):
    wid = OptionMenu(root,gardenTiles[i],
                   *PLANTS)
    wid.grid(row=(i % 6),column=(i // 6))
    gardenBtns.append(wid)
    t = createToolTip(wid, "Planted: Nothing")
    gardenTtps.append(t)

# These functions need to be below the tooltips but above buttons
def UpdateToolTips():
    for i in range(36):
        gardenTtps[i].settext(GetNewInfo(i))

def FillAll(event=None):
    tofill = gardenFill.get()
    for plant in gardenTiles:
        plant.set(tofill)
    return

def RefreshWindow(event=None):
    gardenStatus.config(state=NORMAL)
    gardenStatus.delete(1.0, END)
    gardenStatus.insert(END, RecalcEffects())
    gardenStatus.config(state=DISABLED)
    UpdateToolTips()
    return

# Soil selector
i = 0
for txt, val in SOILS:
    if i < 4:
        Radiobutton(root, text=txt, variable=soil, value=val).grid(
            row=6, column=i)
    else:
        Radiobutton(root, text=txt, variable=soil, value=val).grid(
            row=6, column=i, columnspan=2)
    i+=1

# Info box
gardenStatus = Text(root, height=4, width=58, relief=SUNKEN)
gardenStatus.grid(row=7,column=0,columnspan=6,rowspan=4)
gardenStatus.insert(END, "Garden effects will appear here after recalculation!")
gardenStatus.config(state=DISABLED)


# Extra buttons
Button(root, text="Recalculate",
               command=RefreshWindow).grid(row=11,column=0,columnspan=2)
Button(root, text="Fill All",
       command=FillAll).grid(row=11,column=3)
Label(root,text="with:").grid(row=11,column=4)
OptionMenu(root,gardenFill,*PLANTS).grid(row=11,column=5)

root.mainloop()
