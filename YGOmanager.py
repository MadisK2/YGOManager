import csv
import json
import requests
import time
import os
import PySimpleGUI as sg
import os

from PIL import Image
from io import BytesIO

import textwrap


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




filename = "all-folders.csv"
filename2 = "data.json"

cardlist=[]

with open(filename, 'r', encoding='utf-8') as csvfile:
    print("csvfile open")
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
                    breaking=True
                    break
            if not breaking:
                cardlist.append(card(int(row[1]), row[3]))    


with open('data.json', "r", encoding='utf-8') as file:
    print("datafile open")
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

'''for a in cardlist:
    if a.ctype not in u_ctypes:
        u_ctypes.append(a.ctype)
    try:
        if a.atk not in u_atk:
            u_atk.append(a.atk)
        if a.defence not in u_defs:
            u_defs.append(a.defence)
        if a.level not in u_levels:
            u_levels.append(a.level)
        if a.attribute not in u_attributes:
            u_attributes.append(a.attribute)
    except:
        pass
    if a.race not in u_races:
        u_races.append(a.race)
    try:
        if a.scale not in u_scales:
            u_scales.append(a.scale)
    except:
        pass
    try:
        if a.archetype not in u_archetypes:
            u_archetypes.append(a.archetype)
    except:
        pass'''
cardlist.sort(key=lambda x: x.name, reverse=False)
#u_ctypes.sort()
#u_atk.sort()
#u_defs.sort()
#u_levels.sort()
#u_attributes.sort()
#u_races.sort()
#u_scales.sort()
#u_archetypes.sort()

#print(u_ctypes)
#print(u_levels)
#print(u_attributes)
#print(u_races)
#print(u_scales)
#print(u_archetypes)

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
1784686, 1825445, 1855886, 1876841, 1945387, 1948619, 2084239, 2089016, 2134346, 2204140, 2263869]


def newImage(window, navlocator, cardlist, loadedfull):
    #printcard(cardlist[navlocator])
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
loaded=[]
loadedfull=[]
for i in cardlist:
    image = Image.open("images_small/"+str(i.idno)+"_s.jpg")
    i.imgbuf=BytesIO()
    image.save(i.imgbuf, format="PNG")

imagefull = Image.open("images/89631139.jpg")
loadedfull.append(BytesIO()) 
imagefull.save(loadedfull[0], format="PNG")

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
highlightcolumn = sg.Column([[sg.Image(key="-IMAGEBIG-")], [sg.Text("",key="-CARDNAME-")], [sg.Text("", key="-CARDEFFECT-")]])

selectionframe = [[sg.Button("All", key="4SEL-A"), sg.Button("Monsters", key="4SEL-M"), sg.Button("Spells", key="4SEL-S"), sg.Button("Traps", key="4SEL-T"), sg.Button("Extra Deck", key="4SEL-E") ]]
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
                    #[sg.Text("Racetype")],
                    [sg.Text("Level")],
                    [sg.Text("Pendulum Scale")],
                    [sg.Text("ATK slider")],
                    [sg.Text("DEF slider")]
                ]
# layout = [[sg.ButtonMenu('not used',  ['Menu', ['Menu item 1::optional_key', 'Menu item 2']])]]               
sfilterframe =  [
                    [sg.Text("All")],
                    [sg.Text("Normal")],
                    [sg.Text("Ritual")],
                    [sg.Text("Equip")],
                    [sg.Text("Quick-play")],
                    [sg.Text("Field")],
                    [sg.Text("Continuous")]
                ] 
tfilterframe =  [
                    [sg.Text("All")],
                    [sg.Text("Normal")],
                    [sg.Text("Continuous")],
                    [sg.Text("Counter")]
                ]   

textfilterframe =   [ 
                        [sg.Text("Name search")],
                        [sg.Text("Name box")],
                        [sg.Text("Description search")],
                        [sg.Text("desc box")]
                    ]

stfilterframe = [   
                    [sg.vtop(sg.Frame("Spell Filters", sfilterframe)), sg.vtop(sg.Frame("Trap Filters", tfilterframe))],
                    [sg.Text("")],
                    [sg.Frame("Text search", textfilterframe)]
                ]

sortingframe =  [
                    [sg.Text("by"), sg.Text("asc/desc")]
                ]
             
filtersortframe =   [ 
                        [sg.Frame("Card type", selectionframe)],
                        [sg.Frame("Monster Filters", mfilterframe), sg.vtop(sg.Frame("", stfilterframe))],
                        [sg.Frame("Sorting", sortingframe)]    
                    ]

layout = [[biglistcolumn, sg.vtop(highlightcolumn), sg.Frame("Filtering and Sorting", filtersortframe), sg.Button('Exit')]]

window = sg.Window('YGO Manager', layout, return_keyboard_events=True, finalize=True)
for a in range(0, 24):
    window["-IMAGE"+str(a)+"-"].update(data=cardlist[a].imgbuf.getvalue(), subsample=2)
window["-IMAGEBIG-"].update(data=loadedfull[0].getvalue(), subsample=2)

wrapper=textwrap.TextWrapper(width=70) 

fullcardlist=cardlist


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
    print("checkagainst "+filtertype)
    print("cardlist len "+str(len(cardlist)))
    print("newlist size "+str(len(newlist)))
    for a in range(0, 24):
        try:
            if a < len(newlist):
                window["-IMAGE"+str(a)+"-"].update(data=newlist[a].imgbuf.getvalue(), subsample=2)
            else:
                window["-IMAGE"+str(a)+"-"].update(filename="")
        except:
            pass
    return newlist

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
        print(event)
        newImage(window, navlocator+int(event[6:-1]), cardlist, loadedfull)
        window["-CARDNAME-"].update(cardlist[navlocator+int(event[6:-1])].name)
        window["-CARDEFFECT-"].update(wrapper.fill(text=cardlist[navlocator+int(event[6:-1])].desc))
    if event.find("4SEL")>=0:
        cardlist=reorgcardlist(window, fullcardlist, event)
        navlocator=0
        #window.refresh()
    if event.find("MONST")>=0:
        cardlist=reorgcardlist(window, fullcardlist, event)
        navlocator=0
    if event.find("-ATTRMENU-")>=0:
        print(event)
        print(values[event])
        cardlist=reorgcardlist(window, cardlist, values[event].upper())
        navlocator=0
    if event.find("-RACE-")>=0:
        cardlist=reorgcardlist(window, cardlist, values[event])
window.close()


 
