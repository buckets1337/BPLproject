#gameEngine.py
#handles all of the game logic, running turns and dealing damage, etc
import random

class GameEngine():
	def __init__(self, redTeamList, blueTeamList, console):
		self.redTeamList = redTeamList
		self.blueTeamList = blueTeamList
		self.redTeamDamage = 0
		self.blueTeamDamage = 0

		self.initiativeOrder = []
		for i in range(len(self.redTeamList + self.blueTeamList)):
			self.initiativeOrder.append(None)

		self.console = console
		self.turnNumber = 1
		self.winResult = False

		self.rollForInitiative()


	def checkForWinner(self):
		if self.redTeamList == [] and self.blueTeamList == []:
			self.console.messageList.insert(0, "Everyone Died!  It's a Tie!")
			return True
		elif self.redTeamList == []:
			self.console.messageList.insert(0, "Blue Team Wins!")
			return True
		elif self.blueTeamList == []:
			self.console.messageList.insert(0, "Red Team Wins!")
			return True
		else:
			return False


	def rollForInitiative(self):
		totalMechList = self.redTeamList + self.blueTeamList

		for mech in totalMechList:
			initMod = random.randrange(75,125)
			mech.initiative = int((mech.evasion * initMod) / 100)
			location = 0
			for otherMech in self.initiativeOrder:
				if otherMech is not None:
					# print "O:" + str(otherMech.initiative)
					# print "S:" + str(mech.initiative)
					if otherMech.initiative > mech.initiative:
						location = self.initiativeOrder.index(otherMech) + 1
					else:
						location = self.initiativeOrder.index(otherMech) - 1
				else:
					location = self.initiativeOrder.index(otherMech) - 1
					self.initiativeOrder.remove(otherMech)
			# print location
			if location < 0:
				location = 0
			self.initiativeOrder.insert(location, mech)

		#print self.initiativeOrder


	def round(self, mech, gameState):
		'''
		one mech's actions in a turn
		'''
		if mech.team == 'Red':
			targets = self.blueTeamList
		elif mech.team == 'Blue':
			targets = self.redTeamList

		for gun in mech.weapons:
				#print gun
			if gun != None and gun != 'None':
					target = mech.selectTarget(targets)
					gameState = mech.attack(gameState, target, gun, targets)

		self.resolveDamage()
		self.console.messageList.insert(0, '')
		return gameState


	def turn(self, gameState):
		'''
		handles running one game turn
		'''

		if self.winResult:
			return

		#print "Turn " + str(self.turnNumber)
		if len(self.initiativeOrder) == (len(self.redTeamList) + len(self.blueTeamList)):
			self.console.messageList.insert(0, (26*"*") + " Turn " + str(self.turnNumber) + " " + (32*"*"))
			self.turnNumber += 1


		if len(self.initiativeOrder) > 0:
			mech = self.initiativeOrder.pop(0)
			gameState = self.round(mech, gameState)

		# for mech in self.redTeamList:
		# 	#print mech.weapons
		# 	for gun in mech.weapons:
		# 		#print gun
		# 		if gun != None and gun != 'None':
		# 			target = mech.selectTarget(self.blueTeamList)
		# 			mech.attack(target, gun, self.blueTeamList)

		# for mech in self.blueTeamList:
		# 	for gun in mech.weapons:
		# 		#print gun
		# 		if gun != None and gun != 'None':
		# 			target = mech.selectTarget(self.redTeamList)
		# 			mech.attack(target, gun, self.redTeamList)

		# self.resolveDamage()

		# self.console.messageList.insert(0, '')

			self.winResult = self.checkForWinner()

		else:
			self.initiativeOrder = []
			for i in range(len(self.redTeamList + self.blueTeamList)):
				self.initiativeOrder.append(None)
			self.rollForInitiative()
			self.console.messageList.insert(0, (26* "-") + " Turn " + str(self.turnNumber - 1) +" End " + (28* "-"))
			if len(str(int(self.blueTeamDamage))) == 1:
				redPad = " "
			else:
				redPad = ""
			if len(str(int(self.redTeamDamage))) == 1:
				bluePad = " "
			else:
				bluePad = ""
			self.console.messageList.insert(0, "Red Team:  " + str(int(self.blueTeamDamage)) + " damage dealt")# + redPad + "     |     " + str(int(self.redTeamDamage)) + " damage taken")
			self.console.messageList.insert(0,  "Blue Team: " + str(int(self.redTeamDamage)) + " damage dealt")# + bluePad + "     |     " + str(int(self.blueTeamDamage)) + " damage taken")
			self.console.messageList.insert(0, " ")
			if self.redTeamDamage < self.blueTeamDamage:
				self.console.messageList.insert(0, "Red wins the turn!")
			elif self.blueTeamDamage < self.redTeamDamage:
				self.console.messageList.insert(0, "Blue wins the turn!")
			else:
				self.console.messageList.insert(0, "The turn is a tie!")
			self.console.messageList.insert(0, " ")
			self.console.messageList.insert(0, " ")
			self.console.messageList.insert(0, " ")

			self.redTeamDamage = 0
			self.blueTeamDamage = 0

		return gameState


		#self.console.messageList = []


	def resolveDamage(self):
		'''
		applies damage dealt during the turn to all combatants simultaneously
		'''
		print "*** " + str(self.turnNumber - 1) + " ***"
		#mechList = self.redTeamList + self.blueTeamList
		for mech in self.redTeamList:
			mech.health -= mech.damageTaken
			self.redTeamDamage += mech.damageTaken
			print mech.name, mech.damageTaken, mech.health

			if mech.health <= 0:
				mech.deathBlow = mech.damageTaken
				self.redTeamList = mech.death(self.redTeamList)

				#print self.redTeamList

			mech.damageTaken = 0


		for mech in self.blueTeamList:
			mech.health -= mech.damageTaken
			self.blueTeamDamage += mech.damageTaken
			print mech.name, mech.damageTaken, mech.health

			if mech.health <= 0:
				mech.deathBlow = mech.damageTaken
				self.blueTeamList = mech.death(self.blueTeamList)

				#print self.blueTeamList

			mech.damageTaken = 0

		#print " "




