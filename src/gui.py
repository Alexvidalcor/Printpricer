import PySimpleGUI as sg
from src.calc import FilamentCost, KwCost
from src.handler import MainValidation

sg.SetOptions(element_padding=((40, 0), (10, 10)))


def MainGui():

    electricityCost = 0
    materialCost = 0
    commonParams = [(30, 1), (10, 1),("Helvetica", 12)]

    layout1 = [[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=(commonParams[2]))],
        [sg.Text('· Precio Kw/hora', size=commonParams[0]),
         sg.Input(key='-INaccess11-', size=commonParams[1])],
        [sg.Text('· Horas de impresión', size=commonParams[0]),
         sg.Input(key='-INaccess21-', size=commonParams[1])],
        [sg.Text('· Coste de bobina', size=commonParams[0]),
         sg.Input(key='-INaccess31-', size=commonParams[1])],
        [sg.Text('· Gramos de bobina completa', size=commonParams[0]),
         sg.Input(key='-INaccess41-', size=commonParams[1])],
        [sg.Text('· Gramos de material consumido', size=commonParams[0]),
         sg.Input(key='-INaccess51-', size=commonParams[1])],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess61-', size=commonParams[1])],
        [sg.Button("Calcular", font=(commonParams[2]), key="-INsubmit1-", auto_size_button=True, pad=((115, 10),
                                                                                                     (25, 20))), sg.Cancel("Cancelar", key="-Quit1-", font=(commonParams[2]), pad=((0, 0), (25, 20)))]]

    layout2 = [[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=(commonParams[2]))],
        [sg.Text('· Precio Kw/hora', size=commonParams[0]),
         sg.Input(key='-INaccess12-', size=commonParams[1])],
        [sg.Text('· Horas de impresión', size=commonParams[0]),
         sg.Input(key='-INaccess22-', size=commonParams[1])],
        [sg.Text('· Coste de bobina', size=commonParams[0]),
         sg.Input(key='-INaccess32-', size=commonParams[1])],
        [sg.Text('· Gramos de bobina completa', size=commonParams[0]),
         sg.Input(key='-INaccess42-', size=commonParams[1])],
        [sg.Text('· Gramos de material consumido', size=commonParams[0]),
         sg.Input(key='-INaccess52-', size=commonParams[1])],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess62-', size=commonParams[1])],
        [sg.HorizontalSeparator()],
        [sg.Text(f"El coste total es {electricityCost+materialCost}", font=(commonParams[2]))],
        [sg.Button("Calcular", font=(commonParams[2]), key="-INsubmit2-", auto_size_button=True, pad=((115, 10),
                                                                                                     (25, 20))), sg.Cancel("Cancelar", key="-Quit2-", font=(commonParams[2]), pad=((0, 0), (25, 20)))],
    ]

    layoutMain = [[sg.Column(layout1, key='-COL1-'),
                   sg.Column(layout2, visible=False, key='-COL2-')]]

    window = sg.Window('Estimador de costes', layoutMain)

    layout = 1
    while True:
        event, values = window.read()
        if event == f"-INsubmit{layout}-":
            window[f'-COL{layout}-'].update(visible=False)
            electricityCost = KwCost(MainValidation(
                values[f"-INaccess1{layout}-"]), MainValidation(values[f"-INaccess2{layout}-"]))
            materialCost = FilamentCost(MainValidation(values[f"-INaccess3{layout}-"]), MainValidation(
                values[f"-INaccess4{layout}-"]), MainValidation(values[f"-INaccess5{layout}-"]))
            layout = 1 if layout == 2 else 2
            window[f'-COL{layout}-'].update(visible=True)
        if event == sg.WIN_CLOSED or event == f'-Quit{layout}-':
            break

    window.close()
