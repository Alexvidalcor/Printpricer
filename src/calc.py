
import re

def FilamentCost(SpoolCost, SpoolWeight, SpoolConsumed):
	try:
		return (SpoolCost/SpoolWeight)*SpoolConsumed

	except ZeroDivisionError:
		return SpoolConsumed
	
def KwCost(kwExpense, timePrinting):

	if type(timePrinting) == str:
		hours = int(re.split(r":[0-5]{1}[0-9]{1}", timePrinting)[0])
		minutes = int(re.split(r"[0-9]{1,3}:", timePrinting)[1])
		totalCost = ((hours*60)+minutes)/60
	else:
		totalCost = timePrinting/60
	
	return totalCost * kwExpense
