import sqlite3
from sqlite3 import Error


def CreateCon(dbFile):
	con=None
	try:
		con = sqlite3.connect(dbFile)
		print("Database creado")
	except Error as e:
		print(e)
	finally:
		if con:
			con.close()
            
def PrepareCon(con,cur,values=(), where=[], tableName = "MainPrinter", option="create", closeDB = False):

	if option == "create":
		print("Creando tabla...")
		cur.execute(f'''CREATE TABLE IF NOT EXISTS "{tableName}" 
			("ID" INTEGER PRIMARY KEY AUTOINCREMENT, 
			"PrinterName" TEXT, 
			"KWprize" INTEGER,
			"KWprinter" INTEGER, 
			"PrinterCost" INTEGER, 
			"AmortPrinter" INTEGER, 
			"SpoolCost" INTEGER, 			
			"SpoolWeight" INTEGER);''')
		con.commit()
		print("OK")
		
	if option == "insert":
		print("Insertando datos...")
		cur.execute(f'''INSERT INTO "{tableName}" 
			(PrinterName,KWprize,KWprinter,PrinterCost,AmortPrinter,SpoolCost,SpoolWeight)
		VALUES (?,?,?,?,?,?,?);''', values)
		con.commit()
		print("OK")
	
	if option == "update":
		print("Actualizando datos...")
		cur.execute(f'''UPDATE {tableName} SET 
				KWprize = ?,
                  		KWprinter = ?,
                  		PrinterCost = ?,
                  		AmortPrinter = ?,
                  		SpoolCost = ?,
                  		SpoolWeight = ?
              			WHERE {where[0]} = "{where[1]}"''', values)
		con.commit()
		print("OK")
		
	if option == "add":
		print("Añadiendo nueva fila...")
		cur.execute(f'''INSERT INTO "{tableName}" 
			(PrinterName,KWprize,KWprinter,PrinterCost,AmortPrinter,SpoolCost,SpoolWeight)
			VALUES(?,?,?,?,?,?,?);''', values)
		con.commit()
		print("OK")
		
	if option =="delete":
		print("Borrando fila...")
		cur.execute(f'''DELETE FROM {tableName} WHERE {where[0]} = "{where[1]}"''')
		con.commit
		print("OK")
	
	if closeDB == True:
		con.close()

def SqlConnection(routeDB):
    try:
        con = sqlite3.connect(routeDB)
        cur = con.cursor()
        cur.execute("SELECT * from MainPrinter WHERE ID=1")
        print("Conexión establecida")
        return con, cur

    except:
        print("Conexión NO establecida\nRealizando reparaciones")
        PrepareCon(con, cur)
        if cur.execute("SELECT * from MainPrinter"):
        	print("Reparación completada\nConexión establecida")
        	return con, cur
        else:
        	print("Reparación fallida")
        	return False
    

def GetThings(cur, where=[], selection="PrinterName"):
	if where == []:
        	cur.execute(f"SELECT {selection} FROM MainPrinter")
	else:
        	cur.execute(f"SELECT {selection} FROM MainPrinter WHERE {where[0]} = '{where[1]}'")
        
	thingExtract = cur.fetchall()
	return thingExtract
        
    



