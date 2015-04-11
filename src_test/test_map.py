import src.objects.map as emap
import pytest

#to run, must have pytest installed see: http://pytest.org/latest/getting-started.html
#to get the import statement to run correctly, you must run 
#<export PYTHONPATH=`pwd`> in the root directory

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
