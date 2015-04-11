"""
Holds data about a specific player
"""

import game_constants.py
class Player(object):
	def __init__(self, id, name, IPSNode):
		#int
		self.id = id;
		self.IPSNode = IPSNode;
		#string
		self.name = name;
