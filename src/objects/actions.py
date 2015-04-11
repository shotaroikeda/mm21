def doControl(self, playerId):
        if playerId == self.ownerId:
            for k in self.infiltration.iterkeys():
                self.infiltration[k] = max(self.infiltration[k] - 1, 0)
        else:
            self.infiltration[playerId] = self.infiltration.get(playerId, 0) + 1
            if self.infiltration[playerId] > 50:  # TODO change this number
                self.own(playerId)
        return

def doDDOS(self):
	self.isDDOSed = True
	return

def upgrade(self):
	self.softwareLevel += 1
	return

def clean(self):
	self.rootkitIds = []
	return

def scan(self):
	return self.rootkitIds

def rootkit(self, playerId):
	if playerId in self.rootkitIds:
		raise Exception("This player has a rootkit here already.")
	self.rootkitIds.append(playerId)
	return

def canMoveThrough(self, playerId):
	if playerId in self.rootkitIds:
		return True
	return self.ownerId == playerId

def own(self, playerId):
	if playerId == self.ownerId:
		raise Exception("This player owns this node already.")
	self.ownerId = playerId
	self.rootkitIds = []
	self.infiltration = []
	return
