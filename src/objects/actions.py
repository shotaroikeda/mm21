"""
Data-mutators for actions players can do (to the map, other players, and/or nodes)
"""


class AttemptToMultipleDDosException(Exception):
    pass


class AttemptToMultipleRootkitException(Exception):
    pass


# Node class used to model actions and their results
class ActionNode:

    # Raise an exception if resources are insufficient
    def requireResources(self, processingCost, networkingCost):
        map.decrementPower(self, self.processingCost, self.networkingCost)

    def doControl(self, playerId, multiplier):
        self.requireResources(multiplier, multiplier)
        if playerId == self.ownerId:
            for k in self.infiltration.iterkeys():
                self.infiltration[k] = max(self.infiltration[k] - multiplier, 0)
        else:
            self.infiltration[playerId] = self.infiltration.get(playerId, 0) + multiplier
            if self.infiltration[playerId] > 50:  # TODO change this number
                self.own(playerId)

    def doDDOS(self):
        if self.DDoSStatus == DDoSStatus.PENDING:
            raise AttemptToMultipleDDosException() 
        self.requireResources(self.totalPower / 5, self.totalPower / 5)
        self.DDoSStatus = DDoSStatus.PENDING

    def doUpgrade(self):
        self.requireResources(self.processing, self.networking)
        self.softwareLevel += 1

    def doClean(self):
        self.requireResources(100, 0)
        self.rootkitIds = []

    def doScan(self):
        self.requireResources(25, 0)
        return self.rootkitIds

    def doRootkit(self, playerId):
        if playerId in self.rootkitIds:
            raise AttemptToMultipleRootkitException("This player has a rootkit here already.")
        self.requireResources(self.totalPower / 5, self.totalPower / 5)
        self.rootkitIds.append(playerId)

    def doPortScan(self):
        self.requireResources(0, 500)
        return self
