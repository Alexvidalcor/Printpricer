import PySimpleGUI as sg
from src.calc import FilamentCost, KwCost
from src.handler import MainValidation

sg.SetOptions(element_padding=((40, 0), (10, 10)))


def Collapse(layout, key, visible):
    return sg.pin(sg.Column(layout, key=key, visible=visible))


def Reset(window, layout):
    for element in range(1, 9):
        window[f"-INaccess{element}{2 if layout == 2 else 1}-"].update("")

def MainGui():

    electricityCost = 0
    materialCost = 0
    ivaTax = 0
    marginSales = 0
    commonParams = [(30, 1), (10, 1), ("Helvetica", 12), (20, 1), (38, 1)]

    layout1 = [[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=commonParams[2])],
        [sg.Text('· Precio Kw/hora', size=commonParams[0]),
         sg.Input(key='-INaccess11-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Horas de impresión', size=commonParams[0]),
         sg.Input(key='-INaccess21-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de bobina', size=commonParams[0]),
         sg.Input(key='-INaccess31-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Gramos de bobina completa', size=commonParams[0]),
         sg.Input(key='-INaccess41-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Gramos de material consumido', size=commonParams[0]),
         sg.Input(key='-INaccess51-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess61-', size=commonParams[1], enable_events=True)],
        [sg.Checkbox('Activar Opciones de Venta', enable_events=True,
                     key='-CHbox1-', font=commonParams[2])],
        [Collapse(
            [[sg.Text("· Margen de Venta (%)", size=commonParams[3]), sg.Input(key='-INaccess71-', size=commonParams[1], enable_events=True)],
             [sg.Text("· Porcentaje de IVA (%)", size=commonParams[3]), sg.Input(key='-INaccess81-', disabled=True, size=commonParams[1], enable_events=True),
              sg.Help("Ayuda", tooltip="Margen de ventas debe ser 0 o superior", key="-Help1-", pad=((5, 0), (0, 0)), button_color=("blue"))]], '-Token1-', False)],
        [sg.HorizontalSeparator(pad=((0, 40), (0, 0)))],
        [sg.Button("Calcular", font=commonParams[2], key="-INsubmit1-", auto_size_button=True, pad=((115, 10),
                                                                                                    (25, 20))), sg.Button("Reiniciar", key="-Reset1-", font=commonParams[2], pad=((0, 0), (25, 20)))],
    ]

    layout2 = [[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=(commonParams[2]))],
        [sg.Text('· Precio Kw/hora', size=commonParams[0]),
         sg.Input(key='-INaccess12-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Horas de impresión', size=commonParams[0]),
         sg.Input(key='-INaccess22-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de bobina', size=commonParams[0]),
         sg.Input(key='-INaccess32-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Gramos de bobina completa', size=commonParams[0]),
         sg.Input(key='-INaccess42-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Gramos de material consumido', size=commonParams[0]),
         sg.Input(key='-INaccess52-', size=commonParams[1], enable_events=True)],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess62-', size=commonParams[1], enable_events=True)],
        [sg.Checkbox('Activar Opciones de Venta',
                     enable_events=True, key='-CHbox2-', font=commonParams[2])],
        [Collapse(
            [[sg.Text("· Margen de Venta (%)", size=commonParams[3]), sg.Input(key='-INaccess72-', size=commonParams[1], enable_events=True)],
             [sg.Text("· Porcentaje de IVA (%)", size=commonParams[3]), sg.Input(key='-INaccess82-', size=commonParams[1], enable_events=True),
              sg.Help("Ayuda", tooltip="Margen de ventas debe ser 0 o superior", key="-Help2-", pad=((5, 0), (0, 0)), button_color=("blue"))]], '-Token2-', False)],
        [sg.HorizontalSeparator(pad=((0, 40), (0, 0)))],
        [sg.Text("El coste total es 0 €", key="-Text1-", size=commonParams[4],
                 font=commonParams[2], justification="center")],
        [sg.Text(f"El precio de venta es 0 €", key="-Text2-",
                 size=commonParams[4], font=commonParams[2], justification="center")],
        [sg.Button("Calcular", font=commonParams[2], key="-INsubmit2-", auto_size_button=True, pad=((115, 10),
                                                                                                    (25, 20))), sg.Button("Reiniciar", key="-Reset2-", font=commonParams[2], pad=((0, 0), (25, 20)))],
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

        if values[f"-INaccess7{layout}-"] == "":
            window[f"-INaccess8{layout}-"].update("", disabled=True)
        else:
            window[f"-INaccess8{layout}-"].update(disabled=False)

        if event == f"-INsubmit{layout}-":

            marginSales = MainValidation(
                values[f"-INaccess7{layout}-"])/100 if values[f"-INaccess7{layout}-"] else 0
            ivaTax = MainValidation(
                values[f"-INaccess8{layout}-"])/100 if values[f"-INaccess8{layout}-"] else 0
            electricityCost = KwCost(MainValidation(
                values[f"-INaccess1{layout}-"]), MainValidation(values[f"-INaccess2{layout}-"]))
            materialCost = FilamentCost(MainValidation(values[f"-INaccess3{layout}-"]), MainValidation(
                values[f"-INaccess4{layout}-"]), MainValidation(values[f"-INaccess5{layout}-"]))
            designCost = MainValidation(values[f"-INaccess6{layout}-"])

            totalCost = f"El coste total es {round(electricityCost+materialCost+designCost,2)} €"
            if marginSales != 0:
                salesCost = f"El precio de venta es {round((((electricityCost+materialCost+designCost)*(marginSales+1))*(ivaTax+1)),2)} €"
            elif marginSales == 0:
                salesCost = f"El precio de venta (sólo IVA) es {round((electricityCost+materialCost+designCost)*(ivaTax+1),2)} €"
            window["-Text1-"].update(totalCost)
            window["-Text2-"].update(salesCost)

            if checkSaved == False:
                window[f'-COL{layout}-'].update(visible=False)

                # layout = 1 if layout == 2 else 2
                layout = 2

                if opened != False:
                    window[f'-CHbox{layout}-'].update(value=True)
                    window[f'-Token{layout}-'].update(visible=opened)

                for element in range(1, 9):
                    window[f"-INaccess{element}{2 if layout == 2 else 1}-"].update(
                        values[f"-INaccess{element}{1 if layout == 2 else 2}-"])

                window[f'-COL{layout}-'].update(visible=True)
                checkSaved = True

        if event == sg.WIN_CLOSED:
            break

    window.close()
