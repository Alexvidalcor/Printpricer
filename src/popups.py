import PySimpleGUI as sg

from src.db import CreateCon, SqlConnection, GetThings, PrepareCon
from src.handler import MainValidation


menu_def = [['Archivo', ['Salir']], [
    'Editar', ['Añadir', 'Eliminar', 'Refrescar']]]
commonParams = [("Helvetica", 10), (18, 1), "#ffff80",
                (2, 1), ("Helvetica", 15), (15, 1), (20, 1), (32, 1)]


def PopupDelete(con, cur):
    layout = [
        [sg.Text("Selecciona la impresora a eliminar:")],
        [sg.Combo(values=[element[0] for element in GetThings(cur)], key="-CHOSPRINTDEL-",
                  size=commonParams[1], change_submits=True)],
        [sg.Button("Aceptar", key="-ACEPTARDELETE-",
                   font=commonParams[0], auto_size_button=True)]
    ]

    window = sg.Window('Estimador', layout, icon='Input/LogoIcon.ico')

    while True:
        event, values = window.read()
        if event == "-ACEPTARDELETE-":
            PrepareCon(con, cur, where=["PrinterName",
                       values['-CHOSPRINTDEL-']], option="delete")
            break
        if event == sg.WIN_CLOSED or event == "Salir":
            break
    window.close()


