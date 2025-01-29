import csv
import json
import requests
import time
import os
import PySimpleGUI as sg #pip install pysimplegui
import pickle

from PIL import Image #pip install pillow
from io import BytesIO

import textwrap

import allygocards


#run allygocards.py to update list

'''
Response Information:

All Cards

    id - ID or Passcode of the card.
    name - Name of the card.
    type - The type of card you are viewing (Normal Monster, Effect Monster, Synchro Monster, Spell Card, Trap Card, etc.).
    frameType - The backdrop type that this card uses (normal, effect, synchro, spell, trap, etc.).
    desc - Card description/effect.
    ygoprodeck_url - Link to YGOPRODeck card page.

Monster Cards

    atk - The ATK value of the card.
    def - The DEF value of the card.
    level - The Level/RANK of the card.
    race - The card race which is officially called type (Spellcaster, Warrior, Insect, etc).
    attribute - The attribute of the card.

Spell/Trap Cards

    race - The card race which is officially called type for Spell/Trap Cards (Field, Equip, Counter, etc).

Card Archetype

    archetype - The Archetype that the card belongs to. We take feedback on Archetypes here.

Additional Response for Pendulum Monsters

    scale - The Pendulum Scale Value.

Additional Response for Link Monsters

    linkval - The Link Value of the card if it's of type "Link Monster".
    linkmarkers - The Link Markers of the card if it's of type "Link Monster". This information is returned as an array.
'''
def downloadImage(idno):
    image_url='https://images.ygoprodeck.com/images/cards_small/'+str(idno)+'.jpg'
    image_url2='https://images.ygoprodeck.com/images/cards/'+str(idno)+'.jpg'
    print("downloading "+str(idno))
    #print(image_url)
    #print(image_url2)
    img_data = requests.get(image_url).content
    with open('images_small/'+str(idno)+'_s.jpg', 'wb') as handler:
        handler.write(img_data)
    time.sleep(0.1)
    img_data = requests.get(image_url2).content
    with open('images/'+str(idno)+'.jpg', 'wb') as handler:
        handler.write(img_data)
    time.sleep(0.1)    

def printCard(card):
    print(card.name)
    print(card.quantity)
    print(card.ctype)
    try:
        print(card.atk)
        print(card.defence)
        print(card.level)
        print(card.attribute)
    except:
        pass
    print(card.race)
    try:
        print(card.scale)
    except:
        pass
    try:
        print(card.archetype)
    except:
        pass
    print(card.desc)
    #print(card.image_url)
    #print(card.idno)
    print("")


class card:
    def __init__(self, amount, name):
        self.quantity = amount
        self.name = name
    idno: int
    ctype: str
    frametype: str
    desc: str
    atk: int
    defence: int
    level: int
    race: str
    attribute: str
    archetype: str
    scale: int
    imgbuf: BytesIO
    sets: str


filename = "all-folders.csv"
filename2 = "data.json"

if not os.path.isfile(filename2):
    allygocards.downloadallcardsjson()
if not os.path.exists("images/"):
    os.makedirs("images/")
if not os.path.exists("images_small/"):
    os.makedirs("images_small/")
if not os.path.isfile(filename):
    print("Download cardlist from dragon shield first")
    exit()

cardlist=[]
loaded=[]
loadedfull=[]
    
