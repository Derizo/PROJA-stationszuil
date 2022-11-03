import psycopg2
from tkinter import *
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

connection = psycopg2.connect(dbname='berichtendatabase', user='postgres', password='postgresql')
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
curs = connection.cursor()

curs.execute("""
SELECT naam,bericht,datum,tijd FROM Bericht
ORDER BY datum DESC, tijd DESC
LIMIT 5;""")
laatste5Comments = curs.fetchall()


gui = Tk()
deNS = Label(gui,text='Dit is de NS, denk ik?', background='blue', relief= 'groove', font=("Comic Sans", 20))
deNS.grid(column = 0 , row = 0)

counter = 0
for i in laatste5Comments:
    counter += 10
    i = list(i)
    naam = i[0]
    bericht = i[1]
    datum = i[2]
    tijd = i[3]

    text = naam + " heeft op " +  str(datum) + " " + str(tijd) + " dit achtergelaten: \n" + bericht
    comment = Label(gui, text=text, width = 140,height = 4, relief='groove', font=("Comic Sans", 12))
    comment.grid(column = 0, row = 10 + counter)

gui.mainloop()
