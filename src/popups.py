import PySimpleGUI as sg

from src.db import CreateCon, SqlConnection, GetThings, PrepareCon
from src.handler import MainValidation


menu_def = [['Archivo', ['Salir']],['Editar', ['Añadir', 'Eliminar', 'Refrescar']]]
commonParams = [("Helvetica", 10), (18, 1), "#ffff80", (2,1), ("Helvetica", 15),(15,1)]
	
def PopupDelete():
	layout = [
		[sg.Text("Selecciona la impresora a eliminar:")],
		[sg.Combo(values=[element[0] for element in GetThings(cur)], key="-CHOSPRINTDEL-",  
				size = commonParams[1], change_submits=True)],
		[sg.Button("Aceptar", key="-ACEPTARDELETE-", font=commonParams[4], auto_size_button=True)]
	]
	
	window = sg.Window('Estimador', layout)

	while True:
		event, values = window.read()
		if event == "-ACEPTARDELETE-":
			print([element[0] for element in GetThings(cur)])
			PrepareCon(con,cur,where=["PrinterName",values['-CHOSPRINTDEL-']], option="delete")
			break
		if event == sg.WIN_CLOSED or event == "Salir":
			break
	window.close()


def PopupOptions(con, cur):

	layout = [
		[sg.Menu(menu_def, tearoff=True)],
		[sg.Column([[sg.Text("Introduce los datos de tu impresora 3D", justification="center", font= ("Helvetica", 12))]],
			justification = "center")],
		[sg.Text("Elige tu impresora", size = commonParams[1], font = commonParams[0]),
			sg.Combo(values=[element[0] for element in GetThings(cur)], key="-CHOSPRINTERPOP-",  
				size = commonParams[1], change_submits=True)],
		[sg.Text("", size = commonParams[1], font= commonParams[0])],
		[sg.Text('· Precio KW hora', size = commonParams[1], font = commonParams[0]),
			 sg.Text('(Euros)',  size = commonParams[5],font=commonParams[0]),
			 sg.Input(key="-KWPRIZE-", enable_events =True, size = commonParams[1], font = commonParams[0]),
			 sg.Text("", size = commonParams[3], font= commonParams[0])],
		[sg.Text("", size = commonParams[1], font= commonParams[0])],
		[sg.HorizontalSeparator()],
		[sg.Text("", size = commonParams[1], font= commonParams[0])],
		[sg.Text('· KW Impresora',  size = commonParams[1],font = commonParams[0]),
			 sg.Text('(KWatios)',  size = commonParams[5],font=commonParams[0]),
			 sg.Input(key="-KWPRINTER-",enable_events =True,  size = commonParams[1],font = commonParams[0]),
			 sg.Text("", size = commonParams[3], font= commonParams[0])],
		[sg.Text('· Precio Impresora',  size = commonParams[1],font = commonParams[0]),
			 sg.Text('(Euros)',  size = commonParams[5],font=commonParams[0]),
			 sg.Input(key="-COSTPRINTER-",enable_events =True,  size = commonParams[1],font = commonParams[0]),
			 sg.Text("", size = commonParams[3], font= commonParams[0])],
		[sg.Text('· Amort. Impresora',  size = commonParams[1],font = commonParams[0]),
			 sg.Text('(Años)',  size = commonParams[5],font=commonParams[0]),
			 sg.Input(key="-AMORTPRINTER-", enable_events =True, size = commonParams[1],font = commonParams[0]),
			 sg.Text("", size = commonParams[3], font= commonParams[0])],
		[sg.Text("", size = commonParams[1], font= commonParams[0])],
		[sg.HorizontalSeparator()],
		[sg.Text("", size = commonParams[1], font= commonParams[0])],
		[sg.Text('· Coste de bobina', size = commonParams[1], font=commonParams[0]),
			sg.Text('(Euros)',  size = commonParams[5],font=commonParams[0]),
	 		sg.Input(key='-SPOOLCOST-',size=commonParams[1], font=commonParams[0], enable_events=True),
	 		sg.Text("", size = commonParams[3], font= commonParams[0])],
		[sg.Text('· Bobina completa',  size = commonParams[1],font=commonParams[0]),
			sg.Text('(Gramos)',  size = commonParams[5],font=commonParams[0]),
			sg.Input(key='-SPOOLWEIGHT-',  size = commonParams[1],font=commonParams[0], enable_events=True),
			sg.Text("", size = commonParams[3], font= commonParams[0])],
		[sg.Text("", size = commonParams[1], font= commonParams[0])],
		[sg.HorizontalSeparator()],
		[sg.Text("", size = commonParams[1], font= commonParams[0])],
		[sg.Column([[sg.Button("Actualizar", key="-ACTUALIZAR-", font=commonParams[4], auto_size_button=True)]],
			justification="center")]
		]
	    
	    
	window = sg.Window('Estimador', layout)
	
	while True:
		event, values = window.read()
		
		if event == "-ACTUALIZAR-":
			valKWprize = MainValidation(values["-KWPRIZE-"])
			valKWprinter = MainValidation(values["-KWPRINTER-"])
			valCostprinter = MainValidation(values["-COSTPRINTER-"])
			valAmortprinter = MainValidation(values["-AMORTPRINTER-"])
			valSpoolcost = MainValidation(values["-SPOOLCOST-"])
			valSpoolweight = MainValidation(values["-SPOOLWEIGHT-"])
			PrepareCon(con, cur, option="update", 
				where = ["PrinterName", values["-CHOSPRINTERPOP-"]],
				values=(valKWprize,valKWprinter,valCostprinter,valAmortprinter,valSpoolcost,valSpoolweight))
			window.Element("-KWPRIZE-").update(valKWprize)
			window.Element("-KWPRINTER-").update(valKWprinter)
			window.Element("-COSTPRINTER-").update(valCostprinter)
			window.Element("-AMORTPRINTER-").update(valAmortprinter)
			window.Element("-SPOOLCOST-").update(valSpoolcost)
			window.Element("-SPOOLWEIGHT-").update(valSpoolweight)
			
		if event == "Refrescar":
			window.Element("-CHOSPRINTERPOP-").update(values=[element[0] for element in GetThings(cur)])
		if event == "-CHOSPRINTERPOP-":
			updaterValues = GetThings(cur, selection="*",where=["PrinterName", values["-CHOSPRINTERPOP-"]])[0]
			window.Element("-KWPRIZE-").update(updaterValues[2])
			window.Element("-KWPRINTER-").update(updaterValues[3])
			window.Element("-COSTPRINTER-").update(updaterValues[4])
			window.Element("-AMORTPRINTER-").update(updaterValues[5])
			window.Element("-SPOOLCOST-").update(updaterValues[6])
			window.Element("-SPOOLWEIGHT-").update(updaterValues[7])
			
		if event == "Añadir":
			newPrinter = sg.popup_get_text("Introduce el nombre de tu impresora")
			PrepareCon(con, cur, values=(newPrinter,0,0,0,0,0,0), option="add")
			window.Element("-CHOSPRINTERPOP-").update(values=[element[0] for element in GetThings(cur)])
		elif event == "Eliminar":
			PopupDelete(con, cur)
			window.Element("-CHOSPRINTERPOP-").update(values=[element[0] for element in GetThings(cur)])
			

		if event == sg.WIN_CLOSED or event =="Salir":
			break
	
	window.close()
	
