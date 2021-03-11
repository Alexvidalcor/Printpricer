import PySimpleGUI as sg
from src.calc import FilamentCost, KwCost

sg.SetOptions(element_padding=((0,0),(20,20)))

def MainGui():

	commonParams = [(26,1), (10,1)]

	layout = [
	    [sg.Text('Introduce los siguientes datos para recibir la estimación:', size=(50,2))],
	    [sg.Text('Precio Kw/hora', size=commonParams[0]), sg.Input(key='-INaccess1-', size=commonParams[1])],
	    [sg.Text('Horas de impresión', size=commonParams[0]), sg.Input(key='-INaccess2-', size=commonParams[1])],
	    [sg.Text('Coste de bobina', size=commonParams[0]), sg.Input(key='-INaccess3-', size=commonParams[1])],
	    [sg.Text('Gramos de bobina completa', size=commonParams[0]), sg.Input(key='-INaccess4-', size=commonParams[1])],
	    [sg.Text('Gramos de material consumido', size=commonParams[0]), sg.Input(key='-INaccess5-', size=commonParams[1])],
	    [sg.Text('Coste de diseño (Opcional)', size=commonParams[0]), sg.Input(key='-INaccess6-', size=commonParams[1])],
	    [sg.Button(key="-INsubmit-", pad=((40,10),(1,1)), size=(30,1)), sg.Cancel()]
	]

	window = sg.Window('Estimador de costes', layout)

	while True:
		event, values = window.read()
		if event == "INsubmit":
			electricityCost("-INaccess1-", "-INaccess2-")
			filamentCost("-INaccess3-", "-INaccess4-", "-INaccess5-")
			sg.Popup(f"El coste total es {electricityCost+filamentCost}")
		if event == sg.WIN_CLOSED or event == 'Quit':
    			break
			
	window.close()
