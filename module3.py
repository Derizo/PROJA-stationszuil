import psycopg2
import datetime
from tkinter import *
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.request import urlopen
import json

def cyclePages():
    """
    Deze functie is gemaakt om te blijven loopen,
    zodat het vertoonde scherm constant door 3 paginas heen gaat,
    en de widgets in deze paginas dan ook meteen ververst.

    Deze functie werkt door een counter steeds te incrementen met 1.
    Dit herhaalt totdat de counter 3 is, dan wordt het gezet tot 0.
    De counter bepaalt welke pagina wordt ververst en geplaatsd op het scherm.
    """
    global counter
    global weerIcoonImage

    # Lijst van frames en kleurverandering buttons, zodat de button van de huidige pagina uniek is in kleur
    listPages = [pageComments, pageWeer, pageF]
    button1.config(bg="#003082")
    button2.config(bg="#003082")
    button3.config(bg="#003082")

    # Verversing en plaatsing van commentpagina
    if counter == 0:
        # Kleurverandering button
        button1.config(bg="#0063D3")

        # Dit is een psycopg2 query om laatste 5 comments op te halen.
        curs.execute("""
        SELECT naam,bericht,datum,tijd FROM Bericht
        ORDER BY datum DESC, tijd DESC
        LIMIT 5;""")
        laatste5Comments = curs.fetchall()

        # Textvariabelen aanmaak voor verversing comment pagina.
        # Al zijn er minder dan 5 comments opgehaald in de query,
        # Dan zal het de exception opvangen, dus stopt de var assignment daar.
        try:
            text1 = laatste5Comments[0][0] + " heeft op " +  laatste5Comments[1][2].strftime("%d:%m:%Y") + " " + laatste5Comments[1][3].strftime("%H:%M") + " dit achtergelaten: \n \n" + laatste5Comments[0][1]
            text2 = laatste5Comments[1][0] + " heeft op " +  laatste5Comments[1][2].strftime("%d:%m:%Y") + " " + laatste5Comments[1][3].strftime("%H:%M") + " dit achtergelaten: \n \n" + laatste5Comments[1][1]
            text3 = laatste5Comments[2][0] + " heeft op " +  laatste5Comments[2][2].strftime("%d:%m:%Y") + " " + laatste5Comments[2][3].strftime("%H:%M") + " dit achtergelaten: \n \n" + laatste5Comments[2][1]
            text4 = laatste5Comments[3][0] + " heeft op " +  laatste5Comments[3][2].strftime("%d:%m:%Y") + " " + laatste5Comments[3][3].strftime("%H:%M") + " dit achtergelaten: \n \n" + laatste5Comments[3][1]
            text5 = laatste5Comments[4][0] + " heeft op " +  laatste5Comments[4][2].strftime("%d:%m:%Y") + " " + laatste5Comments[4][3].strftime("%H:%M") + " dit achtergelaten: \n \n" + laatste5Comments[4][1]
        except:
            pass

        # Verversen van de comment labels, net zoals bij de var assignment
        # stopt het al vindt het geen textvariabele.
        try:
            comment1.config(text=text1, relief='groove', bg='#FFC917')
            comment2.config(text=text2, relief='groove', bg='#FFC917')
            comment3.config(text=text3, relief='groove', bg='#FFC917')
            comment4.config(text=text4, relief='groove', bg='#FFC917')
            comment5.config(text=text5, relief='groove', bg='#FFC917')
        except:
            pass

    # Verversing en plaatsing van weerpagina
    elif counter == 1:
        # Kleurverandering button
        button2.config(bg="#0063D3")

        # Ophalen data van OpenWeatherMap API
        weerAPI = urlopen("https://api.openweathermap.org/data/2.5/weather?zip=" + str(stationPostCode[stationVanZuil]) + ",NL&units=metric&appid=ec470c6042f44970faf3c330cd2d13cc")
        weerAPISTR = weerAPI.read().decode()
        weerAPIdict = json.loads(weerAPISTR)
        weerDict = weerAPIdict['weather']
        tempDict = weerAPIdict['main']

        # Data van interesse wordt opgeslagen in variabelen
        beschrijvingWeer = beschrijvingDict[weerDict[0]["main"]]
        vochtigheid = tempDict["humidity"]
        temp = round(tempDict['temp'], 1)
        windSnelheid = round((weerAPIdict['wind']['speed'] * 3.6), 1)
        weerIcoonImage = PhotoImage(file="images/weer/" + weerDict[0]["icon"] + ".png")

        # Verversing van widgets in weerpagina
        weerLabel2.config(text=beschrijvingWeer)
        weerLabel3.config(text=str(temp) + "° C")
        weerLabel4.config(text="Vochtigheid: " + str(vochtigheid) + "%")
        weerLabel5.config(text="Windsnelheid: " + str(windSnelheid) + " km/h")
        weerIcoon.config(image=weerIcoonImage)

    # Verversing en plaatsing van faciliteitenpagina
    elif counter == 2:
        # Globaal maken van de photoimages, zodat deze niet alleen in deze functie werken
        global fietsF
        global liftF
        global toiletF
        global pRF

        # Kleurverandering button
        button3.config(bg="#0063D3")

        # Dit is een psycopg2 query de faciliteiten van het gekozen station op te halen
        curs.execute("""
        SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service
        WHERE station_city = %s""",[stationVanZuil,])
        faciliteiten = curs.fetchall()

        # Booleans opslaan in variabelen
        ovFiets = faciliteiten[0][0]
        lift = faciliteiten[0][1]
        toilet = faciliteiten[0][2]
        pR = faciliteiten[0][3]

        # Al is de booleanvariabel True, dan wordt er een normaal plaatje gekozen
        # Anders wordt er een grijs plaatje gekozen
        if ovFiets == True:
            fietsF = PhotoImage(file='images/img_ovfiets.png')
        else:
            fietsF = PhotoImage(file='images/img_ovfiets_go.png')
        if lift == True:
            liftF = PhotoImage(file='images/img_lift.png')
        else:
            liftF = PhotoImage(file='images/img_lift_go.png')
        if toilet == True:
            toiletF = PhotoImage(file='images/img_toilet.png')
        else:
            toiletF = PhotoImage(file='images/img_toilet_go.png')
        if pR == True:
            pRF = PhotoImage(file='images/img_pr.png')
        else:
            pRF = PhotoImage(file='images/img_pr_go.png')

        # Verversing plaatjes faciliteitenpagina
        fietsI.config(image=fietsF)
        liftI.config(image=liftF)
        toiletI.config(image=toiletF)
        pRI.config(image=pRF)

    # Alle paginas van het scherm afhalen, en dan de huidige op het scherm zetten
    pageComments.pack_forget()
    pageWeer.pack_forget()
    pageF.pack_forget()
    listPages[counter].pack(side='right',expand='true',fill='both')

    # Counter increment, al is het meer dan 2 dan wordt het gereset tot 0
    counter += 1
    if counter > 2:
        counter = 0

    # Verversing van de tijd in zijbalk
    tijdNu = datetime.datetime.today()
    tijd = tijdNu.strftime("%H:%M")
    tijdDeclaratie.config(text= tijd)
    gui.after(10000,lambda: cyclePages())

