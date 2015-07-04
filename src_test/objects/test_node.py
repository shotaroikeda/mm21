"""
Tests for the Node object
"""

from src.game_constants import *
from src.misc_constants import *
import json as JSON


"""
misc.
"""


# Test toPlayerDict
def test_toPlayerDict():

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _map.addPlayer(2)
    _node = _map.getPlayerNodes(1)

    # Check value correctness
    _returned = _node.toPlayerDict(False)
    assert _node.id == _returned["id"]
    assert _node.processing == _returned["processingPower"]
    assert _node.networking == _returned["networkingPower"]
    assert _node.ownerId == _returned["owner"]
    assert _node.softwareLevel == _returned["softwareLevel"]
    assert _node.isIPSed == _returned["isIPSed"]
    assert _node.infiltration == _returned["infiltration"]
    assert _node.nodetype == _returned["nodeType"]
    assert _node.DDoSed == _returned["isDDoSed"]
    assert sorted(_node.adjacentIds) == sorted(returned["adjacentIds"])
    assert sorted(_node.rootkits) == sorted(returned["rootkits"])
    self.rootkits if showRootkits else None

    # Check for rootkit hiding
    _node.isIPSed = False
    _node.targeterId = 2
    _node.doRootkit()
    assert _node.toPlayerDict(False)["rootkits"] is None
    assert _node.toPlayerDict(True)["rootkits"] = [2]


"""
decrementPower()
"""


# Test decrementPower with one node
def test_decrementPower_oneNode():

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Test all-at-once deduction
    _node.decrementPower(500)
    assert _node.remainingProcessing == 0
    assert _node.remainingNetworking == 0
    _map.resetAfterTurn()

    # Test ordering + multiple deductions
    _node.decrementPower(100, 400)
    assert _node.remainingProcessing == 400
    assert _node.remainingNetworking == 100
    _node.decrementPower(400, 100)
    assert _node.remainingProcessing == 0
    assert _node.remainingNetworking == 0
    _map.resetAfterTurn()

    # Test single over-deduction + "single power failure"
    # (No deduction should go through)
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(501, 501)
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(501, 500)
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(500, 501)
    assert _node.remainingProcessing == 500
    assert _node.remainingNetworking == 500

    # Test multiple over-deduction
    _node.decrementPower(499, 499)
    assert _node.remainingProcessing == 1
    assert _node.remainingNetworking == 1
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(2, 2)
    assert _node.remainingProcessing == 1
    assert _node.remainingNetworking == 1
    _map.resetAfterTurn()


# Test decrementPower with multiple nodes
def test_decrementPower_multiNodes():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Conquer all nodes adjacent to the base
    for n in _node.getAdacentNodes():
        n.own(1)
    _nodes = _map.getPlayerNodes(1)
    totalP = sum(x.processingPower for x in _nodes)
    totalN = sum(x.networkingPower for x in _nodes)

    # Test all-at-once deduction
    _node.decrementPower(totalP, totalN)
    for n in _nodes:
        assert n.remainingProcessing == 0
        assert n.remainingNetworking == 0
    _map.resetAfterTurn()

    # Test ordering + multiple deductions
    _node.decrementPower(totalP - 100, 100)
    assert sum(x.remainingProcessing for x in _nodes) == 100
    assert sum(x.remainingNetworking for x in _nodes) == totalN - 100
    _node.decrementPower(100, totalN - 100)
    for n in _nodes:
        assert n.remainingProcessing == 0
        assert n.remainingNetworking == 0
    _map.resetAfterTurn()

    # Test single over-deduction + "single power failure"
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(totalP + 1, totalN + 1)
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(totalP + 1, totalN)
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(totalP, totalN + 1)
    assert sum(x.remainingNetworking for x in _nodes) == totalP
    assert sum(x.remainingProcessing for x in _nodes) == totalN

    # Test multiple over-deduction
    _node.decrementPower(totalP - 1, totalN - 1)
    assert sum(x.remainingNetworking for x in _nodes) == 1
    assert sum(x.remainingProcessing for x in _nodes) == 1
    with pytest.raises(InsufficientPowerException):
        _node.decrementPower(2, 2)
    assert sum(x.remainingNetworking for x in _nodes) == 1
    assert sum(x.remainingProcessing for x in _nodes) == 1


