import PySimpleGUI as sg
from os.path import exists

from src.calc import FilamentCost, KwCost, ManageSales, AmortCost
from src.handler import MainValidation, TimeValidation
from src.popups import PopupOptions
from src.db import CreateCon, SqlConnection, GetThings, PrepareCon

sg.SetOptions(element_padding=((40, 0), (10, 10)))


menu_def = [['Archivo', ['Salir']],['Ajustes', ['Opciones']],['Ayuda', ['Acerca de...']]]
commonParams = [(30, 1), (10, 1), ("Helvetica", 12), (20, 1), (38, 1)]
electricityCost = 0
materialCost = 0
ivaTax = 0
marginSales = 0

def RefactorSupport(cur, printer, selected):
    return MainValidation(GetThings(cur,selection=selected, where=["PrinterName", printer]])[0][0])

def Collapse(layout, key, visible):
    return sg.pin(sg.Column(layout, key=key, visible=visible))

def Reset(window, layout):
    for element in range(1, 9):
        window[f"-INaccess{element}{2 if layout == 2 else 1}-"].update("")
    if layout ==2:
        window[f"-Text1-"].update("El coste total es 0 €")
        window[f"-Text2-"].update("El precio de venta es 0 €")
        
def IntroDB():
	if exists("db/MainPrinter.db"):
		print("Database existe")
		con, cur = SqlConnection("db/MainPrinter.db")
		return con, cur
	else:
		print("Database no existe")
		CreateCon("db/MainPrinter.db")
		con, cur = SqlConnection("db/MainPrinter.db")
		PrepareCon(con, cur, option="insert",
			values=("ImpresoraTest",0,0,0,0,0,0))
		return con, cur