def stationsKeuze():
    "Keuze van station ophalen, en redirect naar het stationshalscherm"
    global stationVanZuil
    global keuzeMenu

    # Ophalen data van input, al is er een exception, dan wordt de functie gestopt.
    # Dit is zodat je niet geredirect wordt al heb je nog geen keuze gemaakt.
    try:
        stationVanZuil = keuzeMenu.get(keuzeMenu.curselection())
    except TclError:
        return

    # Redirect
    switchPage(screen1,pageComments)

def switchPage(frame, page):
    "Functie om van pagina te veranderen, wordt huidig gebruikt voor de redirect"
    global screen2
    global stationVanZuil
    global counter

    # Terugzetting van plaatsing foutmelding, al is er geen foutmelding geplaatsd
    # dan wordt de exception gevangen door de except statement
    try:
        errorLabel.grid_forget()
    except:
        pass

    # Alle paginas van het scherm afhalen
    frame.pack_forget()
    pageComments.pack_forget()
    pageWeer.pack_forget()
    pageF.pack_forget()

    # Stationsnaam verversen in station label zijbalk
    stationDeclaratie.config(text="Station " + stationVanZuil)

    # Gewenste pagina wordt op scherm gezet, en screen2 ook
    page.pack(side='right',expand='true', fill='both')
    screen2.pack(expand='true',fill='both')

    # Definiëring counter en executie van cyclePages, waardoor de loop begint
    counter = 0
    cyclePages()