def PopupOptions(con, cur):

    initLayout = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Text("")],
        [sg.Column([[sg.Text("Introduce los datos de tu impresora 3D", justification="center", font=("Helvetica", 12))]],
                   justification="center", vertical_alignment="center")],
        [sg.Text("")],
        [sg.Column([[sg.Frame("Elige tu impresora", [[sg.Combo(values=[element[0] for element in GetThings(cur)], key="-CHOSPRINTERPOP-", readonly=True, size=(33, 1), change_submits=True, pad=((15, 15), (30, 0)))], [sg.Button("Añadir", key="-ADDPRINTER-",
                                                                                                                                                                                                                                  pad=((15, 5), (30, 15))), sg.Button("Eliminar", key="-DELETPRINTER-", pad=((15, 5), (30, 15))), sg.Button("Refrescar", key="-REFRESHPRINTER-", pad=((15, 5), (30, 15)))]], element_justification="center")]], justification="center")],
        [sg.Text("", size=commonParams[1], font=commonParams[0])]]

    elecLayout = [
        [sg.Text("", size=commonParams[1], font=commonParams[0])],
        [sg.Column([
            [sg.Text('· Precio KW hora', size=commonParams[1], font=commonParams[0]),
             sg.Text(
                '(Euros)',  size=commonParams[5], font=commonParams[0]),
             sg.Input(key='-KWPRIZE-',
                      size=commonParams[1], disabled=True, font=commonParams[0], enable_events=True)],
            [sg.Text("", size=commonParams[7]), sg.Text("Dato mal introducido", visible=False,
                                                        key="-CHECKPOP1-", size=commonParams[6], text_color="red", justification="center")],
            [sg.Text('· KW Impresora',  size=commonParams[1], font=commonParams[0]),
             sg.Text('(KWatios)',
                     size=commonParams[5], font=commonParams[0]),
             sg.Input(key='-KWPRINTER-', disabled=True, size=commonParams[1], font=commonParams[0], enable_events=True)],
            [sg.Text("", size=commonParams[7]), sg.Text("Dato mal introducido", visible=False, key="-CHECKPOP2-", size=commonParams[6], text_color="red", justification="center")]], justification="center")]
    ]

    materialLayout = [
        [sg.Text("", size=commonParams[1], font=commonParams[0])],
        [sg.Column([
            [sg.Text('· Coste de bobina', size=commonParams[1], font=commonParams[0]),
             sg.Text(
                '(Euros)',  size=commonParams[5], font=commonParams[0]),
             sg.Input(key='-SPOOLCOST-',
                      size=commonParams[1], disabled=True, font=commonParams[0], enable_events=True)],
            [sg.Text("", size=commonParams[7]), sg.Text("Dato mal introducido", visible=False,
                                                        key="-CHECKPOP3-", size=commonParams[6], text_color="red", justification="center")],
            [sg.Text('· Bobina completa',  size=commonParams[1], font=commonParams[0]),
             sg.Text(
                '(Gramos)',  size=commonParams[5], font=commonParams[0]),
             sg.Input(key='-SPOOLWEIGHT-', disabled=True, size=commonParams[1], font=commonParams[0], enable_events=True)],
            [sg.Text("", size=commonParams[7]), sg.Text("Dato mal introducido", visible=False, key="-CHECKPOP4-", size=commonParams[6], text_color="red", justification="center")]], justification="center")]
    ]

    amortLayout = [
        [sg.Text("", size=commonParams[1], font=commonParams[0])],
        [sg.Column([
            [sg.Text('· Precio Impresora', size=commonParams[1], font=commonParams[0]),
             sg.Text('(Euros)',  size=commonParams[5], font=commonParams[0]),
             sg.Input(key='-COSTPRINTER-',
                      size=commonParams[1], disabled=True, font=commonParams[0], enable_events=True)],
            [sg.Text("", size=commonParams[7]), sg.Text("Dato mal introducido", visible=False,
                                                        key="-CHECKPOP5-", size=commonParams[6], text_color="red", justification="center")],
            [sg.Text('· Amort. Impresora',  size=commonParams[1], font=commonParams[0]),
             sg.Text('(Años)',  size=commonParams[5], font=commonParams[0]),
             sg.Input(key='-AMORTPRINTER-', disabled=True, size=commonParams[1], font=commonParams[0], enable_events=True)],
            [sg.Text("", size=commonParams[7]), sg.Text("Dato mal introducido", visible=False, key="-CHECKPOP6-", size=commonParams[6], text_color="red", justification="center")]], justification="center")]
    ]

    layout = [[initLayout], [sg.TabGroup(
        [[sg.Tab('Electricidad', elecLayout)], [sg.Tab('Material', materialLayout)], [sg.Tab('Amortización', amortLayout)]], key='-TABS-')], [sg.Column([[sg.Button("Actualizar", key="-ACTUALIZAR-", font=commonParams[4])]], justification="center")]]

    window = sg.Window('Perfiles', layout, icon='Input/LogoIcon.ico')

    while True:
        event, values = window.read()

        if event == "-ACTUALIZAR-":
            valKWprize = MainValidation(values["-KWPRIZE-"])
            valKWprinter = MainValidation(values["-KWPRINTER-"])
            valCostprinter = MainValidation(values["-COSTPRINTER-"])
            valAmortprinter = MainValidation(values["-AMORTPRINTER-"])
            valSpoolcost = MainValidation(values["-SPOOLCOST-"])
            valSpoolweight = MainValidation(values["-SPOOLWEIGHT-"])

            if valKWprize == 0:
                window.Element("-CHECKPOP1-").update(visible=True)
            else:
                window.Element("-CHECKPOP1-").update(visible=False)
            if valKWprinter == 0:
                window.Element("-CHECKPOP2-").update(visible=True)
            else:
                window.Element("-CHECKPOP2-").update(visible=False)
            if valSpoolcost == 0:
                window.Element("-CHECKPOP3-").update(visible=True)
            else:
                window.Element("-CHECKPOP3-").update(visible=False)
            if valSpoolweight == 0:
                window.Element("-CHECKPOP4-").update(visible=True)
            else:
                window.Element("-CHECKPOP4-").update(visible=False)
            if valCostprinter == 0:
                window.Element("-CHECKPOP5-").update(visible=True)
            else:
                window.Element("-CHECKPOP5-").update(visible=False)
            if valAmortprinter == 0:
                window.Element("-CHECKPOP6-").update(visible=True)
            else:
                window.Element("-CHECKPOP6-").update(visible=False)

            if 0 in [valKWprize, valKWprinter, valCostprinter, valAmortprinter, valSpoolcost, valSpoolweight]:
                continue

            for element in [(valKWprize, "KWPRIZE"), (valKWprinter, "KWPRINTER"), (valCostprinter, "COSTPRINTER"), (valAmortprinter, "AMORTPRINTER"), (valSpoolcost, "SPOOLCOST"), (valSpoolweight, "SPOOLWEIGHT")]:
                window.Element(f"-{element[1]}-").update(element[0])
            if valKWprinter != 0:
                PrepareCon(con, cur, option="update",
                           where=["PrinterName", values["-CHOSPRINTERPOP-"]],
                           values=(valKWprize, valKWprinter, valCostprinter, valAmortprinter, valSpoolcost, valSpoolweight))
                window.Element("-KWPRINTER-").update(valKWprinter)

        if event == "Refrescar" or event == "-REFRESHPRINTER-":
            for element in ["-KWPRIZE-", "-KWPRINTER-", "-COSTPRINTER-", "-AMORTPRINTER-", "-SPOOLCOST-", "-SPOOLWEIGHT-"]:
                window.Element(element).update(value="", disabled=True)
            window.Element(
                "-CHOSPRINTERPOP-").update(values=[element[0] for element in GetThings(cur)])
            for element in range(1, 7):
                window.Element(f"-CHECKPOP{element}-").update(visible=False)
        if event == "-CHOSPRINTERPOP-":
            for element in ["-KWPRIZE-", "-KWPRINTER-", "-COSTPRINTER-", "-AMORTPRINTER-", "-SPOOLCOST-", "-SPOOLWEIGHT-"]:
                window.Element(element).update(disabled=False)
            updaterValues = GetThings(
                cur, selection="*", where=["PrinterName", values["-CHOSPRINTERPOP-"]])[0]
            window.Element("-KWPRIZE-").update(updaterValues[2])
            window.Element("-KWPRINTER-").update(updaterValues[3])
            window.Element("-COSTPRINTER-").update(updaterValues[4])
            window.Element("-AMORTPRINTER-").update(updaterValues[5])
            window.Element("-SPOOLCOST-").update(updaterValues[6])
            window.Element("-SPOOLWEIGHT-").update(updaterValues[7])
            for element in range(1, 7):
                window.Element(f"-CHECKPOP{element}-").update(visible=False)

        if event == "Añadir" or event == "-ADDPRINTER-":
            for element in ["-KWPRIZE-", "-KWPRINTER-", "-COSTPRINTER-", "-AMORTPRINTER-", "-SPOOLCOST-", "-SPOOLWEIGHT-"]:
                window.Element(element).update(value="", disabled=True)
            newPrinter = sg.popup_get_text(
                "Introduce el nombre de tu impresora")
            if newPrinter == None or newPrinter=="":
	            continue
            PrepareCon(con, cur, values=(
                newPrinter,0.25,120,300,4,20,1000), option="add")
            window.Element(
                "-CHOSPRINTERPOP-").update(values=[element[0] for element in GetThings(cur)])
        elif event == "Eliminar" or event == "-DELETPRINTER-":
            for element in ["-KWPRIZE-", "-KWPRINTER-", "-COSTPRINTER-", "-AMORTPRINTER-", "-SPOOLCOST-", "-SPOOLWEIGHT-"]:
                window.Element(element).update(value="", disabled=True)
            PopupDelete(con, cur)
            window.Element(
                "-CHOSPRINTERPOP-").update(values=[element[0] for element in GetThings(cur)])

        if event == sg.WIN_CLOSED or event == "Salir":
            break

    window.close()
