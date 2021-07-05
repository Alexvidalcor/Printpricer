def PopupOptions():
    commonParams = ["#ffff80", ("Helvetica", 15)]

    layoutPrep = [
                [sg.Text('· Coste de bobina', size=commonParams[0]),
         		sg.Input(key='-INaccess32-', size=commonParams[1], enable_events=True)],
        	[sg.Text('· Gramos de bobina completa', size=commonParams[0]),
 			sg.Input(key='-INaccess42-', size=commonParams[1], enable_events=True)],
            ]

    layoutMain = [[sg.Column(layoutPrep, element_justification='center')]]
    
    window = sg.Window(':)', layoutMain, icon=r'input/LogoIcon.png')

    while True:           
        event, values = window.read()
 
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
    window.close()