# Connectie tot database
connection = psycopg2.connect(dbname='berichtendatabase', user='postgres', password='postgresql')
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
curs = connection.cursor()

# Aanmaak tabel station_service, voor faciliteiten per station
try:
    curs.execute("""
CREATE TABLE station_service (
     station_city VARCHAR (50) PRIMARY KEY NOT NULL,
     country VARCHAR (2) NOT NULL,
     ov_bike BOOLEAN NOT NULL,
     elevator BOOLEAN NOT NULL,
     toilet BOOLEAN NOT NULL,
     park_and_ride BOOLEAN NOT NULL
);
INSERT INTO station_service (
    station_city, country, ov_bike, elevator, toilet, park_and_ride)
VALUES
    ('Arnhem', 'NL', true, false, true, false),
    ('Almere', 'NL', false, true, false, true),
    ('Amersfoort', 'NL', true, false, true, false),
    ('Almelo', 'NL', false, true, false, true),
    ('Alkmaar', 'NL', true, false, true, false),
    ('Apeldoorn', 'NL', false, true, false, true),
    ('Assen', 'NL', true, false, true, false),
    ('Amsterdam', 'NL', false, true, false, true),
    ('Boxtel', 'NL', true, false, true, false),
    ('Breda', 'NL', false, true, false, true),
    ('Dordrecht', 'NL', true, false, true, false),
    ('Delft', 'NL', false, true, false, true),
    ('Deventer', 'NL', true, false, true, false),
    ('Enschede', 'NL', false, true, false, true),
    ('Gouda', 'NL', true, false, true, false),
    ('Groningen', 'NL', false, true, false, true),
    ('Den Haag', 'NL', true, false, true, false),
    ('Hengelo', 'NL', false, true, false, true),
    ('Haarlem', 'NL', true, false, true, false),
    ('Helmond', 'NL', false, true, false, true),
    ('Hoorn', 'NL', true, false, true, false),
    ('Heerlen', 'NL', false, true, false, true),
    ('Den Bosch', 'NL', true, false, true, false),
    ('Hilversum', 'NL', false, true, false, true),
    ('Leiden', 'NL', true, false, true, false),
    ('Lelystad', 'NL', false, true, false, true),
    ('Leeuwarden', 'NL', true, false, true, false),
    ('Maastricht', 'NL', false, true, false, true),
    ('Nijmegen', 'NL', true, false, true, false),
    ('Oss', 'NL', false, true, false, true),
    ('Roermond', 'NL', true, false, true, false),
    ('Roosendaal', 'NL', false, true, false, true),
    ('Sittard', 'NL', true, false, true, false),
    ('Tilburg', 'NL', false, true, false, true),
    ('Utrecht', 'NL', true, false, true, false),
    ('Venlo', 'NL', false, true, false, true),
    ('Vlissingen', 'NL', true, false, true, false),
    ('Zaandam', 'NL', false, true, false, true),
    ('Zwolle', 'NL', true, false, true, false),
    ('Zutphen', 'NL', false, true, false, true);
ALTER TABLE Bericht ADD FOREIGN KEY (station) REFERENCES station_service(station_city);
""")
except psycopg2.errors.DuplicateTable:
    pass

# Dictionary met alle stations met de postcodes, voor de API call
stationPostCode = {
    "Arnhem":6811,
    "Almere":1315,
    "Amersfoort":3818,
    "Almelo":7604,
    "Alkmaar":1815,
    "Apeldoorn":7311,
    "Assen":9401,
    "Amsterdam":1012,
    "Boxtel":5281,
    "Breda":4811,
    "Dordrecht":3311,
    "Delft":2611,
    "Deventer":7411,
    "Enschede":7514,
    "Gouda":2801,
    "Groningen":9726,
    "Den Haag":2595,
    "Hengelo":7551,
    "Haarlem":2011,
    "Helmond":5705,
    "Hoorn":1621,
    "Heerlen":6411,
    "Den Bosch":5211,
    "Hilversum":1211,
    "Leiden":2312,
    "Lelystad":8232,
    "Leeuwareden":8911,
    "Maastricht":6221,
    "Nijmegen":6512,
    "Oss":5348,
    "Roermond":6041,
    "Roosendaal":4702,
    "Sittard":6131,
    "Tilburg":5038,
    "Utrecht":3511,
    "Venlo":5913,
    "Vlissingen":4382,
    "Zaandam":1506,
    "Zwolle":8017,
    "Zutphen":7201,
    "":6131

}