if not os.path.isfile("cache"):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csvfile=csvfile.readlines()[2:]
        reader = csv.reader(csvfile)
        firstSkip=True
        for row in reader:
            if firstSkip:
                firstSkip=False
                continue
            breaking=False
            if row[3] not in ["Token", "Skill card"]:
                for a in cardlist:
                    if a.name == row[3]:
                        a.quantity+=int(row[1])
                        if a.sets.find(row[4]) < 0:
                            a.sets=a.sets+", "+row[4]
                        breaking=True
                        break
                if not breaking:
                    cardlist.append(card(int(row[1]), row[3]))
                    cardlist[len(cardlist)-1].sets=row[4]
    with open('data.json', "r", encoding='utf-8') as file:
        data = json.load(file)
        
    u_ctypes=[]
    u_atk=[]
    u_defs=[]
    u_levels=[]
    u_attributes=[]
    u_races=[]
    u_scales=[]
    u_archetypes=[]
    for a in cardlist:
        for b in data['data']:
            if b['type'] in ["Skill Card", "Token"]:
                continue
            '''if b['type'] not in u_ctypes:
                u_ctypes.append(b['type'])
            if b['race'] not in u_races:
                u_races.append(b['race'])'''
            if a.name.upper() == b['name'].upper():
                a.idno=b['id']
                a.ctype=b['type']
                a.frametype=b['frameType']
                a.desc=b['desc']
                try:
                    a.archetype=b['archetype']
                except:
                    pass
                try:
                    a.atk=b['atk']
                except:
                    pass
                try:
                    if b['def'] is None:
                        a.defence=0
                    else:
                        a.defence=b['def']
                except:
                    pass
                try:
                    a.level=b['level']
                except:
                    pass
                try:
                    a.race=b['race']
                except:
                    pass    
                try:
                    a.attribute=b['attribute']
                except:
                    pass
                try:
                    a.scale=b['scale']
                except:
                    pass
                try:
                    a.level=b['linkval']
                except:
                    pass
                if not os.path.isfile("images/"+str(a.idno)+".jpg"):
                    downloadImage(a.idno)
                    
    cardlist.sort(key=lambda x: x.name, reverse=False)
    for i in cardlist:
        image = Image.open("images_small/"+str(i.idno)+"_s.jpg")
        i.imgbuf=BytesIO()
        image.save(i.imgbuf, format="PNG")

    
    with open("cache", "wb") as cachefile:
        pickle.dump(cardlist, cachefile)
    
        
else:
    with open("cache", 'rb') as cachelist:
        cardlist=pickle.load(cachelist)

imagefull = Image.open("images/89631139.jpg")
loadedfull.append(BytesIO()) 
imagefull.save(loadedfull[0], format="PNG")



monsterracelist=['Aqua', 'Beast', 'Beast-Warrior', 'Creator God', 'Cyberse', 'Dinosaur', 'Divine-Beast', 'Dragon', 'Fairy', 'Fiend', 'Fish', 'Illusion', 'Insect', 'Machine', \
'Plant', 'Psychic', 'Pyro', 'Reptile', 'Rock', 'Sea Serpent', 'Spellcaster', 'Thunder', 'Warrior', 'Winged Beast', 'Wyrm', 'Zombie']
spellracelist=['Continuous', 'Equip', 'Field', 'Normal', 'Quick-Play', 'Ritual']
trapracelist=['Continuous', 'Counter', 'Normal']

'''['Effect Monster', 'Flip Effect Monster', 'Flip Tuner Effect Monster', 'Fusion Monster', 'Gemini Monster', \
'Link Monster', 'Normal Monster', 'Normal Tuner Monster', 'Pendulum Effect Fusion Monster', 'Pendulum Effect Monster', \
'Pendulum Effect Ritual Monster', 'Pendulum Flip Effect Monster', 'Pendulum Normal Monster', 'Pendulum Tuner Effect Monster', \
'Ritual Effect Monster', 'Ritual Monster', 'Spirit Monster', 'Synchro Monster', 'Synchro Pendulum Effect Monster', \
'Synchro Tuner Monster', 'Toon Monster', 'Tuner Monster', 'Union Effect Monster', 'XYZ Monster', 'XYZ Pendulum Effect Monster']'''


#big 4 separation
monstertab=['Effect Monster', 'Flip Effect Monster', 'Flip Tuner Effect Monster', 'Gemini Monster', \
                'Normal Monster', 'Normal Tuner Monster', 'Pendulum Effect Monster', \
                'Pendulum Effect Ritual Monster', 'Pendulum Flip Effect Monster', 'Pendulum Normal Monster', 'Pendulum Tuner Effect Monster', \
                'Ritual Effect Monster', 'Ritual Monster', 'Spirit Monster', \
                'Toon Monster', 'Tuner Monster', 'Union Effect Monster']
spelltab=['Spell Card']
traptab=['Trap Card']
extradecktab=['Fusion Monster',\
                'Link Monster', 'Pendulum Effect Fusion Monster', \
                'Synchro Monster', 'Synchro Pendulum Effect Monster', \
                'Synchro Tuner Monster', 'XYZ Monster', 'XYZ Pendulum Effect Monster']


#monster separation
normalmonsters=['Normal Monster', 'Normal Tuner Monster', 'Pendulum Normal Monster','Ritual Monster']


effectmonsters=['Effect Monster', 'Flip Effect Monster', 'Flip Tuner Effect Monster', 'Gemini Monster', \
                'Pendulum Effect Fusion Monster', 'Pendulum Effect Monster', \
                'Pendulum Effect Ritual Monster', 'Pendulum Flip Effect Monster', 'Pendulum Tuner Effect Monster', \
                'Ritual Effect Monster', 'Spirit Monster', \
                'Toon Monster', 'Tuner Monster', 'Union Effect Monster']
