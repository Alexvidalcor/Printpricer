import sqlite3
from sqlite3 import Error


def SqlConnection():

    con = sqlite3.connect('../database/mydatabase.db')
    print("Conexión establecida")
    return con


def CreateDatabase(con):

    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE CostEstimation(id integer PRIMARY KEY ASC AUTOINCREMENT, Kw integer, Tiempo integer, CosteBobina integer, Gramos integer, Opcional integer)")
    cursorObj.execute("CREATE TABLE SalesEstimation(id integer PRIMARY KEY ASC AUTOINCREMENT, Margen integer, IVA integer)")
con.commit()
    
    
con = SqlConnection()
CreateDatabase(con)


