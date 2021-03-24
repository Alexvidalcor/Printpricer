import re

def MainValidation(candidate, result=0):
    if "." in candidate:
        if candidate.replace('.', '', 1).isdigit():
            result = float(candidate)
    elif candidate.isdigit():
        result = int(candidate)

    return result

def TimeValidation(candidate, result="00:00"):
    if re.match(r"[0-9]{1,3}:[0-9]{1,2}", candidate):
        result = candidate
    return result

