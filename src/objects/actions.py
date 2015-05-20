"""
Data-mutators for actions players can do (to the map, other players, and/or nodes)
"""


class AttemptToMultipleDDosException(Exception):
    pass


class AttemptToMultipleRootkitException(Exception):
    pass


@costs(multiplier, multiplier)
def doControl(self, playerId, multiplier):
    if playerId == self.ownerId:
        for k in self.infiltration.iterkeys():
            self.infiltration[k] = max(self.infiltration[k] - multiplier, 0)
    else:
        self.infiltration[playerId] = self.infiltration.get(playerId, 0) + multiplier
        if self.infiltration[playerId] > 50:  # TODO change this number
            self.own(playerId)
    return


@costs(self.totalPower / 5, self.totalPower / 5)
def doDDOS(self):
    if self.DDoSStatus == DDoSStatus.PENDING:
        raise AttemptToMultipleDDosException()
    self.DDoSStatus = DDoSStatus.PENDING


@costs(self.processing, self.networking)
def doUpgrade(self):
    self.softwareLevel += 1


@costs(100, 0)
def doClean(self):
    self.rootkitIds = []


@costs(25, 0)
def doScan(self):
    return self.rootkitIds


@costs(self.totalPower / 5, self.totalPower / 5)
def doRootkit(self, playerId):
    if playerId in self.rootkitIds:
        raise AttemptToMultipleRootkitException("This player has a rootkit here already.")
    self.rootkitIds.append(playerId)


@costs(0, 500)
def doPortScan(self):
    return self
