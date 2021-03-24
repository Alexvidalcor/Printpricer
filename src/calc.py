
import re

def FilamentCost(SpoolCost, SpoolWeight, SpoolConsumed):
	try:
		return (SpoolCost/SpoolWeight)*SpoolConsumed

	except ZeroDivisionError:
		return SpoolConsumed
	
def KwCost(kwExpense, timePrinting):

	print(timePrinting)

	hours = re.split(r"[0-9]{1,3}:", timePrinting)
	minutes = re.split(r":[0-9]{1,2}", timePrinting)

	print(hours, minutes)

	return 0
