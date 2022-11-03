def sanitize(str):
    if '"' in str:
        tmpStr = ''
        for i in str:
            if i == '"':
                i = "'"
            tmpStr += i
        str = tmpStr
    return str
def berichtAchterlaten():
    import random
    import datetime
    import csv
    f = open("berichtDataBase.csv", "a", newline='')
    writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
    naam = input("Wat is jouw naam? ")
    while len(naam) > 30:
        naam = input("Sorry, een naam mag maximaal 30 tekens zijn, probeer het nog een keer!")
    naam = sanitize(naam)
    if naam == '':
        naam = 'anoniem'
    bericht = input("Wat is het bericht dat jij wilt achterlaten? ")
    while len(bericht) > 140:
        bericht = input("Sorry, het bericht mag maximaal 140 tekens zijn, probeer het nog een keer! ")
    bericht = sanitize(bericht)
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

berichtAchterlaten()

