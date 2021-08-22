from src.gui import *
from tkinter import TclError
try:
	MainGui()
except TclError:
	print("Programa Terminado")
