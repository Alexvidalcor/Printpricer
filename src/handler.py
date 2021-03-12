def MainValidation(candidate, result=False):

    if "." in candidate:
        if candidate.replace('.', '', 1).isdigit():
            result = float(candidate)
    elif candidate.isdigit():
        result = int(candidate)

    return result
