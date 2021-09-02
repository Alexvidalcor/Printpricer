import re
import PySimpleGUI as sg


#FALTA QUE 0 SEA LEÍDO COMO TRUE QUIZÁS. REVISAR PLANTEAMIENTO.

def MainValidation(candidate, result=False):
    '''
    Transforma enteros o flotantes en string a int o float
    
    Si se introduce cualquier cosa no planteada, devuelve False
    '''
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

def TimeValidation(candidate, result=False):

    '''
    Valida si el tiempo establecido está en formato 000:00 y lo transforma a minutos.
    En caso contrario, sólo transforma los números introducidos a minutos.
    
    
    Si se introduce cualquier cosa no planteada, devuelve False
    '''
    
    if re.fullmatch(r"[0-9]{1,3}:[0-5]{1}[0-9]{1}", candidate):
        if type(candidate) == str:
            splitHours = int(re.split(r":[0-5]{1}[0-9]{1}", candidate)[0])
            splitMinutes = int(re.split(r"[0-9]{1,3}:", candidate)[1])
            result = (splitHours*60)+splitMinutes
    elif candidate.isdigit() and ":" not in candidate:
        result = MainValidation(candidate)
        if candidate!="0":
            sg.popup_no_buttons("Por favor, introduzca el tiempo según el formato 'Horas:Minutos'.\n\nPara este caso, se ha convertido la cifra introducida a minutos",
        	title="Atención",
        	grab_anywhere=False,
        	auto_close=True,
        	auto_close_duration=3)
    return result
