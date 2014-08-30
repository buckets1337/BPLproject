#RFIDreader.py
#grabs the codes from the RFID reader and turns them into a team definition file

import pygame, sys, os, importlib, imp
from pygame.locals import *
import CONFIG

pygame.init()

screen = pygame.display.set_mode(CONFIG.SCREEN_SIZE)
font = pygame.font.SysFont('monospace', 16)
clock = pygame.time.Clock()

teamList = []
playerDef = []
inputString = 'input: '

def finishUp():
	for player in teamList:
		print player
	fileName = sys.argv[1]
	f = open(fileName, 'w')
	for player in teamList:
		for character in player:
			f.write(character)
		f.write("\n")
	f.close

def setupWeapons(weapDict, weapon1ID, weapon2ID, weapon3ID, weapon4ID):
	'''
	configures the mech's weapons when the mech is created
	'''
	weapons = []
	weaponDefList = weapDict

	if int(weapon1ID) > len(CONFIG.WEAPON_REGISTER):
		print "!!!weapon ID is not in weapon register"
		return

	newWeapon1ID = CONFIG.WEAPON_REGISTER[int(weapon1ID)]
	newWeapon2ID = CONFIG.WEAPON_REGISTER[int(weapon2ID)]
	newWeapon3ID = CONFIG.WEAPON_REGISTER[int(weapon3ID)]
	newWeapon4ID = CONFIG.WEAPON_REGISTER[int(weapon4ID)]

	newWeaponIDList = [newWeapon1ID, newWeapon2ID, newWeapon3ID, newWeapon4ID]

	for weapon in newWeaponIDList:
		if weapon == 'SlugGun':
			newWeapon = weaponDefList['SlugGun'].SlugGun()
		elif weapon == 'MachineGun':
			newWeapon = weaponDefList['MachineGun'].MachineGun()
		elif weapon == 'Mortar':
			newWeapon = weaponDefList['Mortar'].Mortar()

		elif weapon == 'None' or weapon == None:
			newWeapon = None

		# if weapon != None:
		# 	newWeapon.owner = self
		# 	newWeapon.console = self.console
		weapons.append(newWeapon)
		
	return weapons

def loadWeaponModules(directory):
    '''
    loads all of the weapons defined by the weapon modules into the world
    '''

    fileList = os.listdir(directory)

    weaponDict = {}

    for weapon in fileList:
        if weapon.endswith('.py'):
            weapon = weapon[:-3]
        elif weapon.endswith('.pyc'):
            weapon = weapon[:-4]


        weaponFile = imp.find_module(weapon, [directory])
        weaponModule = imp.load_module(weapon, weaponFile[0], weaponFile[1], ('.py', 'r', imp.PY_SOURCE) )
        weaponDict[weapon] = weaponModule

    return weaponDict

def renderStats(screen, playerDef, inputString):
	for character in playerDef:
		inputString += character
	inputSurf = font.render(inputString, True, (255,255,255))
	screen.blit(inputSurf, (10,10))

	headerSurf = font.render('ID    Armor    Health    Evade    HeatSinks    Weapon1        Weapon2        Weapon3        Weapon4', True, (255,255,255))
	screen.blit(headerSurf, (10,50))

	ypos = 75
	heatSinks = 0
	for player in teamList:
		playerString = ''
		ID = player[0] + player[1]
		heatSinks = player[2]
		armor = player[3]
		health = str(2*int(armor)+2)

		wep1 = player[4]+player[5]
		wep2 = player[6]+player[7]
		wep3 = player[8]+player[9]
		wep4 = player[10]+player[11]
		weapDict = loadWeaponModules('Weapons')
		weapList = setupWeapons(weapDict, wep1, wep2, wep3, wep4)
		if weapList[0] != None:
			weapon1 = weapList[0].name
			if len(weapon1) > 9:
				weapon1 = weapon1[:9]
				weapon1 += '..'
		else:
			weapon1 = 'None'

		if weapList[1] != None:
			weapon2 = weapList[1].name
			if len(weapon2) > 9:
				weapon2 = weapon2[:9]
				weapon2 += '..'
		else:
			weapon2 = 'None'

		if weapList[2] != None:
			weapon3 = weapList[2].name
			if len(weapon3) > 9:
				weapon3 = weapon2[:9]
				weapon3 += '..'
		else:
			weapon3 = 'None'

		if weapList[3] != None:
			weapon4 = weapList[3].name
			if len(weapon4) > 9:
				weapon4 = weapon2[:9]
				weapon4 += '..'
		else:
			weapon4 = 'None'



		evade = CONFIG.BASE_EVASION
		if int(armor) != 0:
			evade -= 2*int(armor)
		# if self.targeting != 0:
		#     evasion -= self.targeting
		if int(heatSinks) != 0:
			evade -= int(heatSinks)
		for weapon in weapList:
			if weapon != None:
				evade -= weapon.speedPenalty
		if evade > 0:
			evade = str(int((evade / 20) * 100))
		else:
			evade = '0% (' + str(0-int(evade)) + ')'
		if evade != '0':
			if not evade.endswith(")"):
				evade += '%'
		else:
			evade += "%  "


		playerString = str(ID) + "    " + str(armor) + "        " + str(health) + (" " * (10-len(health))) + str(evade) + (" " *(9-len(evade))) + str(heatSinks) + "            " + str(weapon1) + (" " * (15-len(weapon1))) + str(weapon2) + (" " * (15-len(weapon2))) + str(weapon3) + (" " * (15-len(weapon3))) + str(weapon4)

		playerSurf = font.render(playerString, True, (255,255,255))
		screen.blit(playerSurf, (10, ypos))
		ypos += 15



while True:
	clock.tick(20)
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
			if event.key == pygame.K_RETURN:
				if len(playerDef) == 12:
					teamList.append(playerDef)
					playerDef = []
					inputString = 'input: '
					#print teamList
				else:
					print "Player definitions must be 12 characters in length."
					playerDef = []

			elif event.key == pygame.K_SPACE:
				finishUp()
				sys.exit()

			else:
				playerDef.append(pygame.key.name(event.key))


	screen.fill((0,0,0))
	renderStats(screen, playerDef, inputString)
	pygame.display.flip()