ritualmonsters=['Pendulum Effect Ritual Monster', 'Ritual Effect Monster', 'Ritual Monster']
fusionmonsters=['Fusion Monster', 'Pendulum Effect Fusion Monster']
synchromonsters=['Synchro Monster', 'Synchro Pendulum Effect Monster','Synchro Tuner Monster']
pendulummonsters=['Pendulum Effect Fusion Monster', 'Pendulum Effect Monster', \
                'Pendulum Effect Ritual Monster', 'Pendulum Flip Effect Monster', 'Pendulum Normal Monster', 'Pendulum Tuner Effect Monster', \
                'Synchro Pendulum Effect Monster', \
                'XYZ Pendulum Effect Monster']
linkmonsters=['Link Monster']
xyzmonsters=['XYZ Monster', 'XYZ Pendulum Effect Monster']

toonmonsters=['Toon Monster']
unionmonsters=['Union Effect Monster']
flipmonsters=['Flip Effect Monster', 'Flip Tuner Effect Monster', 'Pendulum Flip Effect Monster']
tunermonsters=['Flip Tuner Effect Monster','Normal Tuner Monster', 'Pendulum Tuner Effect Monster', \
                'Synchro Tuner Monster', 'Toon Monster', 'Tuner Monster',]
geminimonsters=['Gemini Monster']
spiritmonsters=['Spirit Monster']



images=[2511, 27551, 39015, 50755, 111280, 131182, 132308, 213326, 313513, 423705, 653675, 691925,\
703897, 856784, 952523, 980973, 1041278, 1149109, 1295442, 1329620, 1475311, 1539051, 1546123, 1571945,\
1784686, 1825445, 1855886, 1876841, 1945387, 1948619, 2084239, 2089016, 2134346, 2204140, 2263869] #test data


def newImage(window, navlocator, cardlist, loadedfull):
    printCard(cardlist[navlocator])
    imagefull = Image.open("images/"+str(cardlist[navlocator].idno)+".jpg")
    loadedimage=BytesIO()
    imagefull.save(loadedimage, format="PNG")
    window["-IMAGEBIG-"].update(data=loadedimage.getvalue(), subsample=2)
    
def scroll(window, navlocator):
    for a in range(0, 24):
        if a+navlocator < len(cardlist):
            window["-IMAGE"+str(a)+"-"].update(data=cardlist[a+navlocator].imgbuf.getvalue(), subsample=2)
        else:
            window["-IMAGE"+str(a)+"-"].update(filename="")

navlocator=0
#counter=0


row1=[]
row2=[]
row3=[]
row4=[]

for a in range(0,6):
    row1.append(sg.Image(key="-IMAGE"+str(a)+"-", subsample=2, enable_events=True))
for a in range(6,12):
    row2.append(sg.Image(key="-IMAGE"+str(a)+"-", subsample=2, enable_events=True))
for a in range(12,18):
    row3.append(sg.Image(key="-IMAGE"+str(a)+"-", subsample=2, enable_events=True))
for a in range(18,24):
    row4.append(sg.Image(key="-IMAGE"+str(a)+"-", subsample=2, enable_events=True))


biglistcolumn = sg.vtop(sg.Column([row1, row2, row3, row4], scrollable=False))
highlightcolumn = sg.Column([[sg.Image(key="-IMAGEBIG-")], [sg.Text("",key="-CARDNAME-")], [sg.Text("", key="-CARDEFFECT-")], [sg.Text("Amount:"), sg.Text("",key="-CARDCOUNT-")], [sg.Text("Sets:"), sg.Text("",key="-SETS-")]])


reversebox=sg.Checkbox("Reverse?", default=False)
lvlbox=sg.Checkbox("Enable", default=False)
scalebox=sg.Checkbox("Enable", default=False)
atkbox=sg.Checkbox("Enable", default=False)
defbox=sg.Checkbox("Enable", default=False)

