import PySimpleGUI as sg
from os.path import exists

from src.calc import FilamentCost, KwCost, ManageSales, AmortCost
from src.handler import MainValidation, TimeValidation
from src.popups import PopupOptions
from src.db import CreateCon, SqlConnection, GetThings, PrepareCon

#sg.SetOptions(element_padding=((40, 0), (10, 10)))


menu_def = [['Archivo', ['Salir']],['Ajustes', ['Opciones']],['Ayuda', ['Acerca de...']]]
commonParams = [(20, 1), (10, 1), ("Helvetica", 12), (38, 1),(17,1),("Helvetica", 14)]
electricityCost = 0
materialCost = 0
ivaTax = 0
marginSales = 0

def RefactorSupport(cur, printer, selected):
    try:
        return MainValidation(GetThings(cur,selection=selected, where=["PrinterName", printer])[0][0])
    except IndexError:
        raise Exception("Selecciona perfil de impresora válido")
    

def Collapse(layout, key, visible):
    return sg.pin(sg.Column(layout, key=key, visible=visible))

def Reset(window, layout):
    window[f"-CHOSPRINTER{layout}-"].update("")
    window[f"-COLUMNINPUTS{layout}-"].update(visible=False)
    window[f"-CHECKPRINTER{layout}-"].update(visible=False)
    window["-OUTPUTPRINT-"].update(value="")
    for element in range(1, 6):
        window[f"-INaccess{element}{2 if layout == 2 else 1}-"].update("")
    if layout ==2:
        window[f"-Text1-"].update("0 €")
        window[f"-Text2-"].update("0 €")

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
			values=("ImpresoraTest",0.25,120,300,4,20,1000))
		return con, cur