# Test decrementPower with negative values
def test_decrementPower_negative():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Should raise an exception
    with pytest.raises(ValueError):
        _node.decrementPower(-1, 1)
    with pytest.raises(ValueError):
        _node.decrementPower(1, -1)
    assert _node.remainingProcessing == 500
    assert _node.remainingNetworking == 500


"""
getClusteredNodes()
"""


# Test one node
def test_getClusteredNodes_oneNode():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    assert sorted(_node.getClusteredNodes()) == sorted(_map.getPlayerNodes(1))


# Test one node cluster
def test_getClusteredNodes_oneCluster():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    for n in _node.getAdjacentNodes():
        n.own(1)

    assert sorted(_node.getClusteredNodes()) == sorted(_map.getPlayerNodes(1))


# Test two separate node clusters
def test_getClusteredNodes_twoClusters():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Find clusters
    _cluster1 = [_node]
    _cluster1.extend(_node.getAdjacentNodes())
    _cluster2 = [n for n in _map.nodes if n not in _cluster1]

    # Assign ownership (cluster 1 - blob based around initial base)
    for n in _node.getAdjacentNodes():
        n.own(1)

    # Determine "no man's land" between clusters 1 and 2
    _noMansLand = []
    for n in _cluster2:
        _noMansLand.extend(n.getAdjacentNodes)
    _noMansLand = list(set([x for x in _noMansLand if x.ownerId != 1]))

    # Assign ownership (cluster[s] 2+ - any nodes not connected directly to cluster 1)
    _cluster2 = [x for x in _cluster2 if x not in _noMansLand]
    for n in _cluster2:
        n.own(1)

    # Check cluster sizes
    assert len(_cluster1) > 1
    assert len(_cluster2) > 1

    # Check getClusteredNodes()' correctness
    assert sorted(_cluster1) == sorted(_node.getClusteredNodes())
    assert sorted(_cluster2) == sorted(_cluster2[0].getClusteredNodes())


# Test custom playerId specifier
def test_getClusteredNodes_customPlayerId():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Find clusters
    _cluster1 = [_node]
    _cluster1.extend(_node.getAdjacentNodes())
    _cluster2 = [n for n in _map.nodes if n not in _cluster1]

    # Assign ownership (cluster 1 - blob based around initial base)
    for n in _node.getAdjacentNodes():
        n.own(1)

    # Make sure cluster shows up correctly depending on player ID
    assert sorted(_node.getClusteredNodes()) == sorted(_map.getPlayerNodes(1))
    assert len(_node.getClusteredNodes(2)) == 0


"""
getVisibleNodes()
"""


# Test one node
def test_getVisibleNodes_oneNode():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    _expected = [_node].extend(_node.getAdjacentNodes())
    assert sorted(_expected) == sorted(_node.getVisibleNodes())


# Test one node cluster
def test_getVisibleNodes_oneCluster():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)

    # Construct cluster
    _node = _map.getPlayerNodes(1)[0]
    for n in _node.getAdjacentNodes():
        n.own(1)

    # Determine expected answer
    _expected = [_node].extend(_node.getAdjacentNodes())
    for n in _node.getAdjacentNodes():
        _expected.extend(n.getAdjacentNodes())
    _expected = list(set(_expected))

    assert sorted(_expected) == sorted(_node.getVisibleNodes())