selectionframe = [[sg.Button("All", key="4SEL-A"), sg.Button("Monsters", key="4SEL-M"), sg.Button("Spells", key="4SEL-S"), sg.Button("Traps", key="4SEL-T"), sg.Button("Extra Deck", key="4SEL-E") ]]
lvlmin=sg.Input("1",key="-LVLMIN-", size=(5,1), enable_events=False)
lvlmax=sg.Input("13",key="-LVLMAX-", size=(5,1), enable_events=False)
scalemin=sg.Input("0",key="-SCALEMIN-", size=(5,1), enable_events=False)
scalemax=sg.Input("13",key="-SCALEMAX-", size=(5,1), enable_events=False)
atkmin=sg.Input("-1",key="-ATKMIN-", size=(5,1), enable_events=False)
atkmax=sg.Input("5000",key="-ATKMAX-", size=(5,1), enable_events=False)
defmin=sg.Input("-1",key="-DEFMIN-", size=(5,1), enable_events=False)
defmax=sg.Input("5000",key="-DEFMAX-", size=(5,1), enable_events=False)
mfilterframe =  [
                    [sg.Button("All", key="MONST-A")],
                    [sg.Button("Normal", key="MONST-N")],
                    [sg.Button("Effect", key="MONST-E")],
                    [sg.Button("Ritual", key="MONST-R")],
                    [sg.Button("Fusion", key="MONST-F")],
                    [sg.Button("Synchro", key="MONST-S")],
                    [sg.Button("Pendulum", key="MONST-P")],
                    [sg.Button("XYZ", key="MONST-X")],
                    [sg.Button("Link", key="MONST-L")],
                    [sg.Text("")],
                    [sg.ButtonMenu("Attribute", ["-ATTRMENU-",["Light","Dark","Fire","Water","Earth","Wind","Divine"]], key="-ATTRMENU-")],
                    [sg.ButtonMenu("Racetype", ["-RACE-",monsterracelist], key="-RACE-")],
                    [sg.Text("Level/Link/Rank")],
                    [lvlbox],
                    [sg.Text("min"), lvlmin,sg.Text("max:"), lvlmax],
                    [sg.Text("SCALE")],
                    [scalebox],
                    [sg.Text("min"), scalemin,sg.Text("max:"), scalemax],
                    [sg.Text("ATK")],
                    [atkbox],
                    [sg.Text("min"), atkmin,sg.Text("max:"), atkmax],
                    [sg.Text("DEF")],
                    [defbox],
                    [sg.Text("min"), defmin,sg.Text("max:"), defmax],
                    [sg.Button("Limit", key="-MINMAX-")]
                ]
# layout = [[sg.ButtonMenu('not used',  ['Menu', ['Menu item 1::optional_key', 'Menu item 2']])]]               
sfilterframe =  [
                    [sg.Button("All", key="SPELL-A")],
                    [sg.Button("Normal", key="SPELL-N")],
                    [sg.Button("Ritual", key="SPELL-R")],
                    [sg.Button("Equip", key="SPELL-E")],
                    [sg.Button("Quick-play", key="SPELL-Q")],
                    [sg.Button("Field", key="SPELL-F")],
                    [sg.Button("Continuous", key="SPELL-C")]
                ] 
tfilterframe =  [
                    [sg.Button("All", key="TRAP-A")],
                    [sg.Button("Normal", key="TRAP-N")],
                    [sg.Button("Continuous", key="TRAP-STAY")],
                    [sg.Button("Counter", key="TRAP-FAST")]
                ]   

textfilterframe =   [ 
                        [sg.Input(key="-TEXTINPUT-", enable_events=False)],
                        [sg.Button("Search", key="-TEXTSEARCH-")]
                    ]

stfilterframe = [   
                    [sg.vtop(sg.Frame("Spell Filters", sfilterframe)), sg.vtop(sg.Frame("Trap Filters", tfilterframe))],
                    [sg.Text("")],
                    [sg.Frame("Text search", textfilterframe)]
                ]

sortingframe =  [
                    [sg.ButtonMenu("Sort By", ["-SORT-",["ATK","DEF","Name","Level","Quantity",]], key="-SORT-"), reversebox]
                ]
             
filtersortframe =   [ 
                        [sg.Frame("Card type", selectionframe)],
                        [sg.Frame("Monster Filters", mfilterframe), sg.vtop(sg.Frame("", stfilterframe))],
                        [sg.Frame("Sorting", sortingframe)]    
                    ]

layout = [[biglistcolumn, sg.vtop(highlightcolumn), sg.Frame("Filtering and Sorting", filtersortframe), sg.Button('Exit')]]

window = sg.Window('YGO Manager', layout, return_keyboard_events=True, finalize=True, size=(1800, 1000))
for a in range(0, 24):
    window["-IMAGE"+str(a)+"-"].update(data=cardlist[a].imgbuf.getvalue(), subsample=2)
