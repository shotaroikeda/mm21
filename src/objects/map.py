"""
Holds data about the map
"""

import game_constants

class DuplicateTeamException(Exception):
	pass

class InsufficientPowerException(Exception):
	pass

class Map(object):
	def __init__(self):
		self.teams = []
		self.nodes = []
		self.nodesByID = {}

	# Add a team and assign them a starting node
	def addTeam(self, teamId):
		if teamId in self.teams:
			raise DuplicateTeamException("teamId is already in teams.")
		self.teams.append(teamId)

	# Get all nodes of a given type (e.g. all ISPs)
	def getNodesOfType(self, nodeType):
		return [x for x in self.nodes if x.type == nodeType] # DOES NOT WORK PLZ FIX

	# Decrement the power of connected nodes
	# Will raise an exception if the required amount of power is not available
	def decrementPower(self, startingNode, processing, networking):
		connectedNodes = set()
		getConnectedNodes(startingNode, connectedNodes, startingNode.ownerId)
		totalProcessing = 0
		totalNetworking = 0
		for node in connectedNodes:
			totalProcessing += node.remainingProcessing
			totalNetworking += node.remainingNetworking
		if totalProcessing < processing or totalNetworking < networking:
			raise InsufficientPowerException("networking = " + totalNetworking + ", processing = " + 
				totalProcessing + "\nNeeded networking = " + networking + ", processing = " + processing)
		for node in connectedNodes:
			if processing > node.remainingProcessing:
				processing -= node.remainingProcessing
				node.remainingProcessing = 0
			else:
				node.remainingProcessing -= processing
				processing = 0
			if networking > node.remainingNetworking:
				networking -= node.remainingNetworking
				node.remainingNetworking = 0
			else:
				node.remainingNetworking -= networking
				networking = 0

	# recursive function to add all connected nodes to the connectedNodes set
	def getConnectedNodes(self, startingNode, connectedNodes, ownerId):
		if startingNode.ownerId != ownerId or startingNode in connectedNodes:
			return
		connectedNodes.append(startingNode)
		for adjacent in startingNode.adjacentIds:
			getConnectedNodes(adjacent, connectedNodes, ownderId)
