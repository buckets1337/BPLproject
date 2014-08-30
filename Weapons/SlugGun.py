# SlugGun.py
# a sample weapon definition.  This one is really weak, though


import classes

class SlugGun(classes.Weapon):
	def __init__(self):
		classes.Weapon.__init__(self, owner = None, name = 'Slug Gun', firepower = 1, tracking = 1, splash = 0, ammo = 1, rate = 1)