def MainGui():

    con, cur = IntroDB()
    
    layout1 = [[sg.Menu(menu_def, tearoff=True)],
    	[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=commonParams[2])],
        [sg.Text("· Elige tu impresora", size = commonParams[0]),
		sg.Combo(values=[element[0] for element in GetThings(cur)], key="-CHOSPRINTER1-",  
				size = commonParams[1], change_submits=True)],
        [sg.Text('· Tiempo de impresión (H:M)', size=commonParams[0]),
         sg.Input(key='-INaccess11-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Material Consumido', size=commonParams[0]),
         sg.Input(key='-INaccess21-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess31-', size=commonParams[1], enable_events=True)],
        [sg.Text("")],
        [sg.Checkbox('Activar Opciones de Venta', enable_events=True,
                     key='-CHbox1-', font=commonParams[2])],
        [Collapse(
            [[sg.Text("· Margen de Venta (%)", size=commonParams[3]), sg.Input(key='-INaccess41-', size=commonParams[1], 			enable_events=True)],
             [sg.Text("· Porcentaje de IVA (%)", size=commonParams[3]), sg.Input(key='-INaccess51-', disabled=True, 			size=commonParams[1], enable_events=True),
              sg.Help("Ayuda", tooltip="Margen de ventas debe ser 0 o superior", key="-Help1-", pad=((5, 0), (0, 0)), 			button_color=("blue"))]], '-Token1-', False)],
        [sg.HorizontalSeparator(pad=((0, 0), (0, 0)))],
        [sg.Text("")],
        [sg.Column([[sg.Button("Calcular", font=commonParams[2], key="-INsubmit1-", auto_size_button=True, pad=((0, 0),(0,0))), 		     sg.Button("Reiniciar", key="-Reset1-", font=commonParams[2], pad=((10, 80), (0, 0)))]],
                     justification ="center")],
    ]

    layout2 = [[sg.Menu(menu_def, tearoff=True)],
    	[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=(commonParams[2]))],
        [sg.Text("· Elige tu impresora", size = commonParams[0]),
		sg.Combo(values=[element[0] for element in GetThings(cur)], key="-CHOSPRINTER2-",  
				size = commonParams[1], change_submits=True)],
        [sg.Text('· Tiempo de impresión (H:M)', size=commonParams[0]),
         sg.Input(key='-INaccess12-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Material Consumido', size=commonParams[0]),
         sg.Input(key='-INaccess22-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess32-', size=commonParams[1], enable_events=True)],
        [sg.Text("")],
        [sg.Checkbox('Activar Opciones de Venta',
                     enable_events=True, key='-CHbox2-', font=commonParams[2])],
        [Collapse(
            [[sg.Text("· Margen de Venta (%)", size=commonParams[3]), sg.Input(key='-INaccess42-', size=commonParams[1], enable_events=True)],
             [sg.Text("· Porcentaje de IVA (%)", size=commonParams[3]), sg.Input(key='-INaccess52-', size=commonParams[1], enable_events=True),
              sg.Help("Ayuda", tooltip="Margen de ventas debe ser 0 o superior", key="-Help2-", pad=((5, 0), (0, 0)), button_color=("blue"))]], '-Token2-', False)],
        [sg.HorizontalSeparator(pad=((0, 40), (0, 0)))],
        [sg.Text("El coste total es 0 €", key="-Text1-", size=commonParams[4],
                 font=commonParams[2], justification="center")],
        [sg.Text(f"El precio de venta es 0 €", key="-Text2-",
                 size=commonParams[4], font=commonParams[2], justification="center")],
        [sg.Text("")],
        [sg.Column([[sg.Button("Calcular", font=commonParams[2], key="-INsubmit2-", auto_size_button=True, pad=((0, 0),(0,0))), 
                     sg.Button("Reiniciar", key="-Reset2-", font=commonParams[2], pad=((10, 80), (0, 0)))]],
                     justification ="center")],
    ]

    layoutMain = [[sg.Column(layout1, key='-COL1-'),
                   sg.Column(layout2, visible=False, key='-COL2-')]]

    window = sg.Window('Estimador de costes', layoutMain)

    layout = 1
    opened = False
    checkSaved = False
    while True:
        event, values = window.read()
        if event == f'-CHbox{layout}-':
            opened = not opened
            window[f'-CHbox{layout}-'].update(opened)
            window[f'-Token{layout}-'].update(visible=opened)

        if event == f"-Help{layout}-":
            sg.popup("Margen de ventas debe ser 0 o superior para poder introducir el porcentaje de IVA",
                     title="Ayuda IVA", grab_anywhere=False)

        if event == f"-Reset{layout}-":
            Reset(window, layout)

        if values[f"-INaccess4{layout}-"] == "":
            window[f"-INaccess5{layout}-"].update("", disabled=True)
        else:
            window[f"-INaccess5{layout}-"].update(disabled=False)

        if event == f"-INsubmit{layout}-":

	    #REFACTORIZAR INTRODUCCIONES A CALC
	    
            marginSales = ManageSales(MainValidation(values[f"-INaccess4{layout}-"]))
            ivaTax = ManageSales(MainValidation(values[f"-INaccess5{layout}-"]))

            electricityCost = KwCost(RefactorSupport(cur, values["-CHOSPRINTER-"],"KWprize"),
            				MainValidation(values[f"-INaccess1{layout}-"]))
            				
            materialCost = FilamentCost(RefactorSupport(cur,values["-CHOSPRINTER-"],"SpoolCost"), 
            				RefactorSupport(cur,values["-CHOSPRINTER-"],"SpoolWeight"),
            				MainValidation(values[f"-INaccess2{layout}-"]))
            				
            amortCost = AmortCost(RefactorSupport(cur,values["-CHOSPRINTER-"],"PrinterCost"), 
            				RefactorSupport(cur,values["-CHOSPRINTER-"],"AmortPrinter"))
            				
            designCost = MainValidation(values[f"-INaccess3{layout}-"])

            totalCost = f"El coste total es {round(electricityCost+materialCost+amortCost+designCost,2)} €"
            if marginSales != 0:
                salesCost = f"El precio de venta es {round((((electricityCost+materialCost+amortCost+designCost)* 					(marginSales))*(ivaTax)),2)} €"
            elif marginSales == 0:
                salesCost = f"El precio de venta (sólo IVA) es {round((electricityCost+materialCost+amortCost+designCost)*(ivaTax),2)} €"
            window["-Text1-"].update(totalCost)
            window["-Text2-"].update(salesCost)

            if checkSaved == False:
                window[f'-COL{layout}-'].update(visible=False)

                # layout = 1 if layout == 2 else 2
                layout = 2

                if opened != False:
                    window[f'-CHbox{layout}-'].update(value=True)
                    window[f'-Token{layout}-'].update(visible=opened)

                for element in range(1, 5):
                    window[f"-INaccess{element}{2 if layout == 2 else 1}-"].update(
                        values[f"-INaccess{element}{1 if layout == 2 else 2}-"])

                window[f'-COL{layout}-'].update(visible=True)
                checkSaved = True
                
        elif event == "Opciones":
        	PopupOptions(con, cur)
        
        if event == sg.WIN_CLOSED or event =="Salir":
            break

    window.close()



