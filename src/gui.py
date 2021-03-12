import PySimpleGUI as sg
from src.calc import FilamentCost, KwCost
from src.handler import MainValidation

sg.SetOptions(element_padding=((50, 0), (10, 10)))


def MainGui():

    electricityCost = 0
    materialCost = 0
    commonParams = [(30, 1), (10, 1),("Helvetica", 12)]

    layout1 = [[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=(commonParams[2]))],
        [sg.Text('· Precio Kw/hora', size=commonParams[0]),
         sg.Input(key='-INaccess1-', size=commonParams[1])],
        [sg.Text('· Horas de impresión', size=commonParams[0]),
         sg.Input(key='-INaccess2-', size=commonParams[1])],
        [sg.Text('· Coste de bobina', size=commonParams[0]),
         sg.Input(key='-INaccess3-', size=commonParams[1])],
        [sg.Text('· Gramos de bobina completa', size=commonParams[0]),
         sg.Input(key='-INaccess4-', size=commonParams[1])],
        [sg.Text('· Gramos de material consumido', size=commonParams[0]),
         sg.Input(key='-INaccess5-', size=commonParams[1])],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess6-', size=commonParams[1])],
        [sg.Button("Calcular", font=(commonParams[2]), key="-INsubmit-", auto_size_button=True, pad=((145, 10),
                                                                                                     (25, 20))), sg.Cancel("Cancelar", key="Quit", font=(commonParams[2]), pad=((0, 0), (25, 20)))]]

    layout2 = [[sg.Text('Introduce los siguientes datos para recibir la estimación:', pad=(
        (10, 0), (10, 0)), size=(50, 2), font=(commonParams[2]))],
        [sg.Text('· Precio Kw/hora', size=commonParams[0]),
         sg.Input(key='-INaccess1-', size=commonParams[1])],
        [sg.Text('· Horas de impresión', size=commonParams[0]),
         sg.Input(key='-INaccess2-', size=commonParams[1])],
        [sg.Text('· Coste de bobina', size=commonParams[0]),
         sg.Input(key='-INaccess3-', size=commonParams[1])],
        [sg.Text('· Gramos de bobina completa', size=commonParams[0]),
         sg.Input(key='-INaccess4-', size=commonParams[1])],
        [sg.Text('· Gramos de material consumido', size=commonParams[0]),
         sg.Input(key='-INaccess5-', size=commonParams[1])],
        [sg.Text('· Coste de diseño (Opcional)', size=commonParams[0]),
         sg.Input(key='-INaccess6-', size=commonParams[1])],
        [sg.Button("Calcular", font=(commonParams[2]), key="-INsubmit-", auto_size_button=True, pad=((145, 10),
                                                                                                     (25, 20))), sg.Cancel("Cancelar", key="Quit", font=(commonParams[2]), pad=((0, 0), (25, 20)))],
        [sg.HorizontalSeparator()],
        [sg.Text(
            f"El coste total es {electricityCost+materialCost}", font=(commonParams[2]))]
    ]

    layoutMain = [[sg.Column(layout1, key='-COL1-'),
                   sg.Column(layout2, visible=False, key='-COL2-')]]

    window = sg.Window('Estimador de costes', layoutMain)

    layout = 1
    while True:
        event, values = window.read()
        if event == "-INsubmit-":
            window[f'-COL{layout}-'].update(visible=False)
            electricityCost = KwCost(MainValidation(
                values["-INaccess1-"]), MainValidation(values["-INaccess2-"]))
            materialCost = FilamentCost(MainValidation(values["-INaccess3-"]), MainValidation(
                values["-INaccess4-"]), MainValidation(values["-INaccess5-"]))
            layout = 1 if layout == 2 else 2
            window[f'-COL{layout}-'].update(visible=True)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()