# Test two separate node clusters
def test_getVisibleNodes_twoClusters():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Find clusters
    _cluster1 = [_node]
    _cluster1.extend(_node.getAdjacentNodes())
    _cluster2 = [n for n in _map.nodes if n not in _cluster1]

    # Assign ownership (cluster 1 - blob based around initial base)
    for n in _node.getAdjacentNodes():
        n.own(1)

    # Determine "no man's land" between clusters 1 and 2
    _noMansLand = []
    for n in _cluster2:
        _noMansLand.extend(n.getAdjacentNodes)
    _noMansLand = list(set([x for x in _noMansLand if x.ownerId != 1]))

    # Assign ownership (cluster[s] 2+ - any nodes not connected directly to cluster 1)
    _cluster2 = [x for x in _cluster2 if x not in _noMansLand]
    for n in _cluster2:
        n.own(1)

    # Check cluster sizes
    assert len(_cluster1) > 1
    assert len(_cluster2) > 1

    # Add visible nodes to clusters
    for n in _cluster1:
        _cluster1.extend(n.getAdjacentNodes())
    for n in _cluster2:
        _cluster2.extend(n.getAdjacentNodes())
    _cluster1 = list(set(_cluster1))
    _cluster2 = list(set(_cluster2))

    # Check getVisibleNodes()' correctness
    assert sorted(_cluster1) == sorted(_node.getVisibleNodes())
    assert sorted(_cluster2) == sorted(_cluster2[0].getVisibleNodes())


# Test custom playerId specifier
def test_getVisibleNodes_customPlayerId():
    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    _expected = [_node].extend(_node.getAdjacentNodes())
    assert len(_node.getVisibleNodes(2)) == 0
    assert sorted(_expected) == sorted(_node.getVisibleNodes())


# Test two nodes connected by a rootkit chain (1 cluster)
def test_getVisibleNodes_rootkitChain():

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)

    # Build cluster
    _node = _map.getPlayerNodes(1)[0]
    for n in _node.getAdjacentNodes():
        n.rootkitIds.append(1)

    # Determine expected answer
    _expected = [_node].extend(_node.getAdjacentNodes())
    for n in _node.getAdjacentNodes():
        _expected.extend(n.getAdjacentNodes())
    _expected = list(set(_expected))

    assert sorted(_expected) == sorted(_node.getVisibleNodes())


# Test two nodes not connected by a rootkit chain (2 clusters)
def test_getVisibleNodes_severedRootkitChain():

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Find clusters
    _cluster1 = [_node]
    _cluster1.extend(_node.getAdjacentNodes())
    _cluster2 = [n for n in _map.nodes if n not in _cluster1]

    # Assign rootkits (cluster 1 - blob based around initial base)
    for n in _node.getAdjacentNodes():
        n.rootkitIds.append(1)

    # Determine "no man's land" between clusters 1 and 2
    _noMansLand = []
    for n in _cluster2:
        _noMansLand.extend(n.getAdjacentNodes)
    _noMansLand = list(set([x for x in _noMansLand if x.ownerId != 1]))

    # Assign ownership (cluster[s] 2+ - any nodes not connected directly to cluster 1)
    _cluster2 = [x for x in _cluster2 if x not in _noMansLand]
    for n in _cluster2:
        n.rootkitIds.append(1)

    # Check cluster sizes
    assert len(_cluster1) > 1
    assert len(_cluster2) > 1

    # Add visible nodes to clusters
    for n in _cluster1:
        _cluster1.extend(n.getAdjacentNodes())
    for n in _cluster2:
        _cluster2.extend(n.getAdjacentNodes())
    _cluster1 = list(set(_cluster1))
    _cluster2 = list(set(_cluster2))

    # Check getVisibleNodes()' correctness
    assert sorted(_cluster1) == sorted(_node.getVisibleNodes())
    assert sorted(_cluster2) == sorted(_cluster2[0].getVisibleNodes())


"""
more misc.
"""


# Test canMoveThrough
def test_canMoveThrough():

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Test unowned node
    _unownedNode = _node.getAdjacentNodes()[0]
    assert _unownedNode.canMoveThrough(1) is False

    # Test owned node
    assert _node.canMoveThrough(1) is True

    # Test rootkitted node
    _unownedNode.rootkitIds.append(1)
    assert _node.canMoveThrough(1) is True

    # Test custom playerID specifier
    assert _node.canMoveThrough(2) is False


# Test own
def test_own(self, playerId):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    # Test owning an unowned node
    _unownedNode = _node.getAdjacentNodes()[0]
    _unownedNode.own(1)
    assert _unownedNode.ownerId == 1

    # Test that owning an already-owned node throws an exception
    with pytest.raises(AlreadyOwnedException):
        _node.own(1)

    # Test resetting of isIPSed/rootkits/infiltration
    _unownedNode.own(0)
    assert _unownedNode.ownerId == 0
    _unownedNode.isIPSed = True
    _unownedNode.rootkitIds.add(1)
    _unownedNode.infiltration[1] = 999
    _unownedNode.own(1)
    assert _unownedNode.isIPSed is False
    assert len(_unownedNode.rootkitIds) == 0
    assert _unownedNode.infiltration[1] == 0


