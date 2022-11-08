from tkinter import *
import datetime

def tijdUpdate():
    "Functie om de klok in de zijbalk te verversen, zodat deze synchroon blijft met de echte tijd"
    global tijdLabel

    tijdNu = datetime.datetime.today()
    tijd = tijdNu.strftime("%H:%M")
    tijdLabel.config(text= tijd)
    gui.after(5000,lambda:tijdUpdate())
def storeComment():
    """

    Functie om de inhoud van het naam en bericht veld op te halen.
    Hierbij wordt de inhoud van de velden in variabelen opgeslagen,
    en al zijn deze te lang, of niet ingevuld, dan zal er een foutmelding verschijnen.

    Al is er geen fout in de invoer, dan wordt er een willekeurig station
    uitgekozen en in een variable opgeslagen, de huidige datum en tijd in een variable opgeslagen.

    Hierna wordt er met de module csv deze variabelen in een csv bestand opgeslagen.

    """
    import random
    import csv

    global naamEntry
    global commentEntry
    global errorLabel

# Terugzetting van plaatsing foutmelding, al is er geen foutmelding geplaatsd, wordt de exception gevangen door de except statement
    try:
        errorLabel.grid_forget()
    except:
        pass
# Ophalen inputvelden en in variabelen stoppen
    naam = naamEntry.get()
    bericht = commentEntry.get()
# Checks condities voor foute invoer, al is er foute invoer dan worden er foutmeldingen gemaakt en geplaatst
    if len(naam) > 30:
        errorLabel = Label(inputFrame, text="De naam mag niet meer dan 30 karakters zijn. Probeer het nog een keer!")
        errorLabel.grid(column=0,row=2)
        return
    elif bericht == '':
        errorLabel = Label(inputFrame, text="Het naamveld mag leeg zijn, maar het commentveld niet. Probeer het nog een keer!")
        errorLabel.grid(column=0,row=2)
        return
    elif len(bericht) > 140:
        errorLabel = Label(inputFrame, text="Het bericht moet onder 140 de karakters blijven. Probeer het nog een keer!")
        errorLabel.grid(column=0,row=2)
        return
    #Sanitisatie apostrofen van naam en bericht en al is er niks ingevoerd dan zal naam als value 'anoniem' krijgen
    naam = naam.replace("'",'"')
    if naam == '':
        naam = 'anoniem'
    bericht = bericht.replace("'",'"')

    f = open("berichtDataBase.csv", "a", newline='')
    writer = csv.writer(f, delimiter=",")

    stations = {
        1:"Arnhem",
        2:"Almere",
        3:"Amersfoort",
        4:"Almelo",
        5:"Alkmaar",
        6:"Apeldoorn",
        7:"Assen",
        8:"Amsterdam",
        9:"Boxtel",
        10:"Breda",
        11:"Dordrecht",
        12:"Delft",
        13:"Deventer",
        14:"Enschede",
        15:"Gouda",
        16:"Groningen",
        17:"Den Haag",
        18:"Hengelo",
        19:"Haarlem",
        20:"Helmond",
        21:"Hoorn",
        22:"Heerlen",
        23:"Den Bosch",
        24:"Hilversum",
        25:"Leiden",
        26:"Lelystad",
        27:"Leeuwareden",
        28:"Maastricht",
        29:"Nijmegen",
        30:"Oss",
        31:"Roermond",
        32:"Roosendaal",
        33:"Sittard",
        34:"Tilburg",
        35:"Utrecht",
        36:"Venlo",
        37:"Vlissingen",
        38:"Zaandam",
        39:"Zwolle",
        40:"Zutphen"
    }

    stationsNaam = stations[random.randint(1,40)]
    tijdNu = datetime.datetime.today()
    datum = tijdNu.strftime("%Y-%m-%d")
    tijd = tijdNu.strftime("%T")
    berichtAppend = [naam, bericht, datum, tijd, stationsNaam]
    writer.writerow(berichtAppend)
    try:
        errorLabel.grid_forget()
    except:
        pass
    naamEntry.delete(0,END)
    commentEntry.delete(0,END)
    errorLabel = Label(inputFrame, text="Bedankt voor jouw input!")
    errorLabel.grid(column=0,row=2, sticky="NW")

# Aanmaking van root en het root window op fullscreen zetten
gui = Tk()
gui.attributes('-fullscreen', True)

# Aanmaak van zijbalk en plaatsing op scherm
sideBar = LabelFrame(gui,bg='#FFC917',padx=5,pady=5)
nsLogoImage = PhotoImage(file="images/NSLogo.png")
nsLogo = Label(sideBar, image=nsLogoImage, bg='#FFC917').grid(column=0,row=0,pady=30)
sideBar.pack(side='left',expand='true',fill='both')
tijdNu = datetime.datetime.today()
tijd = tijdNu.strftime("%H:%M")
tijdLabel = Label(sideBar, text=tijd,font=("Open_Sans", 20, 'bold'), bg= "#FFC917", fg='#003082')
tijdLabel.grid(column=0,row=1)
pageCA = Frame(gui)
rest = LabelFrame(pageCA)
rest.pack(side='bottom',expand='true',fill='both')
topBar = Frame(pageCA)
topBar_label = Label(topBar, text="Comment achterlaten",font=("Open_Sans", 25), fg='#003082')
topBar_label.grid(column=0,row=1, pady=50)
topBar.pack(side='top')
pageCA.pack(side='right',expand='true',fill='y')

# Aanmaak van inputvelden en plaatsing op scherm
inputFrame = LabelFrame(rest)
naamLabel = Label(inputFrame, text= "Wat is uw naam?", font=("Open_Sans", 15))
naamEntry = Entry(inputFrame)
commentLabel = Label(inputFrame, text='Wat is de comment die u wilt acherlaten?',font=("Open_Sans", 15))
commentEntry = Entry(inputFrame)
submitButton = Button(inputFrame, text='Verzend', command=storeComment)
naamLabel.grid(column=0,row=0, sticky='NW')
naamEntry.grid(column=1,row=0)
commentLabel.grid(column=0,row=1, sticky='NW')
commentEntry.grid(column=1,row=1)
submitButton.grid(column=1,row=2, sticky='NE')
inputFrame.grid(column=0, row=0, padx=420, pady=300)

# Executie van tijdUpdate() en mainloop op root
gui.after(5000,lambda:tijdUpdate())
gui.mainloop()
