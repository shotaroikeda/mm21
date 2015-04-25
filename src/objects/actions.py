"""
Data-mutators for actions players can do (to the map, other players, and/or nodes)
"""
class AttemptToMultipleDDosException(Exception)
    pass

class 

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
    if self.isDDOSed is True:
        raise AttemptToMultipleDDosException() # what should I put in here? 
    self.isDDOSed = True
    return


def doUpgrade(self):
    self.softwareLevel += 1
    return


def doClean(self):
    self.rootkitIds = []
    return


def doScan(self):
    return self.rootkitIds


def doRootkit(self, playerId):
    if playerId in self.rootkitIds:
        raise Exception("This player has a rootkit here already.")
    self.rootkitIds.append(playerId)
    return

# action called upon the entire map
def doPortScan(self):
	return self
