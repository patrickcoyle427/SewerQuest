'''
This contains all variables needed for the SewerQuest main file
to navigate the game. It's not meant to be ran by itself.
'''

coordinates = {
    
    'northsouth': 0,
    'eastwest': 0

    }
#These are the coordinates that the game uses to figure out what room
#hould be loaded.

rooms = {
        
    "0,0": 'north0east0()',
    "1,0": 'north1east0()',
    "0,1": 'north0east1()',
    "1,1": 'north1east1()',
    "2,1": 'north2east1()',
    "1,2": 'north1east2()',
    "2,2": 'north2east2()',
    "2,0": 'north2east0()',
    "0,2": 'north0east2()',
    "-1,0": 'south1east0()',
    "-2,0": 'south2east0()',
    "0,-1": 'north0west1()',
    "0,-2": 'north0west2()',
    "1,-1": 'north1west1()',
    "1,-2": 'north1west2()',
    "2,-1": 'north2west1()',
    "2,-2": 'north2west2()',
    "-1,1": 'south1east1()',
    "-1,2": 'south1east2()',
    "-2,1": 'south2east1()',
    "-2,2": 'south2east2()',
    "-1,-1": 'south1west1()',
    "-2,-1": 'south2west1()',
    "-1,-2": 'south1west2()',
    "-2,-2": 'south2west2()'
    
    }

#Dict that prompt() uses to determine which room should be loaded

visited_rooms = {
    
    "0,0": False,
    "1,0": False,
    "0,1": False,
    "1,1": False,
    "2,1": False,
    "1,2": False,
    "2,2": False,
    "2,0": False,
    "0,2": False,
    "-1,0": False,
    "-2,0": False,
    "0,-1": False,
    "0,-2": False,
    "1,-1": False,
    "1,-2": False,
    "2,-1": False,
    "2,-2": False,
    "-1,1": False,
    "-1,2": False,
    "-2,1": False,
    "-2,2": False,
    "-1,-1": False,
    "-2,-1": False,
    "-1,-2": False,
    "-2,-2": False
    
    }

#Visited rooms are rooms the user has already been to. If its set to false,
#the room runs as normal. When its true, the game gives a shortened version
#of the room text and makes it so the user won't have to replay any puzzles.

corner_cases = {
    
    'load': False,
    'name': "AAA",
    'count': 0,
    'jailtime': False
    
    }

#A few special cases.
# load is only for when the game loads a save file. Load = True makes it so
# the game won't load the first room, only the one that was loaded.
# Name and Count are both for one puzzle that has an arcade and I wanted to
# save the high scores.
# jailtime is for one room as well. If you can be thrown into jail it will be
# True so that every time you enter one particular room you will be taken
# back to jail.

if __name__ == '__main__':
    
    print('This file is meant to support the main game, SewerQuest.py.')
    print('Please open that instead.')
