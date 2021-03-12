
def FilamentCost(SpoolCost, SpoolWeight, SpoolConsumed):
	try:
		return (SpoolCost/SpoolWeight)*SpoolConsumed

	except ZeroDivisionError:
		return SpoolConsumed
	
def KwCost(kwExpense, hoursPrinting):
	return kwExpense * hoursPrinting
