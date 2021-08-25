from src.gui import *
from tkinter import TclError



try:
	sg.popup_auto_close(
    title = "Bienvenid@ a Gcode Estimator",
    button_type = 5,
    auto_close = True,
    auto_close_duration = 1,
    icon = None,
    no_titlebar = True,
    grab_anywhere = False,
    keep_on_top = True,
    image = "Input/LogoStart.png")

	MainGui()
except TclError:
	print("Programa Terminado")