"""
Per-node action criteria
"""


# Test requireNotDDoSed
def test_requireNotDDoSed(self, actionName):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    self.requireNotDDoSed("")
    self.DDoSed = True
    with pytest.raises(NodeIsDDoSedException):
        self.requireNotDDoSed("")


# Test requireOwned
def test_requireOwned(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    _node.requireOwned()
    with pytest.raises(ActionOwnershipException):
        _node.getAdjacentNodes[0].requireOwned()


# Test requireNotOwned
def test_requireNotOwned(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    _node.getAdjacentNodes[0].requireNotOwned()
    with pytest.raises(ActionOwnershipException):
        _node.requireNotOwned()


# Test requireNotIPSed
def test_requireNotIPSed(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    _node.requireNotIPSed()
    _node.isIPSed = True
    with pytest.raises(IpsPreventsActionException):
        node.requireNotIPSed()


"""
Player actions
"""


# Test doControl in attacking mode
def test_doControl_attack(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _map.addPlayer(2)
    _node = _map.getPlayerNodes(1)[0]

    _target = node.getAdjacentNodes()[0]
    _target.own(2)
    _target.targeterId = 1

    # Test attacking without multiplier
    assert _target.infiltration[1] == 0
    _target.doControl()
    assert _target.infiltration[1] == 1

    # Test attacking with multiplier
    _target.doControl(9)
    assert _target.infiltration[1] == 10


# Test doControl in healing mode
def test_doControl_heal():

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _map.addPlayer(2)
    _node = _map.getPlayerNodes(1)[0]

    _target = node.getAdjacentNodes()[0]
    _target.own(2)
    _target.targeterId = 1
    _target.doControl(5)
    assert _target.infiltration[1] == 5

    # Test healing a damaged node without multiplier
    _target.targeterId = 2
    _target.doControl()
    assert _target.infiltration[1] == 4

    # Test overhealing a damaged node with multiplier
    _target.doControl(5)
    assert _target.infiltration[1] == 0

    # Test overhealing a fully-healed node without multiplier
    _target.doControl()
    assert _target.infiltration[1] == 0


# Player action to DDOS a node
def test_doDDoS(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    _node.doDDoS()
    assert self.DDoSPending is True
    _map.resetAfterTurn()
    assert self.DDoSed is True
    assert self.remainingProcessing = 0
    assert self.remainingNetworking = 0


# Player action to upgrade a node's Software Level
def test_doUpgrade(self):

    # TODO Figure out what "upgrade" is going to look like gameplay-wise
    pass


# Player action to clean a node of rootkits
def test_doClean(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _map.addPlayer(2)
    _node = _map.getPlayerNodes(1)[0]

    _node.rootkitIds.append(2)
    _node.clean()
    assert len(_node.rootkitIds) == 0


# Player action to scan a node for rootkits
def test_doScan(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _map.addPlayer(2)
    _node = _map.getPlayerNodes(1)[0]

    assert len(_node.doScan()) == 0
    _node.rootkitIds.append(2)
    assert len(_node.doScan()) == 1
    _node.clean()
    assert len(_node.doScan()) == 0


# Player action to add a rootkit to a node
def test_doRootkit(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    _target = _node.getAdjacentNodes()[0]
    assert len(_target.rootkitIds) == 0
    _target.targeterId = 1
    _target.doRootkit()
    assert target.rootkitIds == [1]


# Player action to do a port scan
def test_doPortScan(self):

    _map = GameMap(misc_constants.mapFile)
    _map.addPlayer(1)
    _node = _map.getPlayerNodes(1)[0]

    assert len(_map.portScans) == 0
    _node.targeterId = 1
    _node.portScan()
    assert _map.portScans == [1]
    _map.resetAfterTurn()
    assert len(_map.portScans) == 0