window["-IMAGEBIG-"].update(data=loadedfull[0].getvalue(), subsample=2)

wrapper=textwrap.TextWrapper(width=70) 

fullcardlist=cardlist

def updateCardDisplay(window, newlist):
    for a in range(0, 24):
        try:
            if a < len(newlist):
                window["-IMAGE"+str(a)+"-"].update(data=newlist[a].imgbuf.getvalue(), subsample=2)
            else:
                window["-IMAGE"+str(a)+"-"].update(filename="")
        except:
            pass


def reorgcardlist(window, cardlist, filtertype):
    newlist=[]
    if filtertype.find("4SEL")>=0 or filtertype.find("MONST")>=0:
        if filtertype == "4SEL-A":
            for a in range(0, 24):
                if a+navlocator < len(cardlist):
                    window["-IMAGE"+str(a)+"-"].update(data=fullcardlist[a+navlocator].imgbuf.getvalue(), subsample=2)
                else:
                    window["-IMAGE"+str(a)+"-"].update(filename="")
            return fullcardlist
            
        elif filtertype == "4SEL-M":
            checkagainst=monstertab
        elif filtertype == "4SEL-S":
            checkagainst=spelltab 
        elif filtertype == "4SEL-T":
            checkagainst=traptab
        elif filtertype == "4SEL-E":
            checkagainst=extradecktab 
            
        elif filtertype == "MONST-A":
            checkagainst=monstertab
        elif filtertype == "MONST-N":
            checkagainst=normalmonsters #23
        elif filtertype == "MONST-E":
            checkagainst=effectmonsters
        elif filtertype == "MONST-R":
            checkagainst=ritualmonsters
        elif filtertype == "MONST-F":
            checkagainst=fusionmonsters
        elif filtertype == "MONST-P":
            checkagainst=pendulummonsters
        elif filtertype == "MONST-L":
            checkagainst=linkmonsters
        elif filtertype == "MONST-S":
            checkagainst=synchromonsters
        elif filtertype == "MONST-X":
            checkagainst=xyzmonsters
        
        for a in cardlist:
            if a.ctype in checkagainst:
                newlist.append(a)
    
    if filtertype in ["LIGHT", "DARK", "FIRE", "WATER", "EARTH", "WIND", "DIVINE"]:
        for a in cardlist:
            try:
                if a.attribute == filtertype:
                    newlist.append(a)
            except:
                pass
    if filtertype in monsterracelist:
        for a in cardlist:
            try:
                if a.race == filtertype:
                    newlist.append(a)
            except:
                pass
    if filtertype.find("SPELL")>=0 or filtertype.find("TRAP")>=0:
        if filtertype == "SPELL-A":
            checkagainst = spellracelist
        elif filtertype == "SPELL-N" or filtertype == "TRAP-N":
            checkagainst = "Normal"
        elif filtertype == "SPELL-C" or filtertype == "TRAP-STAY":
            checkagainst = "Continuous"
        elif filtertype == "SPELL-R":
            checkagainst = "Ritual"
        elif filtertype == "SPELL-E":
            checkagainst = "Equip"
        elif filtertype == "SPELL-Q":
            checkagainst = "Quick-Play"
        elif filtertype == "SPELL-F":
            checkagainst = "Field"
        elif filtertype == "TRAP-FAST":
            checkagainst = "Counter"
        elif filtertype == "TRAP-A":
            checkagainst = trapracelist
            
        if filtertype.find("SPELL")>=0:
            checktype=spelltab
        if filtertype.find("TRAP")>=0:
            checktype=traptab
            
        for a in cardlist:
            try:
                if a.ctype in checktype and a.race in checkagainst:
                    newlist.append(a)
            except:
                pass
    print("checkagainst "+filtertype)
    print("cardlist len "+str(len(cardlist)))
    print("newlist size "+str(len(newlist)))
    updateCardDisplay(window, newlist)
    return newlist
    
    

def textsearch(cardlist, text):
    avoid=['', "", " ", "AND", "OR", "THE", "ON", "IN", "ARE", "TO", "OF"]
    newlist=[]
    print(text)
    if text == "":
        return cardlist
    
    splitted=text.upper().split(" ")
    print(splitted)
    for a in splitted:
        if a in avoid:
            splitted.remove(a)
    if len(splitted) > 1:
        for a in cardlist:
            if all(x in a.name.upper() for x in splitted) or all(x in a.desc.upper() for x in splitted) and a not in newlist:
                newlist.append(a)
    else:
        for a in cardlist:
            if splitted[0] in a.name.upper() or splitted[0] in a.desc.upper():
                newlist.append(a)
    return newlist
    