def MainGui():

    con, cur = IntroDB()
    
    layout1 = [[sg.Menu(menu_def, tearoff=True)],

	[sg.Column([
		[sg.Frame("Perfil de impresora",layout=[
			[sg.Combo(values=[element[0] for element in GetThings(cur)], readonly=True, key="-CHOSPRINTER1-",size = (33,1), change_submits=True),sg.Button("Editar",key ="-EDITPRINTER1-")]])]],vertical_alignment='center', justification='center')],
	
	 [sg.Column([[Collapse([[sg.Text("Selecciona perfil de impresora válido", auto_size_text=True,text_color="red",justification="center")]],"-CHECKPRINTER1-", False)]], vertical_alignment="center",justification="center")],

        [sg.Column([[sg.Frame(title="",layout=[[sg.Text('· Tiempo de impresión', size=commonParams[0]),
        	sg.Text("(Horas:Minutos)", size=commonParams[0]),
         	sg.Input(key='-INaccess11-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Material Consumido', size=commonParams[0]),
        	sg.Text("(Gramos)", size=commonParams[0]),
         	sg.Input(key='-INaccess21-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de laminado', size=commonParams[0]),
        	sg.Text("(Euros)", size=commonParams[0]),
         	sg.Input(key='-INaccess31-', size=commonParams[1], enable_events=True)]])]], 				vertical_alignment='center', justification='center')],
         	
        [sg.Column([[Collapse([[sg.Text("Dato mal introducido",key="-CHECKINPUTS1-",size=commonParams[3],text_color="red",justification="center")]],"-COLUMNINPUTS1-", False)]], vertical_alignment="center",justification="center")],
        [sg.Checkbox('Activar Opciones de Venta', enable_events=True,
                     key='-CHbox1-', font=commonParams[2])],
        [sg.Column([[Collapse(
            [[sg.Text("· Margen de Venta (%)", size=commonParams[0]), sg.Input(key='-INaccess41-', size=commonParams[1], enable_events=True)],
             [sg.Text("· Porcentaje de IVA (%)", size=commonParams[0]), sg.Input(key='-INaccess51-', disabled=True, 			size=commonParams[1], enable_events=True),
              sg.Help("Ayuda", tooltip="Margen de ventas debe ser 0 o superior", key="-Help1-", pad=((5, 0), (0, 0)), 			button_color=("blue"))]], '-Token1-', False)]], vertical_alignment='center', justification='center')],
        
        [sg.HorizontalSeparator(pad=((0, 0), (0, 0)))],
        [sg.Text("")],
        [sg.Column([[sg.Button("Calcular", font=commonParams[2], key="-INsubmit1-", auto_size_button=True, pad=((0, 0),(0,0))), 		     sg.Button("Reiniciar", key="-Reset1-", font=commonParams[2], pad=((20, 0), (0, 0)))]],
                     justification ="center")],
        
    ]

    layout2 = [[sg.Menu(menu_def, tearoff=True)],
	
	[sg.Column([
		[sg.Frame("Perfil de impresora",layout=[
			[sg.Combo(values=[element[0] for element in GetThings(cur)], readonly=True, key="-CHOSPRINTER2-",size = (33,1), change_submits=True),sg.Button("Editar",key ="-EDITPRINTER2-")]])]],vertical_alignment='center', justification='center')],
				
	[sg.Column([[Collapse([[sg.Text("Selecciona perfil de impresora válido", auto_size_text=True,text_color="red",justification="center")]],"-CHECKPRINTER2-", False)]], vertical_alignment="center",justification="center")],
	
        [sg.Column([[sg.Frame(title="",layout=[[sg.Text('· Tiempo de impresión', size=commonParams[0]),
        	sg.Text("(Horas:Minutos)", size=commonParams[0]),
         	sg.Input(key='-INaccess12-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Material Consumido', size=commonParams[0]),
        	sg.Text("(Gramos)", size=commonParams[0]),
         	sg.Input(key='-INaccess22-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de laminado', size=commonParams[0]),
        	sg.Text("(Euros)", size=commonParams[0]),
         	sg.Input(key='-INaccess32-', size=commonParams[1], enable_events=True)]])]], 				vertical_alignment='center', justification='center')],
        [sg.Column([[Collapse([[sg.Text("Dato mal introducido",size=commonParams[3],key="-CHECKINPUTS2-",text_color="red",justification="center")]],"-COLUMNINPUTS2-", False)]], vertical_alignment="center",justification="center")],
        [sg.Checkbox('Activar Opciones de Venta',
                     enable_events=True, key='-CHbox2-', font=commonParams[2])],
        
        [sg.Column([[Collapse(
            [[sg.Text("· Margen de Venta (%)", size=commonParams[0]), sg.Input(key='-INaccess42-', size=commonParams[1], enable_events=True)],
             [sg.Text("· Porcentaje de IVA (%)", size=commonParams[0]), sg.Input(key='-INaccess52-', size=commonParams[1], enable_events=True),
              sg.Help("Ayuda", tooltip="Margen de ventas debe ser 0 o superior", key="-Help2-", pad=((5, 0), (0, 0)), button_color=("blue"))]], '-Token2-', False)]], vertical_alignment='center', justification='center')],
        [sg.Text("")],
        [sg.HorizontalSeparator()],
      
        [sg.Column([
        	[sg.Column([[sg.Text("Coste Total", size=commonParams[4],justification="center",font=commonParams[2])]], justification="center")],
        	[sg.Column([[sg.Text("0 €",text_color="orange", key="-Text1-", size=commonParams[4],
                 	font=commonParams[5], justification="center")]], justification="center")],
            [sg.HorizontalSeparator(pad=((0,0), (5,5)))],
            [sg.Column([[sg.Text("Precio Venta", size=commonParams[4],justification="center",font=commonParams[2])]], justification="center")],
        	[sg.Column([[sg.Text("0 €",text_color="orange", key="-Text2-", size=commonParams[4],
                 	font=commonParams[5], justification="center")]], justification="center")]],justification="center"),
        	sg.VerticalSeparator(pad=((0,20),(0,0))),
            sg.Column([[sg.Multiline(reroute_stderr=False,autoscroll=True,size=(22,9),key="-OUTPUTPRINT-",reroute_stdout=True, disabled=True)]], justification="center", vertical_alignment="center")],
            
    
        [sg.HorizontalSeparator(pad=((0,0), (0,0)))],
        [sg.Text("")],
        [sg.Column([[sg.Button("Calcular", font=commonParams[2], key="-INsubmit2-", auto_size_button=True, pad=((0, 0),(0,0))), 
                     sg.Button("Reiniciar", key="-Reset2-", font=commonParams[2], pad=((20, 0), (0, 0)))]],
                     justification ="center")],
      
    ]

    layoutMain = [[sg.Column(layout1, key='-COL1-'),
                   sg.Column(layout2, visible=False, key='-COL2-')]]

    window = sg.Window('Estimador de costes', layoutMain, icon='Input/LogoIcon.ico')

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
            
        try:
            if values[f"-INaccess4{layout}-"] == "":
                window[f"-INaccess5{layout}-"].update("", disabled=True)
            else:
                window[f"-INaccess5{layout}-"].update(disabled=False)
        except TypeError:
            break
		
	#Al clickar el botón para calcular costes
        if event == f"-INsubmit{layout}-":

            '''
            Evalúa si hay un perfil de impresora seleccionado
	    '''
            chosPrinter = ""
            if values[f"-CHOSPRINTER{layout}-"] == "":
                window[f"-CHECKPRINTER{layout}-"].update(visible=True)
                chosPrinter = False
            else:
            	window[f"-CHECKPRINTER{layout}-"].update(visible=False)
	   
	   
            '''
            Evalúa si los input introducidos son válidos
	    '''
            badInputs = []
            checkTime = TimeValidation(values[f"-INaccess1{layout}-"])
            if checkTime==False:
            	badInputs.append("Tiempo")
            if MainValidation(values[f"-INaccess2{layout}-"])==False:
            	badInputs.append("Material")
            if MainValidation(values[f"-INaccess3{layout}-"])==False and values[f"-INaccess3{layout}-"]!="0":
                badInputs.append("Laminado")
            if badInputs == []:
                window[f"-COLUMNINPUTS{layout}-"].update(visible=False)
            else:
            	window[f"-CHECKINPUTS{layout}-"].update(value=", ".join(badInputs)+": mala introducción")
            	window[f"-COLUMNINPUTS{layout}-"].update(visible=True)
            
            if chosPrinter != "" or badInputs != []:
            	continue
            	
            
            '''
            Envía la información formateada a las funciones de cálculo de costes
	    '''	
            marginSales = ManageSales(MainValidation(values[f"-INaccess4{layout}-"]))
            
            ivaTax = ManageSales(MainValidation(values[f"-INaccess5{layout}-"]))

            electricityCost = KwCost(RefactorSupport(cur, values[f"-CHOSPRINTER{layout}-"],"KWprinter"),
            			RefactorSupport(cur, values[f"-CHOSPRINTER{layout}-"],"KWprize"),
            			checkTime)
            				
            materialCost = FilamentCost(RefactorSupport(cur,values[f"-CHOSPRINTER{layout}-"],"SpoolCost"), 
            				RefactorSupport(cur,values[f"-CHOSPRINTER{layout}-"],"SpoolWeight"),
            				MainValidation(values[f"-INaccess2{layout}-"]))
            				
            amortCost = AmortCost(RefactorSupport(cur,values[f"-CHOSPRINTER{layout}-"],"PrinterCost"), 
            				RefactorSupport(cur,values[f"-CHOSPRINTER{layout}-"],"AmortPrinter"),
            				checkTime)
            				
            designCost = MainValidation(values[f"-INaccess3{layout}-"])
            
            print(f"--------------\nCoste Electricidad: {electricityCost}\nCoste Material: {materialCost}\nCoste Laminado: {designCost}\nCoste Amortización: {amortCost}\n")
            
            '''
            Gestiona la información recibida de las funciones de costes y las muestra
	    '''
            totalCost = round(electricityCost+materialCost+amortCost+designCost,2)
            salesCost = round((totalCost*marginSales)*ivaTax,2)
            
            marginCostPrint = abs(round(totalCost*(marginSales-1),2))
            ivaCostPrint = abs(round(salesCost-totalCost-totalCost*(marginSales-1),2))
            print(f"Margen de venta: {marginCostPrint}\nCoste IVA: {ivaCostPrint}\n--------------")
	

            window["-Text1-"].update(f"{totalCost} €")
            window["-Text2-"].update(f"{salesCost} €")


            '''
            Guarda la información introducida entre cambio de layouts
            '''
            if checkSaved == False:
                window[f'-COL{layout}-'].update(visible=False)

                # layout = 1 if layout == 2 else 2
                layout = 2

                if opened != False:
                    window[f'-CHbox{layout}-'].update(value=True)
                    window[f'-Token{layout}-'].update(visible=opened)
                
                window[f"-CHOSPRINTER{2 if layout == 2 else 1}-"].update(
                        values[f"-CHOSPRINTER{1 if layout == 2 else 2}-"])

                for element in range(1, 6):
                    window[f"-INaccess{element}{2 if layout == 2 else 1}-"].update(
                        values[f"-INaccess{element}{1 if layout == 2 else 2}-"])

                window[f'-COL{layout}-'].update(visible=True)
                checkSaved = True
        
        '''
        Redirige al apartado de gestión de perfiles de impresora
        '''
        if event == "Opciones" or event == f"-EDITPRINTER{layout}-":
        	PopupOptions(con, cur)
        	window.Element(f"-CHOSPRINTER{2 if layout == 2 else 1}-").update(values=[element[0] for element in GetThings(cur)])

        '''
        Cierra la ventana
        '''
        if event == sg.WIN_CLOSED or event =="Salir":
            break

    window.close()



