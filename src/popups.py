def PopupOptions():
    commonParams = ["#ffff80", ("Helvetica", 15)]

    layoutPrep = [
    		[sg.Text('· Precio KW hora', size = commonParams[0]),
    			 sg.Input(key="-KWPRICE-" size = commonParams[0])],

    		[sg.Text("", size= commonParams[0]],
    		[sg.HorizontalSeparator()],
    		[sg.Text("", size= commonParams[0]],
    		[sg.Text('· KW Impresora', size = commonParams[0]),
    			 sg.Input(key="-KWPRINTER-", size = commonParams[0])],
    		[sg.Text('· Amort. Impresora', size = commonParams[0]),
    			 sg.Input(key="-AMORTPRINTER-" size = commonParams[0])],
    		[sg.Text("", size= commonParams[0]],
    		[sg.HorizontalSeparator()],
    		[sg.Text("", size= commonParams[0]],
                [sg.Text('· Coste de bobina', size=commonParams[0]),
         		sg.Input(key='-SPOOLCOST-', size=commonParams[1], enable_events=True)],
        	[sg.Text('· Gramos de bobina completa', size=commonParams[0]),
 			sg.Input(key='-SPOOLWEIGHT-', size=commonParams[1], enable_events=True)],
            ]

    layoutMain = [[sg.Column(layoutPrep, element_justification='center')]]
    
    window = sg.Window(':)', layoutMain, icon=r'input/LogoIcon.png')

    while True:           
        event, values = window.read()
 
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
    window.close()
