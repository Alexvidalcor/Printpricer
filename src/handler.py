import re
import PySimpleGUI as sg

def MainValidation(candidate, result=0):
    if type(candidate) != str:
    	candidate = str(candidate)
    if "." in candidate or "," in candidate:
        if candidate.replace('.', '', 1).isdigit():
            result = float(candidate)
        elif candidate.replace(',', "",1).isdigit():
            result = float(candidate.replace(",",".",1))
    elif candidate.isdigit():
        result = int(candidate)

    return result

def TimeValidation(candidate, result="00:00"):
    if re.match(r"[0-9]{1,3}:[0-5]{1}[0-9]{1}", candidate):
        result = candidate
    elif ":" not in candidate:
        result = MainValidation(candidate)
        sg.popup_no_buttons("Por favor, introduzca el tiempo según el formato 'Horas:Minutos'.\n\nPara este caso, se ha convertido la cifra introducida a minutos",
        title="Atención",
        grab_anywhere=False,
        auto_close=True,
        auto_close_duration=3)
    return result