# Dictionary voor beschrijvingen om gebruikt te worden in de weerpagina
beschrijvingDict = {
"Thunderstorm":"Er is een onweersbui gaande.",
"Drizzle":"Het is aan het motregenen",
"Rain":"Het is aan het regenen",
"Snow":"Het is aan het sneeuwen",
"Clouds":"Het is bewolkt",
"Clear":"Er is geen bewolking"
}

# Root aanwijzing en fullscreen maken hier van
gui = Tk()
gui.attributes("-fullscreen",True)

# Frames aanmaak
screen1 = Frame(gui)
screen2 = Frame(gui)
sideBar = LabelFrame(screen2,bg='#FFC917',padx=5,pady=5)
buttons = LabelFrame(sideBar)

# Startscherm voor input station
stationVanZuil = ''
inputFrame = Frame(screen1, pady=310, bg="#FFC917")
label = Label(inputFrame, text="Hallo, welkom bij het stationszuil, op welk station zit u?", fg='#003082', bg='#FFC917', font=("Open_Sans", 40), padx=150)
keuzeMenu = Listbox(inputFrame)
submitButton = Button(inputFrame, text="Indienen", command=stationsKeuze)
keuzeMenu.insert(1,"Arnhem")
keuzeMenu.insert(2,"Almere")
keuzeMenu.insert(3,"Amersfoort")
keuzeMenu.insert(4,"Almelo")
keuzeMenu.insert(5,"Alkmaar")
keuzeMenu.insert(6,"Apeldoorn")
keuzeMenu.insert(7,"Assen")
keuzeMenu.insert(8,"Amsterdam")
keuzeMenu.insert(9,"Boxtel")
keuzeMenu.insert(10,"Breda")
keuzeMenu.insert(11,"Dordrecht")
keuzeMenu.insert(12,"Delft")
keuzeMenu.insert(13,"Deventer")
keuzeMenu.insert(14,"Enschede")
keuzeMenu.insert(15,"Gouda")
keuzeMenu.insert(16,"Groningen")
keuzeMenu.insert(17,"Den Haag")
keuzeMenu.insert(18,"Hengelo")
keuzeMenu.insert(19,"Haarlem")
keuzeMenu.insert(20,"Helmond")
keuzeMenu.insert(21,"Hoorn")
keuzeMenu.insert(22,"Heerlen")
keuzeMenu.insert(23,"Den Bosch")
keuzeMenu.insert(24,"Hilversum")
keuzeMenu.insert(25,"Leiden")
keuzeMenu.insert(26,"Lelystad")
keuzeMenu.insert(27,"Leeuwareden")
keuzeMenu.insert(28,"Maastricht")
keuzeMenu.insert(29,"Nijmegen")
keuzeMenu.insert(30,"Oss")
keuzeMenu.insert(31,"Roermond")
keuzeMenu.insert(32,"Roosendaal")
keuzeMenu.insert(33,"Sittard")
keuzeMenu.insert(34,"Tilburg")
keuzeMenu.insert(35,"Utrecht")
keuzeMenu.insert(36,"Venlo")
keuzeMenu.insert(37,"Vlissingen")
keuzeMenu.insert(38,"Zaandam")
keuzeMenu.insert(39,"Zutphen")
keuzeMenu.insert(40,"Zwolle")

# Plaatsing startscherm
inputFrame.grid(column=0, row=0)
label.grid(column=0,row=0)
keuzeMenu.grid(column=0,row=1)
submitButton.grid(column=0,row=2)

# Aanmaak commentpagina, comments en plaatsing comments
pageComments = Frame(screen2)
topBar = Frame(pageComments)
topBar_label = Label(topBar, text="Comments",font=("Open_Sans", 30), fg='#003082')
topBar_label.grid(column=0,row=1,pady=50)
topBar.pack(side='top')
rest = LabelFrame(pageComments)
rest.pack(side='right', expand='true', fill='both')
pageComments.pack(side='right',expand='true', fill='both')
comment1 = Label(rest, width = 100, height = 5, font=("Open_Sans", 15, 'bold'),wraplength=800, anchor='center', fg='black')
comment2 = Label(rest, width = 100, height = 5, font=("Open_Sans", 15, 'bold'),wraplength=800, anchor='center', fg='black')
comment3 = Label(rest, width = 100, height = 5, font=("Open_Sans", 15, 'bold'),wraplength=800, anchor='center', fg='black')
comment4 = Label(rest, width = 100, height = 5, font=("Open_Sans", 15, 'bold'),wraplength=800, anchor='center', fg='black')
comment5 = Label(rest, width = 100, height = 5, font=("Open_Sans", 15, 'bold'),wraplength=800, anchor='center', fg='black')