def sort(cardlist, event, rev):
    print(event)
    if event =="ATK":
        cardlist.sort(reverse=rev, key=byAtk)
    elif event =="DEF":
        cardlist.sort(reverse=rev, key=byDef)
    elif event == "Name":
        cardlist.sort(reverse=rev, key=byName)
    elif event == "Level":
        cardlist.sort(reverse=rev, key=byLvl)
    elif event == "Quantity":
        cardlist.sort(reverse=rev, key=byQuant)
    return cardlist

def byAtk(e):
    try:
        return e.atk
    except:
        return -1
def byDef(e):
    try:
        return e.defence
    except:
        return -1
def byName(e):
    return e.name
def byQuant(e):
    return e.quantity
def byLvl(e):
    try:
        return e.level
    except:
        return -1

def limiters(cardlist, lvlmin, lvlmax, scalemin, scalemax, atkmin, atkmax, defmin, defmax, lvlenable, scaleenable, atkenable, defenable):
    newlist=[]
    add=True
    for a in cardlist:
        add=True
        try:
            if lvlenable:
                if a.level<lvlmin or a.level>lvlmax:
                    add=False
            if scaleenable:
                if a.scale<scalemin or a.scale>scalemax:
                    add=False
            if atkenable:
                if a.atk<atkmin or a.atk>atkmax:
                    add=False
            if defenable:
                if a.defence<defmin or a.defence>defmax:
                    add=False
            if add:
                newlist.append(a)
        except:
            pass
    return newlist

prevtextlen=0

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "MouseWheel:Up" and navlocator >=6:
        navlocator=navlocator-6
        scroll(window, navlocator)
    if event == "MouseWheel:Down" and navlocator+24 < len(cardlist):
        navlocator=navlocator+6
        scroll(window, navlocator)
    if event.find("IMAGE")>=0:
        print()
        newImage(window, navlocator+int(event[6:-1]), cardlist, loadedfull)
        window["-CARDNAME-"].update(cardlist[navlocator+int(event[6:-1])].name)
        window["-CARDEFFECT-"].update(wrapper.fill(text=cardlist[navlocator+int(event[6:-1])].desc))
        window["-CARDCOUNT-"].update(wrapper.fill(text=str(cardlist[navlocator+int(event[6:-1])].quantity)))
        window["-SETS-"].update(wrapper.fill(text=str(cardlist[navlocator+int(event[6:-1])].sets)))
    if event.find("4SEL")>=0:
        cardlist=reorgcardlist(window, fullcardlist, event)
        navlocator=0
    if event.find("MONST")>=0 or event.find("SPELL")>=0 or event.find("TRAP")>=0:
        print(event)
        cardlist=reorgcardlist(window, fullcardlist, event)
        navlocator=0
    if event.find("-ATTRMENU-")>=0:
        cardlist=reorgcardlist(window, cardlist, values[event].upper())
        navlocator=0
    if event.find("-RACE-")>=0:
        cardlist=reorgcardlist(window, cardlist, values[event])
        navlocator=0
    if event.find("-TEXTSEARCH-")>=0:
        #if len(window["-TEXTINPUT-"].get()) > prevtextlen:
        #    cardlist=textsearch(cardlist, window["-TEXTINPUT-"].get())
        #else:
        cardlist=textsearch(fullcardlist, window["-TEXTINPUT-"].get())
        navlocator=0
        updateCardDisplay(window, cardlist)
        prevtextlen=len(window["-TEXTINPUT-"].get())
    if event.find("MINMAX")>=0:
        
        cardlist=limiters(cardlist,int(lvlmin.get()), int(lvlmax.get()), int(scalemin.get()), int(scalemax.get()), int(atkmin.get()), int(atkmax.get()), int(defmin.get()), int(defmax.get()), lvlbox.get(), scalebox.get(), atkbox.get(), defbox.get())
        navlocator=0
        updateCardDisplay(window, cardlist)
    if event.find("-SORT-")>=0:
        cardlist=sort(cardlist, values[event], reversebox.get())
        navlocator=0
        updateCardDisplay(window, cardlist)
        
    
window.close()


'''
for a in cardlist:
    showlist=[]
    if a.attribute in attrselect and a.race in raceselect and a.atk in range(atklow, atkhigh) and a.defence in range(deflow, defhigh) and a.level in range(levellow, levelhigh):
        showlist.append(a)
        
'''