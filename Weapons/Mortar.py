#Mortar.py

import classes

class Mortar(classes.Weapon):
	def __init__(self):
		classes.Weapon.__init__(self, owner = None, name = 'Mortar', firepower = 2, tracking = 1, splash = 1, ammo = 1, rate = 1)