comment1.grid(column = 0, row = 0)
comment2.grid(column = 0, row = 1)
comment3.grid(column = 0, row = 2)
comment4.grid(column = 0, row = 3)
comment5.grid(column = 0, row = 4)

# Aanmaak weerpagina, weerdata en plaatsing weerdata
pageWeer = Frame(screen2)
topBar = Frame(pageWeer)
rest = Frame(pageWeer)
topBar_label = Label(topBar, text="Weer",font=("Open_Sans", 30), fg='#003082')
weerFrame = LabelFrame(rest)
topBar_label.grid(column=0,row=1, pady=50)
weerFrame.grid(column=0,row=0, padx=450, pady=250)

weerLabel2 = Label(weerFrame, font=("Open_Sans", 20), fg='#003082')
weerLabel3 = Label(weerFrame, font=("Open_Sans", 15), fg='#003082')
weerLabel4 = Label(weerFrame, font=("Open_Sans", 15), fg='#003082')
weerLabel5 = Label(weerFrame, font=("Open_Sans", 15), fg='#003082')
weerLabel2.grid(column=0,row=0)
weerLabel3.grid(column=0,row=3)
weerLabel4.grid(column=0,row=4)
weerLabel5.grid(column=0, row=5)
weerIcoon = Label(weerFrame, bg="#FFC917")
weerIcoon.grid(column=0,row=2)
rest.pack(side='bottom',expand='true', fill='both')
topBar.pack(side='top')

# Aanmaak faciliteitenpagina , faciliteitplaatjes en plaatsing plaatjes
pageF = Frame(screen2)
topBar = Frame(pageF)
rest = Frame(pageF)
facilFrame = LabelFrame(rest)

fietsI = Label(facilFrame)
liftI = Label(facilFrame)
toiletI = Label(facilFrame)
pRI = Label(facilFrame)
fietsI.grid(column=0, row=0)
liftI.grid(column=0, row=1)
toiletI.grid(column=1, row=0)
pRI.grid(column=1, row=1)
topBar_label = Label(topBar, text="Faciliteiten",font=("Open_Sans", 30), fg='#003082')
topBar_label.grid(column=0,row=1, pady=50)
topBar.pack(side='top')
facilFrame.grid(column=0,row=0, padx=425, pady=150)
rest.pack(expand='true', fill='both')

# Aanmaak en plaatsing widgets zijbalk
nsLogoImage = PhotoImage(file="images/NSLogo.png")
nsLogo = Label(sideBar, image=nsLogoImage, bg='#FFC917')
stationDeclaratie = Label(sideBar, text="Station " + stationVanZuil, font=("Open_Sans", 20, 'bold'), bg='#FFC917', fg='#003082')
tijdDeclaratie = Label(sideBar, font=("Open_Sans", 20, 'bold'), bg='#FFC917', fg='#003082')
nsLogo.grid(column=0,row=0,pady=30)
stationDeclaratie.grid(column=0,row=1)
tijdDeclaratie.grid(column=0,row=2)

# Aanmaak en plaatsing buttons zijbalk, niet functioneel, maar voor show
button1 = Button(buttons, text="Comments",bg='#0063D3', fg='white',  width=30, height=4, font=("Open_Sans", 15, 'bold'))
button2 = Button(buttons, text="Weer",bg='#003082', fg='white', width=30, height=4, font=("Open_Sans", 15, 'bold'))
button3 = Button(buttons, text="Faciliteiten",bg='#003082', fg='white', width=30, height=4, font=("Open_Sans", 15, 'bold'))

button1.grid(column=0,row=1)
button2.grid(column=0,row=3)
button3.grid(column=0,row=4)
buttons.grid(column=0,row=3,pady=150)

# Plaatsing sidebar en screen1
sideBar.pack(side="left")
screen1.pack(expand='true', fill='both')

# Mainloop
gui.mainloop()
