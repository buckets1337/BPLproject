#MachineGun.py

import classes

class MachineGun(classes.Weapon):
	def __init__(self):
		classes.Weapon.__init__(self, owner = None, name = 'Machine Gun', firepower = 1, tracking = 1, splash = 0, ammo = 1, rate = 2)