
import re

def FilamentCost(SpoolCost, SpoolWeight, SpoolConsumed):
	try:
		return (SpoolCost/SpoolWeight)*SpoolConsumed

	except ZeroDivisionError:
		return SpoolConsumed
	
def KwCost(kwPrinter, kwExpense, timePrinting):	
	return round(timePrinting * (kwPrinter/60 * kwExpense/60),2)
	
def ManageSales(numberSales):
	return (numberSales/100 if numberSales else 0)+1

def AmortCost(printerCost, years, timePrinting):
	#REPLANTEAR FÓRMULA DE AMORTIZACIÓN
	repairPercent = 0.25
	dailyHours = 4
	
	return round((printerCost/(years*(365*dailyHours*60))+printerCost*repairPercent/(years*(365*dailyHours*60)/4))*timePrinting,2)
	
