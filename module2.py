def moderatie():
    try:
        import csv
        import datetime
        from sys import exit
        from time import sleep
        from email_validator import validate_email, EmailNotValidError
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    except ModuleNotFoundError:
        print("""Er zijn modules niet geinstalleerd op deze computer!
Hoogstwaarschijnlijk is dit 'email_validator' of 'psycopg2', deze kan je installeren doormiddel van het command-line commando
'pip install $MODULE'. Neem eventueel contact op met de IT-afdeling!\n""")
        exit()

    connection = psycopg2.connect(user='postgres', password='postgresql')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    curs = connection.cursor()

    try:
        curs.execute("CREATE DATABASE berichtendatabase")
        connection.close()
    except psycopg2.errors.DuplicateDatabase:
        pass
    connection = psycopg2.connect(dbname='berichtendatabase', user='postgres', password='postgresql')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    curs = connection.cursor()

    try:
        curs.execute("""CREATE TABLE Moderator
        (
        	email_adres VARCHAR(345) PRIMARY KEY,
        	voornaam VARCHAR(50) NOT NULL,
        	tussenvoegsel VARCHAR(50),
        	achternaam VARCHAR(51) NOT NULL
        );

        CREATE TABLE Bericht
(
	berichtnr SERIAL PRIMARY KEY ,
	naam VARCHAR(30) NOT NULL,
	bericht VARCHAR(140) NOT NULL,
	datum DATE NOT NULL,
	tijd TIME NOT NULL,
	station VARCHAR(33) NOT NULL,
	status VARCHAR(11) NOT NULL,
	datum_beoordeling DATE NOT NULL,
	tijd_beoordeling TIME NOT NULL,
    moderator_email VARCHAR(345) NOT NULL,
    FOREIGN KEY(moderator_email) REFERENCES Moderator(email_adres)
);

""")
    except psycopg2.errors.DuplicateTable:
        pass

    while True:
        try:
            email = str(input("Voer jouw email adres in: "))
            validate_email(email, check_deliverability=False)
            break
        except EmailNotValidError:
            print("Dit is geen email adres, probeer het nog een keer.")
    print("Welkom bij het moderatiecentrum, " + email + "!")

    curs.execute("SELECT * FROM Moderator WHERE email_adres = %s",[email,])
    if len(curs.fetchall()) == 0:
        print("Er is geen moderator met het email-adres: '" + email + "' gevonden.")
        sleep(0.8)
        print("Voor administratie doeleinden vragen we nu jouw volledige naam voor opslag in onze database.")
        voornaam = str(input("Voornaam: "))
        tussenvoegsel = str(input("Tussenvoegsel: "))
        achternaam = str(input("Achternaam: "))
        curs.execute("""INSERT INTO Moderator(email_adres,voornaam,tussenvoegsel,achternaam)
            VALUES(%s,%s,%s,%s)""",[email, voornaam, tussenvoegsel, achternaam])

    counter = 0
    while True:
        f = open("berichtDataBase.csv", "r")
        comment = f.readline().replace('\n','')
        if comment == '':
            print("Er zijn geen comments voor jou om te keuren, moderator. Kom later terug!")
            sleep(2)
            break
        splitComment = comment.split(",")
        naam = splitComment[0]
        bericht = splitComment[1]
        datum = splitComment[2]
        tijd = splitComment[3]
        station = splitComment[4]
        sleep(2)

        print(naam + " heeft dit bericht achtergelaten: " + bericht)
        sleep(0.5)
        goedkeuring = input("Wordt dit bericht goedgekeurd of afgekeurd? (g/a/s) ")
        if goedkeuring == 'g':
            status = "Goedgekeurd"
        elif goedkeuring == 'a':
            status = "Afgekeurd"
        elif goedkeuring == 's':
            print("Jij hebt " + str(counter) + " berichten gekeurd. Bedankt voor jouw werk, moderator " + email + "!")
            break
        else:
            while goedkeuring != 'g' and goedkeuring != 'a' and goedkeuring != 's':
                goedkeuring = input("Foute invoer! Wordt dit bericht goedgekeurd of afgekeurd? (g/a/s) ")

        tijdNu = datetime.datetime.today()
        tijdModeratie = tijdNu.strftime("%T")
        datumModeratie = tijdNu.strftime("%Y-%m-%d")
        counter += 1

        curs.execute("""INSERT INTO Bericht(naam,bericht,datum,tijd,station,status,datum_beoordeling,tijd_beoordeling,moderator_email)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,[naam,bericht,datum,tijd,station,status,datumModeratie,tijdModeratie,email])

        restOfFile = f.readlines()
        f.close()
        f = open("berichtDataBase.csv", "w")
        writeString = ''.join(restOfFile)
        f.write(writeString)
        f.close()

        if writeString == '':
            print('Dat waren alle berichten, bedankt, moderator ' + email + '! Je hebt ' + str(counter) + ' comments gekeurd!')
            break

moderatie()
