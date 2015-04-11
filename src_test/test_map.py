import src.objects.map as emap
import pytest

def test_addTeam():
	_map = emap.Map()
	_map.addTeam(1)
	assert _map.teams[0] == 1

def test_addDupTeam():
	with pytest.raises(emap.DuplicateTeamException):
		_map = emap.Map()
		_map.addTeam(1)
		_map.addTeam(1)
		assert _map.teams[0] == 1
