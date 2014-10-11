#gameEngine.py
#handles all of the game logic, running turns and dealing damage, etc

# import the 'random' module, letting us pick random numbers
import random

# the GameEngine is an 'invisible' object that makes things happen when a key on the keyboard is pressed.
class GameEngine():

	# set up the GameEngine object, telling it who the teams are, and how much damage each team has taken (which will be 0 since the game just started).
	# Then determine the order the mechs will fire in.
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


	# Each round, the GameEngine object checks to make sure both teams still have mechs remaining.  If one team is out of mechs, the game ends, and the
	# team with mechs remaining wins!
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


	# At the beginning of each game 'turn', set the order that mechs get to fire in based on their evasion stat, with some randomness.
	def rollForInitiative(self):
		totalMechList = self.redTeamList + self.blueTeamList

		# for each mech, give it a score based on evasion, with a random modifier.
		for mech in totalMechList:
			initMod = random.randrange(75,125)
			mech.initiative = int((mech.evasion * initMod) / 100)
			location = 0

			# compare the mech's initiative score to the other mechs, and put it in the queue accordingly
			for otherMech in self.initiativeOrder:
				if otherMech is not None:

					if otherMech.initiative > mech.initiative:
						location = self.initiativeOrder.index(otherMech) + 1
					else:
						location = self.initiativeOrder.index(otherMech) - 1
				else:
					location = self.initiativeOrder.index(otherMech) - 1
					self.initiativeOrder.remove(otherMech)

			# if somehow the mech ends up before the start of the queue, give them the first spot in the queue instead.
			if location < 0:
				location = 0
			self.initiativeOrder.insert(location, mech)


	# Describes what happens when each mech gets it's chance to fire that turn.
	def round(self, mech, gameState):
		'''
		one mech's actions in a turn
		'''
		# define who the enemy is.
		if mech.team == 'Red':
			targets = self.blueTeamList
		elif mech.team == 'Blue':
			targets = self.redTeamList

		# for each weapon the mech has, choose a target, and then attempt to take a shot at it
		for gun in mech.weapons:
			if gun != None and gun != 'None':
					target = mech.selectTarget(targets)
					gameState = mech.attack(gameState, target, gun, targets)

		# once all weapons have fired, deal damage to targets that were hit
		self.resolveDamage()
		self.console.messageList.insert(0, '')

		# return information about whether the game has ended or not.
		return gameState


	# Describes a full turn, with each surviving mech getting a round in which to fire their weapons at the other team
	def turn(self, gameState):
		'''
		handles running one game turn
		'''
		# if there is a winner to the game, don't bother with the turn
		if self.winResult:
			return

		# display a message in the console declaring what turn number it is.
		if len(self.initiativeOrder) == (len(self.redTeamList) + len(self.blueTeamList)):
			self.console.messageList.insert(0, (26*"*") + " Turn " + str(self.turnNumber) + " " + (32*"*"))
			self.turnNumber += 1

		# Grab the first mech in the queue.  Give it a round to fire it's weapons.  Afterward, check to see if that was enough to cause one
		# team to win the game.
		if len(self.initiativeOrder) > 0:
			mech = self.initiativeOrder.pop(0)
			gameState = self.round(mech, gameState)

			self.winResult = self.checkForWinner()

		# if their are no more mechs in the queue, the turn has ended.  Reset the queue, and display a message about who won the turn.
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
			self.console.messageList.insert(0, "Red Team:  " + str(int(self.blueTeamDamage)) + " damage dealt")
			self.console.messageList.insert(0,  "Blue Team: " + str(int(self.redTeamDamage)) + " damage dealt")
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

		# return information about whether the game has ended or not.
		return gameState


	# deal damage to mechs that were hit during the round.
	def resolveDamage(self):
		'''
		applies damage dealt during the turn to all combatants simultaneously
		'''
		print "*** " + str(self.turnNumber - 1) + " ***"	# this just displays the turn number in the system console.  It just makes it easier to keep track, but you can ignore this.
		# for each mech on the red team, deal them damage.
		for mech in self.redTeamList:
			mech.health -= mech.damageTaken
			self.redTeamDamage += mech.damageTaken
			print mech.name, mech.damageTaken, mech.health		# show damage info in the system console for debugging purposes.  You can ignore this.

			# if the mech has no health left, kill it.
			if mech.health <= 0:
				mech.deathBlow = mech.damageTaken
				self.redTeamList = mech.death(self.redTeamList)

			# since damage was already applied, clear out the damage for the mech that turn
			mech.damageTaken = 0


		# this works exactly the same as it did for the red team.  See above for info about how this is working.
		for mech in self.blueTeamList:
			mech.health -= mech.damageTaken
			self.blueTeamDamage += mech.damageTaken
			print mech.name, mech.damageTaken, mech.health

			if mech.health <= 0:
				mech.deathBlow = mech.damageTaken
				self.blueTeamList = mech.death(self.blueTeamList)

			mech.damageTaken = 0






