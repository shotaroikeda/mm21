import game_constants

class Map(object):
	def __init__(self):
		self.teams = []
		self.nodes = []

	# Add a team and assign them a starting node
	def addTeam(self, teamId):
		if teamId in self.teams:
			raise Exception("teamId is already in teams.")
		self.teams.append(teamId)

	# Get all nodes of a given type (e.g. all ISPs)
	def getNodesOfType(self, nodeType):
		return [x for x in self.nodes if x.type == nodeType] # DOES NOT WORK PLZ FIX

	# Decrement the power of connected nodes
	# Will raise an exception if the required amount of power is not available
	def decrementPower(self, processing, networking):


	# decrementPower() recursive helper function
	def decrementPowerRecursor(self, processing, networking):

