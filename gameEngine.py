#gameEngine.py
#handles all of the game logic, running turns and dealing damage, etc

class GameEngine():
	def __init__(self, redTeamList, blueTeamList, console):
		self.redTeamList = redTeamList
		self.blueTeamList = blueTeamList
		self.console = console
		self.turnNumber = 1
		self.winResult = False

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

	def turn(self):
		'''
		handles running one game turn
		'''

		if self.winResult:
			return

		#print "Turn " + str(self.turnNumber)
		self.console.messageList.insert(0,"*** Turn " + str(self.turnNumber) +" ***")
		self.turnNumber += 1



		for mech in self.redTeamList:
			#print mech.weapons
			for gun in mech.weapons:
				#print gun
				if gun != None and gun != 'None':
					target = mech.selectTarget(self.blueTeamList)
					mech.attack(target, gun, self.blueTeamList)

		for mech in self.blueTeamList:
			for gun in mech.weapons:
				#print gun
				if gun != None and gun != 'None':
					target = mech.selectTarget(self.redTeamList)
					mech.attack(target, gun, self.redTeamList)

		self.resolveDamage()

		self.console.messageList.insert(0, '')

		self.winResult = self.checkForWinner()
		#self.console.messageList = []

	def resolveDamage(self):
		'''
		applies damage dealt during the turn to all combatants simultaneously
		'''
		print "*** " + str(self.turnNumber - 1) + " ***"
		#mechList = self.redTeamList + self.blueTeamList
		for mech in self.redTeamList:
			mech.health -= mech.damageTaken
			print mech.name, mech.damageTaken, mech.health

			if mech.health <= 0:
				mech.deathBlow = mech.damageTaken
				self.redTeamList = mech.death(self.redTeamList)

				#print self.redTeamList

			mech.damageTaken = 0


		for mech in self.blueTeamList:
			mech.health -= mech.damageTaken
			print mech.name, mech.damageTaken, mech.health

			if mech.health <= 0:
				mech.deathBlow = mech.damageTaken
				self.blueTeamList = mech.death(self.blueTeamList)

				#print self.blueTeamList

			mech.damageTaken = 0

		print " "




