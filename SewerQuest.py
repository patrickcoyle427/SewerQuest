#!/usr/bin/python3

'''
# SewerQuest.py - An old school text adventure game written by Patrick Coyle.
'''

from random import randint
import sys, pickle, os, time
from navigation import *

#Randint is used in room South2East2 to teleport the player to a random room.
#Sys is used to help exit.
#
#Pickle is used for saving the game. This game isn't saving any sensitive information
#and pickle is easy to use.
#
#Os is used in saving as well, to get the current working directory path so the game
#saves and loads properly.
#
#Time is used in room south2east2 to give the player some time to read text before being sent to a
#random room.
#
#navigation is a .py file I wrote to go along with this game that contains dicts that hold
#game information.

def play():

    if corner_cases['load'] == False:
            
        north0east0()
        #This loads the first room if you're not loading a save. The load_save function below handles
        #putting you into the first room, and then sets load to True to skip the first room.

    while True:
        
        current_room = prompt()
        exec(current_room)

        #Prompt is where the user enters their direction, and that will
        #return the function that corresponds to the room the player is entering.
 

def prompt():

    north = ('n', 'N', 'north', 'North', 'NORTH')
    south = ('s', 'S', 'south', 'South', 'SOUTH')
    east = ('e', 'E', 'east', 'East', 'EAST')
    west = ('w', 'W', 'west', 'West', 'WEST')
    replay = ('r', 'R', 'replay', 'Replay', 'REPLAY')
    quit_game = ('q', 'Q', 'quit', 'Quit', 'QUIT')

    while True:

        print("\nWhich direction would you like to travel?")
        
        try:
            direction = input("> ")

            if direction in north:

                if coordinates['northsouth'] == 2:
                        
                    print("Sorry, you can't go further in that direction. Try a different one.")

                else:
                        
                    coordinates['northsouth'] += 1
                    
                    break
                    
                    #When you enter a command, the game will check to see if it isn't going to make a coordinate
                    #greater than 2 or -2. If this passes, it'll increment the number, then break the loop.

            elif direction in south:

                if coordinates['northsouth'] == -2:
                        
                    print("Sorry, you can't go further in that direction. Try a different one.")

                else:
                        
                    coordinates['northsouth'] -= 1
                    
                    break

            elif direction in east:

                if coordinates['eastwest'] == 2:
                    
                    print("Sorry, you can't go further in that direction. Try a different one.")

                else:
                        
                    coordinates['eastwest'] += 1
                    
                    break

            elif direction in west:

                if coordinates['eastwest'] == -2:
                        
                    print("Sorry, you can't go further in that direction. Try a different one.")

                else:
                        
                    coordinates['eastwest'] -= 1
                    break

            elif direction in replay:
                    
                #This allows you to replay the text of a room before it was visited.
                
                room_coordinate = "{},{}".format(coordinates['northsouth'], coordinates['eastwest'])
                next_room = rooms[room_coordinate]
                change_room_status()
                                          
                #This sets the room you're visiting back to False so that you can see
                #The opening text again
                                    
                break

            elif direction in quit_game:

                yes = ('y', 'Y', 'yes', 'Yes', 'YES')
                no = ('n', 'N', 'no', 'No', 'NO')
                                    
                print("Would you like to save the game?")

                try:
                        
                    while True:
                            
                        saving = input("> ")

                        if saving in yes:
                                
                            save_game()
                            
                            break
                            #This saves and exits the game. Saving is used with pickle and I'll
                            #go into more detail about it below where the function is.

                        elif saving in no:

                            break

                        else:

                            print("Sorry, what was that again?")

                    print("Exiting game...")
                            
                    sys.exit(0)

                except KeyboardInterrupt:
                    print("Exiting game...")
                    sys.exit(0)

            else:
                print("\nSorry, that's not a direction. Directions are North, South, East, or West. You may")
                print("also type replay to read the room introduction again, or quit to exit the game.")

        except KeyboardInterrupt:
            print("\nType quit to save and close the game.")

            
    if direction not in replay:
            
        room_coordinate = "{},{}".format(coordinates['northsouth'], coordinates['eastwest'])
        next_room = rooms[room_coordinate]
        #This is where the game checks the rooms dictionary and then sets
        #that result to the room to be loaded next.
        
    return next_room
    #next room is returned to the engine so that it can load the room you are entering.
    #Once that room is finished, prompt will be loaded again so that you can navigate
    #to another room by typing a command.

def test_mode():
    
    val1 = int(input("Enter a north/south coordinate: "))
    val2 = int(input("Enter an east/west coordinate: "))
    #This will be the first coordinate for rooms
    #and this is the second.
    #North and East coordinates are positive integers
    #South and West are negative integers
                                          
    coordinates['northsouth'] = val1
    coordinates['eastwest'] = val2

    #These two set the map coordinates so you'll be in the correct location
    #When you leave the loaded room
                                          
    room_coordinate = "{},{}".format(val1, val2)
    #This is setting up the string that will be fed to the dictionary
                                          
    load_room = rooms[room_coordinate]
    #This sets load_room up to have the play function load the correct room.

    return load_room                

def save_game():

    print("Saving game...")

    corner_cases['load'] = True

    where_to_save = os.getcwd()
    
    save_file = open('{}\\savefile.dat'.format(where_to_save), 'wb')
    #sets save to open savefile.dat in write binary mode, and will create it if it doesn't exist.
                                          
    pickle.dump((coordinates, visited_rooms, corner_cases), save_file, protocol = 0)
    #Pickle saves the coordinates, visted_rooms, and corner_cases dicts
    #into a file called savefile.dat. Save_file is a variable that was
    #set in the previous line. Protocol zero saves the info in ASCII format
    #This information doesn't need to be encrypted or secured, so I went with
    #the simplest way to save it.

    save_file.close()

def load_save():

    load_success = False

    load_from = os.getcwd()

    yes = ('y', 'Y', 'yes', 'Yes', 'YES')
    no = ('n', 'N', 'no', 'No', 'NO')

    while True:
                                              
        print("Load saved game?")
        print("Type yes to load your save, or no to return to the main menu.")

        loading = input("> ")

        if loading in yes:

            try:

                #handles the error in the case of no save file existing.
            
                with open('{}\\savefile.dat'.format(load_from), 'rb') as save_file:

                    #Sets save to open savefile.dat in read binary mode
                               
                    player_coordinates, player_visited_rooms, player_corner_cases = pickle.load(save_file)
                    #This loads the info back into the game

                    for k, v in player_coordinates.items():

                        coordinates[k] = v

                    for k, v in player_visited_rooms.items():

                        visited_rooms[k] = v

                    for k, v in player_corner_cases.items():

                        corner_cases[k] = v

                    save_file.close()

                    load_success = True
                                                      
                    room_coordinate = "{},{}".format(coordinates['northsouth'], coordinates['eastwest'])
                    load_room = rooms[room_coordinate]
                    #Sets room to a string that the dict can read
                    #The dict is read and then the result is set to load_room
                    
                    exec('{}'.format(load_room))
                    #Load room is returned to the loop in and the game will continue as normal.
                    break

            except IOError:
                
                print('\n ERROR! Could not read save file! Returning you to the main menu...\n')
                
                break

        elif loading in no:
            
            print('')
            break

        else:

            print('What was that? Please type it again!\n')

    return load_success
                                          

def start_game():

    #This is the main menu. You're able to start the game, load, exit, or run test mode

    start = ('s', 'S', 'start', 'Start', 'START')
    load = ('l', 'L', 'load', 'Load', 'LOAD')
    exit_game = ('e', 'E' 'exit', 'Exit', 'EXIT')

    while True:
            
        print("Sewer Quest")
        print("START, LOAD, or EXIT?")
        
        game = input("> ")
        
        try:
                
            if game in start:
                print("Starting game...")
                
                break
                #if this loop wasn't broken, when the player finished the game it would come back to here.

            elif game in load:

                game_loaded = load_save()

                if game_loaded == True:
                    
                    break

                else:

                    continue

            elif game in exit_game:
                    
                print("Thanks for playing!")
                
                sys.exit(0)

            elif game == "test mode":
                    
                corner_cases['load'] = True
                
                current_room = test_mode()
                
                exec('{}'.format(current_room))
                
                break

            else:
                    
                print("What was that? Please type it again!\n")

        except KeyboardInterrupt:
                
            print("\nThanks for playing!")
            
            sys.exit(0)


def check_visited_status():
    
    to_check = '{},{}'.format(coordinates['northsouth'], coordinates['eastwest'])

    return visited_rooms[to_check]

def change_room_status():

    to_change = '{},{}'.format(coordinates['northsouth'], coordinates['eastwest'])

    if check_visited_status() == False:
    
        visited_rooms[to_change] = True

    else:
            
        visited_rooms[to_change] = False

def north0east0():

    if check_visited_status() == False:
            
        print("\nYou wake up in a dark cave. Light is shining from above.")
        print("You can see that you fell into what you believe to be a.")
        print("sewer? It sure smells like one. Yeesh. It looks like it's")
        print("possible to leave somehow though. You think it would be a")
        print("good idea to get a piece of paper and a pen to draw a map")
        print("with, as well as your trusty flashlight and compass (good thing")
        print("you were walking home from a night class last night, huh?)")
        print("and start to get your bearings. As you shine your flashlight")
        print("around, it appears that you can travel North, South, East or West")
        
        change_room_status()

    else:
            
        print("\nYou are back where you started. You try in vain to jump")
        print("up to the hole you fell through. Looks like")
        print("you'll just have to press on.")

def north1east0():

    if check_visited_status() == False:
            
        print("\nA voice yells out \"WHO GOES THERE?\" in the distance. You")
        print("quietly approach this strange sewer man. He stands there,")
        print("eyeing you up and down, taking you in. You do the same and")
        print("take notice of his raggy clothes, big bushy beard, weirdly")
        print("patched together pointy hat, and his non-threatening stance.")
        print("\"What are you doing down here young man? This is no place")
        print("for surface dwellers.\" You explain to him your sitation...")
        print("\"I see... well good luck to you boy. I might live down here ")
        print("but even I don\'t want to be here.\"You decide to see if you")
        print("can ask him some questions about where you are.")
        
        change_room_status()

    else:
            
        print("\nYou are once again greated by the sewer wizard. You decide")
        print("to ask some more questions.")

    while True:
            
        print("\nHere's what you can ask:")
        print("1. Where exactly am I?")
        print("2. Who are you?")
        print("3. How can I get out of here?")
        print("4. Alright thanks for the info. I'll be on my way now.\n")
        
        try:
                
            question = input("What would you like to ask? ")
            
            #I made the user enter numbers instead of typing an action because I thought
            #it would make picking an action clearer and faster.
            
            if question == '1':
                    
                print("\nYou ask the man \"Where exactly am I?\"")
                print("\"You are in sewerland young man. The land of the sewer people.\"")
                print("\"Tread carefully down here. Danger awaits at every turn!\"")
                print("Well... that was ominous. Guess you had better be careful.")

            elif question == '2':
                    
                print("\nYou ask the man \"Who are you?\"")
                print("\"I am Sewer Merlin, the Sewer Wizard!!!\" the sewer man says.")
                print("As you examine his outfit closer, you see that he indeed looks")
                print("like a wizard. That pointy hat should have been a dead giveaway.")
                print("You don't think you need to learn anything else about Sewer Merlin")

            elif question == '3':
                    
                print("\nYou ask the man \"How can I get out of here?\"")
                print("\"I've heard tales that in one of the corners of the sewer this")
                print("is a pathway to the surface world.\" He says with a look of whimsy")
                print("in his eye. \"But be warned young man, a strange witch guards the")
                print("eastern corner, there are sewer mutants everywhere as well! Danger")
                print("awaits at eveeeeerry turn!\" Well I suppose that answers your question.")
                print("Look for the corners...")

            elif question == '4':
                    
                print("\n\"Alright, thanks for the info.\" You say to the sewer man.")
                print("You're not really sure how much you've actually learned, but")
                print("you might as well see if any of what he says helps.")
                print("You wave goodbye, leaving a little more confused than when you left.")
                
                break

            elif question == '5':
                    
                print("\nYou ask the sewer wizard \"Can you cast a sewer spell on me?\"")
                print("\"Sure thing young man!\" The sewer wizard says enthusiastically.")
                print("He begins to chant...")
                print("\"109... 109... 109...\" over and over.")
                print("You feel much luckier! Maybe that actually did something?")

            else:
                    
                print("The sewer man may be \"wise\", but he didn\'t understand that. Try again.")

        except KeyboardInterrupt:
                
            print("Hey! That wasn't a number! This guy only understands what you want if it's a number!")

def north0east1():

    if check_visited_status() == False:
            
        print("\nYou arrive east of where you fell. A tall sewer woman")
        print("with cracked glasses and her brown hair in a bun")
        print("sees you there. \"You there? what are you doing here.")
        print("You know there are sewer mutants around, right? It's")
        print("dangerous around these parts. I run the sign library to the")
        print("east of here. If you don't know what you're doing here, maybe")
        print("you could learn there. It is safe at least. If you")
        print("are really strapped for how to get out of here, there's")
        print("a wise old sewer man who might be able help you. Some say")
        print("he helped build these tunnels.\" she says confidently.")
        print("You thank her for the advice and decide where to go next.")
        
        change_room_status()

    else:
            
        print("\nYou arrive back where you met the librarian. Her library")
        print("was east of where you are now. The crisp sewer air reminds")
        print("you of your conversation with her. You shoud watch out for")
        print("sewer mutants and look for the wise sewer man!")

def north1east1():

    def back_to_zero(number):
            
        if number > 12:
                
            number -= 12
            
            return number
            #This is used in the puzzle below. You're manipulating clocks so I don't want them to above 12.

        else:
                
            return number
    
    a = 0
    b = 0
    c = 0
    triple = False

    if check_visited_status() == False:
            
        print("\nYou enter a lavish sewer room. \"ARCADE ROOM\" it says in big bright")
        print("letters. Awesome! Finally something fun to do! You're not sure why")
        print("there isn't anyone else here, but hey, maybe it's early in the morning")
        print("or something like that. You sit down at a strange looking machine.")
        print("You see all the doors lock behind you! Oh crap, it's a sewer trap!")
        print("A robot lowers from the sewer celing and tells you what's up: ")
        print("\n\"WELCOME USER TO OUR SEWER ARCADE PUZZLE TESTING FACILITY.")
        print("YOU HAVE BEEN SELECTED TO TEST OUR MATCH THREE NUMBERS PUZZLE GAME!")
        print("HOW LUCKY FOR YOU! YOU WILL BE PLAYING THIS GAME UNTIL YOU MATCH NUMBERS!")
        print("ANY 3 NON-0 NUMBERS WILL DO! HAVE FUN!!!!\"")
        print("\n Well, this blows. You're trapped in here until you beat the game.")
        print("You only win when all three clocks in front of you display the same")
        print("number. If it goes over 12, it will reset back to 0 and continue from")
        print("there. The clocks will increment depending on what you press.")
        #I'm sure there are a bunch of solutions to this puzzle, but there are two really easy ones.
        #The first one is to just hit A 12 times and they all end up being the same number eventually
        #The other is to just type no to bypass the puzzle entirely.

        while triple != True:
                
            print("\nPressing A increments all clocks by 5, 1, and 2 respectively.")
            print("Pressing B increments clocks 2 and 3 by 1 and 2.")
            print("Pressing C incremements clock 3 by 2.")
                                          
            try:
                    
                spin = input("Press which button? ")

                if spin == "a" or spin == "A":
                        
                    a += 5
                    b += 1
                    c += 2
                    a = back_to_zero(a)
                    b = back_to_zero(b)
                    c = back_to_zero(c)
                    #eveytime you press a button the game will check to see if it's above 12.
                                          
                    print("A = ", a)
                    print("B = ", b)
                    print("C = ", c)
                    Rooms.count += 1

                elif spin == "b" or spin == "B":
                        
                    b += 1
                    c += 2
                    b = back_to_zero(b)
                    c = back_to_zero(c)

                    print("A = ", a)
                    print("B = ", b)
                    print("C = ", c)
                    
                    Rooms.count += 1

                elif spin == "c" or spin == "C":
                        
                    c += 2
                    c = back_to_zero(c)

                    print ("A = ", a)
                    print ("B = ", b)
                    print ("C = ", c)
                    
                    Rooms.count += 1

                elif spin == "no":
                        
                    print ("\nSECRET CODE WHOAAAA!!!")
                    print ("YOU INSTANTLY WIN!")
                    
                    triple = True

                else:
                        
                    print("That definitely wasn't a button you pressed... hopefully it doesn't matter.")

            except KeyboardInterrupt:
                    
                print("You decide to give up on this puzzle.")
                print("You are dead.")
                print("\n\n\t\tTHE END\n\n")

            solution_test = '{}{}{}'.format(a, b, c)

            solution = ('111', '222', '333', '444', '555', '666', '777', '888', '999', '101010', '111111', '121212')

            if solution_test in solution:
                    
                triple = True

        print("\nA horn blasts while confetti shoots out of the arcade machine.")
        print("It appears that you have won.")
        print("It took you only {} button presses! A new high score!".format(rooms.count))
        
        try:
                
            corner_cases['name'] = input("What are you initials? ").upper()

        except KeyboardInterrupt:
                
            print("You just mash the A button. You're no fun.")

        print("\n\t\tHIGH SCORES")
        print("\n\t1. {}\t{}".format(corner_cases['name'][:3], corner_cases['count']))
        #The [:3] is so the first 3 letters are displayed. It's an arcade machine after all.
        print("\t2. HBJ\t{}".format(corner_cases['count'] + 2))
        print("\t3. BUT\t{}".format(corner_cases['count'] + 5))
        print("\nLooks like you've been immortalized with the greats.")
        print("Well, while that was a \"fun\" distraction, you feel like it's time you left this \"arcade\".")
        
        change_room_status()

    else:

        print("\nYou arrive back at the arcade. Since you solved the puzzle test it no longer tries")
        print("to trap you, and, you can still see your high score!")
        print("\n\t\tHIGH SCORES")
        print("\n\t1. {}\t{}".format(corner_cases['name'][:3], corner_cases['count']))
        print("\t2. HBJ\t{}".format(corner_cases['count'] + 2))
        print("\t3. BUT\t{}".format(corner_cases['count'] + 5))

def north2east1():
    
    i = 0

    if check_visited_status() == False:
            
        print("\nAs you explore further and further into the sewers, you come")
        print("across a corridor that smells far worse than any you have walked")
        print("down so far. Smells like a mix between cooked sewage and clothes")
        print("washed in stagnant pond water. You can see in the distance a small")
        print("fire sitting below a large cauldron. A shadowy figure sits beside")
        print("it. As you approach, you see that it is an old, smelly, wrinkly, woman.")
        print("\nWHAT ARE YOU DOING HERE?!?!?")
        print("You try to explain that you are just trying to get home and mean")
        print("no harm, but...")
        print("I DON'T BELIEVE YOU!!! THE LAST PERSON WHO I LET BY STOLE MY")
        print("FAVORITE MOLD CARPET! I'LL BELIEVE YOU IF YOU CAN TELL ME MY")
        print("FAVORITE NUMBER!!! THAT'S THE ONLY WAY I'LL LET YOU PASS!!!!")
        print("I'LL EVEN GIVE YOU THREE CHANCES TO TELL ME IT BECAUSE I'M SO NICE.")
        print("I WON'T BE SO NICE IF YOU DON'T KNOW IT THOUGH!!! YOU WILL")
        print("DIIIIIIIIIIIE!!!")

        while i < 3:
                
            try:
                    
                number = input("\nWHAT IS MY FAVORITE NUMBER!!? ")

                if number == '109':
                        
                    print("\nWOW!!! I REALLY CAN TRUST YOU!!! YOU'RE FREE TO GO YOUNG PERSON!!!\n")
                    print("You decide you probably should leave quickly before she changes her mind.")
                    print("Something catches your eye to the east... maybe you should check it out?")
                    
                    change_room_status()
                    
                    break
                    
                else:
                    i += 1
                    
                    print("\nWROOOOOONG YOU DUMMY!!!")
                    
                    if i == 1:
                            
                        print("THAT WAS {} GUESS!!!\n".format(i))
                        
                        print("YOU HAVE {} GUESSES LEFT NOW!!!".format(3-i))
                    else:
                            
                        print("THAT WAS {} GUESSES!\n".format(i))
                        
                        if i == 2:
                                
                            print("YOU HAVE {} GUESS LEFT NOW!!!".format(3-i))
                            
                        else:
                                
                            print("YOU HAVE {} GUESSES LEFT NOW!!!".format(3-i))

                    if i == 3:
                            
                        print("NOW YOU DIE!!!")
                        print("\nThe witch starts wiggling her fingers around menacingly.")
                        print("All of a sudden... BOOM!!! You explode! Looks like you won't.")
                        print("Be going home...")
                        print("\n\n\t\tTHE END\n\n")
                        
                        sys.exit(0)

            except KeyboardInterrupt:
                    
                print("Hey, c'mon dude. She's literally trying to kill you and you're")
                print("Hitting random buttons? Just tell her a number!")

    else:
            
        print("\nYou return to the corridor with the old, smelly, sewer witch.")
        print("Instead of trying to kill you this time, she kindly waves to you!")
        print("You wave back, making sure to match her politeness. Looks like now")
        print("that she can trust you, you can come and go as you please!")
        print("Not sure why you're still exploring though, the exit to go home is")
        print("literally to the east. Go and win the game!")

def north1east2():
        
    print("\nOH NO IT'S A BOTTOMLESS PIT. YOU FALL IN IT AN DIE.")
    print("\n\n\t\tTHE END\n\n")
    
    sys.exit(0)
    #There's a few rooms where you die right away. They only exist to make walls
    #that the player can't pass. This one blocks the path to the end of the game.

def north2east2():
        
    print("\nAfter making it past the weird sewer witch woman, you can finially")
    print("see the light at the end. A ladder leading to the surface awaits you")
    print("in the corner of this room. You take it up and finally can brethe in")
    print("the sweet, sweet, non sewer air. At last, you can go home and play a")
    print("video game. Just try not to fall in any more open sewer pipes, ok?")
    print("\n\n\t\tTHE END! CONGRATULATIONS! YOU WIN!\n\n")
    
    sys.exit(0)

def north2east0():

    #STOPPING POINT

    if check_visited_status() == False:
        
        print("\nIn front of you sits a sign. You're at a fork in the road")
        print("You can only go south, east or west from this point. The ")
        print("sign pointing to the east says \"EXIT\", but on closer inspection")
        print("it has been crossed out and written over in big black letters")
        print("that says \"CLOSED\". Weird. To the west, the sign says")
        print("\"DANGER\", but that too has been crossed out and written over.")
        print("The new text says \"COMPLETELY SAFE NEW EXIT\". Good to know!")
        
        change_room_status()

    else:
        
        print("\nYou are back at the strangely edited sign. The \"EXIT\" sign")
        print("pointing to the east is still written over crudely with")
        print("with the words \"CLOSED\". The west sign's \"DANGER\" also")
        print("still says \"COMPLETELY SAFE NEW EXIT\". You appriciate the")
        print("reminder!")

def north0east2():
    
    if rooms.check_visited_status() == False:
        
        print("You arrive in a larger than average room room with")
        print("signs everywhere. Big signs, small signs, some as")
        print("large as your head! Obviously, there is a sign above")
        print("your head as you enter. It reads: \"Sign Library\"")
        print("Maybe you should take some time to look at the signs?")
        
        rooms.change_room_status()

    else:
        
        print("\nYou arrive back at the sign library. You decide")
        print("to review some of the signs you read.")

    while True:
        
        print("\nHere's what catches your eye.")
        print("1. A Big red sign that looks like it says \"DANGER\"")
        print("\tacross the top.")
        print("2. A sign that looks like your grandmother would have")
        print("\tit on her mantle.")
        print("3. A spooky looking sign that is all black with white")
        print("\tletters.")
        print("4. A weird sign with only one repeated letter on it.")
        print("5. Screw reading! I wanna go somewhere else!")

        try:
            read = input("What would you like to check out? ")

            if read == '1':
                
                print("\nYou walk over to the big red sign that definitely says danger on it.")
                print("It reads: DANGER! BOTTOMLESS PIT TO THE NORTH. DO NOT ENTER BOTTOMLESS PIT.")
                print("Short, sweet, and to the point. Perhaps you should heed its warning?")

            elif read == '2':
                
                print("\nYou pick up the granny sign. It says \"Smiles are always better than frowns.\"")
                print("As much as you appreciate the message, you don't think you'll have the space")
                print("to check the sign out. It'd look so good in your room. You sadly place the")
                print("sign back on the shelf.")

            elif read == '3':
                
                print("\nYou check out the spooky looking sign. It was sitting all by itself in a dark")
                print("corner of the room. You brush off some of the dust and see that it says: \" Femurs")
                print("make the best fishing rods\". You don't get it.")

            elif read == '4':
                
                print("\nYou pick up a sign that only has one letter repeated twelve time on it. It's just")
                print("the letter a written 12 times. Why is this even here? It looks like the name on a high")
                print("score board on some stupid arcade machine to you.")
                print("You place it back where you found it, still confused.")

            elif read == '5':
                
                print("\nYou grow weary of all the signs on the walls. No wonder you never liked Applebees")
                print("much. You decide it's time to be on your way. You push through the door and hit")
                print("the slimey sewer streets..")
                
                break

            elif read == '6':
                
                print("\nYou look at the sign in the front entrance. \"No sewer people allowed!\" is what")
                print("is sprawled across it in big black bold letters. Huh, who is supposed to go in here")
                print("then? What's the point? Another of life's great mysteries I suppose.")

            else:
                
                print("\nThe sign librarian scuttles over to you. \"We don't have the sign you're looking for,")
                print("huh? Well fill out the information on this piece of paper, and we'll try to")
                print("transfer it here from another sign library. It will probably take a week to get it")
                print("here.\". You decide to check out another book.")

        except KeyboardInterrupt:
            
            print ("\nWhat was that? I don't think they have that sign here!")
    
def south1east0():

    if check_visited_status() == False:
            
        print("\nYou wander off to see what the sewer has to offer. You can't see much of intrest around you,")
        print("but you think you see what appears to be a bunch of hovels lined up together.")
        print("There might be a sewer person village to the south. Maybe they know how to get out of here?")
        
        change_room_status()

    else:
        
        print ("\nYou've been here before. Being here again reminds you")
        print ("of how thoroughly disapointing the sewer has been.")
        print ("You can still see the sewer village to the south of here.")

def south2east0():
    
    gotojail = False
    #If this flips to true, the player will be moved to jail, a specific room with a puzzle involved

    if check_visited_status() == False:
                
        print("\nAs you continue on your travels, your eye catches light in the distance.")
        print("Fire? Down here? That must mean there are other people! Not just a few people")
        print("either. As you approach, you notice several crudely built sewer hovels. The")
        print("smell of all the sewer citizens in one place is bad enough to make you want to")
        print("wretch, but for the sake of getting home, you decide it might be worth exploring")
        print("and talking to the locals.")
        
        change_room_status()

    else:
                
        print("\nThe familiar sight of fire, hovels, and extra sewer garbage means you've arrived")
        print("back at the sewer village. You decide to take another look around.")

    while True:
                
        print("\nHere's the places you think might have information for you.")
        print("1. The sewer tavern, Sewage Mcdrinksalot's alcohol hole.")
        print("2. The sewer general store.")
        print("3. The sewer hobo gathering grounds.")
        print("4. You feel like it's time to go. You think you should be on your way.")

        try:
            
            location = input("Where would you like to go? ")

            if location == '1':
                                
                print("\nYou enter Sewage Mcdrinksalot's Alcohol Hole. You don't really know what to expect")
                print("from this place. You wade through all the drunken sewer people enjoying themselves")
                print("to speak the the bartender. The man looks older and has an eyepatch. Must have been")
                print("in some serious sewer fights in his prime. You tell him your sitation. He remarks")
                print("\" The only exit I've ever heard anyone talking about was up north past an old sewer")
                print("witch. Nasty lady who doesn't trust anyone. Check it out but prepare for the worst\"")
                print("You thank the man for the information and leave on your way.")

            elif location == '2' and corner_cases['jailtime'] == False:
                                
                print("\nYou arrive at the sewer general store. A grizzled old sewer man with an eyepatch and")
                print("a scruffy white beard greets you with \"Welcome young man. Whaddre ya buyin?\"")
                print("You explain to him your situation, but he doesn't look sympathetic in the least.")
                print("\"OH BOO HOO all you surface dwellers ever want to do is leave. Cry me a sewer river.")
                print("Look if you're not buying, then I don't want you here. If you come back again I'll")
                print("get you thrown in SEWER JAIL.\"")
                print("You hastily leave. You probably shouldn't come back.")
                
                corner_cases['jailtime'] = True

            elif location == '2' and corner_cases['jailtime'] == True:
                                
                print("\nYou walk back into the sewer general store despite being told never to return.")
                print("You\'re such a rebel. \"WHAT DID I TELL YOU?\" screams the sewer general store owner.")
                print("\"NOW YOU'RE GONNA GO TO SEWER JAIL.\" A guard immediately bursts in and drags you")
                print("off to sewer jail...")
                
                gotojail = True
                
                break

            elif location == '3':
                                
                print("\nYou stumble into the hobo hole, not sure what you're expecting but you're optimistic.")
                print("No one seems to want to speak to you, but you hear some screams in the distance.")
                print("SEWER MUTANTS HATE FLASHLIGHTS")
                print("WITCHES LOVE NUMBERS, ESPECIALLY ONES FOUND ON WALLS")
                print("WHY CAN\'T I GO TO TO THE SIGN LIBRARY ANYMORE?")
                print("IF A ROBOT WANTS TO PLAY A GAME, TELL IT no!!!")
                print("That all sounds like pure madness to you. You decide to turn around.")

            elif location == '4':
                                
                print("\nYou think it's time to hit the old dusty trail. Or sewagy in this case.")
                print("You turn around and continue on your quest to go home.")
                
                break

            else:
                                
                print("\nYou wander around aimlessly instead of chosing a destination. You")
                print("Don\'t find anything of interesting! Maybe you should stick to the list!")

        except KeyboardInterrupt:
                        
            print("\nYou wander around aimlessly instead of chosing a destination. You")
            print("Don\'t find anything of interesting! Maybe you should stick to the list!")

    if gotojail == True:
                
        Rooms().northsouth = -2
        Rooms().eastwest = -1
        current_room = Map.rooms["-2,-1"]
        current_room().contents()
        #After you leave this room and come back, gotojail will be set back
        #to False, so unless you talk to the general store guy again,
        #you won't get thrown in jail on repeat visits when you try to leave.

def north0west1():

    if check_visited_status() == False:
                
        print("\nYou see an eldery sewer couple enjoying the fresh sewer air.")
        print("They seem nice enough. You decide to talk to them. \"Why hello there")
        print("deary!\" The old sewer woman says to you nicely. You explain to")
        print("the couple what has happened to you. \"Well daggonit, let")
        print("us tell you how to get out of this daggurn place! We used")
        print("to live on the surface but decided to retire here. It's not")
        print("so bad once you get used to it.\" You don't know if you believe")
        print("that, but you'll take all the help you can get. You decide to")
        print("ask some questions.")
        
        change_room_status()

    else:
                
        print("\nYou return back to the location where the elderly couple is relaxing.")
        print("You decide to talk to them some more since they were so friendly before!")


    while True:
                
        print("\nWhat would you like to ask them?")
        print("1. How do I get out of here?")
        print("2. How do you survive down here?")
        print("3. Anything I should look out for?")
        print("4. Thanks for your help. I'll be on my way now.")

        try:
            question = input("What would you like to do? ")

            if question == '1':
                                
                print("\nYou ask how to get out of here.")
                print("\"There was an exit somewhere around here...\" The old woman says with a confused")
                print("look on her face.\" I think it was to the northwest? or maybe the southeast?")
                print("I can't remember deary I'm sorry. I just know it was a corner of the sewer...\"")

            elif question == '2':
                                
                print("\nYou ask them how they could possibly enjoy being down here.")
                print("\"Oh it's simple young man!\" The older gentleman excitedly exclaims.\"Plenty of")
                print("sewer greens and daily exercise!\" He begins doing pushups in front of you.")
                print("That's totally not what you meant but you don't really care to ask again.")

            elif question == '3':
                                
                print("\nYou ask if there's anything you should look out for.")
                print("\"Hmm well there is a sign library to the east. Lots of great signs to read there!")
                print("To the south is the village where we stay. Make sure to stop in the bar there!")
                print("Great people in that village. I hear there are sewer mutants about these days but")
                print("we haven't seen any. I'm sure you'll be safe deary.\"")
                print("You hope so too.")

            elif question == '4':
                                
                print("\nYou tell the nice couple that you're going to see if you can find the exit.")
                print("You give them each a hug and continue on your way.")
                                          
                break

            else:
                print("\n\"What was that deary?\" The old lady says. \"Could you repeat that?\"")

        except KeyboardInterrupt:
                        
            print("\nThis elderly couple definitely doesn\'t know slang like that. Try typing in")
            print("a number instead! They like numbers!")

def north0west2():
                                          
    blinded = False
                                          
    mutantalive = True
                                          
    behindhim = False
                                          
    #Blinded and behindhim are used to unlock different options in the fight.
    #Once they're flipped to True you can win and flag the mutant as dead.

    if check_visited_status() == False:
                                          
        print("\nOH NO! A SEWER MUTANT ATTACK! You don't want to go down without")
        print("a fight. You decide to make it one. You scream \"It's go time you")
        print("green pice of garbage!\" at the monster! With some quick thinking you")
        print("think you can make it out of this alive. Hopefully your fighting")
        print("skills are better than your one-liners. Yeesh.")


        while mutantalive != False:

            print("\nWhat do you want to do?")
            print("1. Punch him in the spleen.")

            if blinded == True:
                                          
                print("2. Bonk the mutant on the head with a rock.")
                                          
            else:
                                          
                print("2. Blind the mutant with your flashlight")
                #examples of options that change based on what the player has done.

            if behindhim == True:
                                          
                print("3. Push the mutant over.")

            else:
                                          
                print("3. Run behind the mutant.")

            print("4. Run away scared")

            try:
                                          
                option = input("What are you going to? ")

                if option == '1':
                                          
                    print("\nYou fool! Sewer mutants don't have spleens! The sewer mutant is unphased by your attack")
                    print("And strikes you down with one blow!")
                    print("\n\n\t\tTHE END!\n\n")
                                          
                    sys.exit(0)

                elif option == '2' and blinded == False:
                                          
                    print("\nYou whip out your trusty flashlight and blind the mutant! Good work!")
                    print("The sewer mutant swats around now, unsure of what to do.")
                                          
                    blinded = True

                elif option == '2' and blinded == True and behindhim == False:
                                          
                    print("\nYou run into the mutant's face to him him in the head with a rock. His blind")
                    print("swinging though hits you in the head and kills you instantly! Whoops!")
                    print("\n\n\t\tTHE END!\n\n")
                                          
                    sys.exit(0)

                elif option == '2' and blinded == True and behindhim == True:
                                          
                    print("\nYou bonk the mutant in the back of the head! This kills the mutant instantly!")
                    print("You see the look on the mutant's face. It was one of shock and surprise at its defeat.")
                                          
                    mutantalive = False
                                          
                    break

                elif option == '3' and behindhim == False and blinded == False:
                                          
                    print("\nYou run behind the mutant... but he can clearly see your plan. That didn't work")
                    print("so well. At least you're not dead.")

                elif option == '3' and behindhim == False and blinded == True:
                                          
                    print("\nYou easily make your way around the blinded mutant. Now is the perfect opportunity")
                    print("for an attack!")
                                          
                    behindhim = True

                elif option == '3' and behindhim == True:
                                          
                    print("\nYou giggle and push the mutant over. Just like when you were in middle school!")
                    print("Unfornately that doesn't really seem to do anything. The mutant just gets back up.")
                    print("He still can't see though so he can't kill you. It's the little things in life.")

                elif option == '4':
                                          
                    print("\nYou realize how stupid of a plan this is and decide to run away.")
                    print("The mutant has other plans though and kills you instantly. There are no such")
                    print("things as sewer cowards around here!")
                    print("\n\n\t\tTHE END!\n\n")
                                          
                    sys.exit(0)

                else:
                    print("\nI don't know what you were trying to do, but it didn't work. Try something else.")

            except KeyboardInterrupt:
                                          
                print("The sewer mutant is so confused by what you're saying that he just kills you!")
                print("\n\n\t\tTHE END!\n\n")
                                          
                sys.exit(0)

        print("\nYou are victorious! You can now be on your merry way!")
                                          
        change_room_status()

    else:
                                          
        print("\nYou enter the area where you fought that sewer mutant. His")
        print("corpse is still lying on the ground. Don't worry it's not gonna")
        print("get you! This area is pretty boring now. You leave as quick")
        print("as you came.")
                                              
def north1west1():
                                          
    i = 0
                                          
    buttons = []

    solution = ['G', 'R', 'B', 'G', 'R']
    #These three are all related to the puzzle below.
                                          
    freedom = False
    #This needs to be True in order for the player to progress.

    if change_room_status():

        print("\nThis corridor is much smaller than the others you have encountered so far. You see a pedistal")
        print("Sitting in the center of this room. As you approach it, cage doors fall in front of all the exits!")
        print("A sewer trap! And a fiendish one at that! As you scramble to uncover a way to leave the room, you")
        print("remember the pedistal in the center. You look it over. On the top there is a red, a green, and a")
        print("blue button. On the front of the panel, there is a plaque. This is what it says.")

        print("\n\tGoing through this should point you in the right direction.")
        print("\tRight now you're probably thinking \"How can this plaque help me\"")
        print("\tGeniuses like you can solve this puzzle, but you're not sure how!")
        print("\tBut you haven't thought about it yet. How the first thing you see is what helps the most.")
        print("\tReally make sure you press those buttons good!")
        #the answer to the puzzle is the first letter of these sentences.
        # G R G B R

        print("\nHuh... well that was cryptic. From what you gather from the message and the panels in front of")
        print("you, you must press these buttons in a specific order to open the doors. Judging by the 1-5 panel,")
        print("it appears as though you have to hit buttons 5 times. After 5 tries if you're right, it'll work.")
        print("Looks like you only get one shot at this. The panel looks so old and worn, it probably won't work")
        print("more than 3 times. You'd better be careful!")
                          
        while i < 3:

            if len(buttons) > 5:
                print("\nYou have pressed more than 5 buttons...")
                print("The panel resets your choices.")
                del buttons[:]

            print("\nButtons pressed so far: ", buttons)
            print("\nHere's what you can do")
            print("0. Re-read the plaque for clues.")
            print("1. Blue Button")
            print("2. Red Button.")
            print("3. Green Button.")
            print("4. Check if you're correct.")

            try:

                choice = input("What would you like to do? ")

                if choice == '0':
                                          
                    print("\nHere is the text of the plaque again.")
                    print("\tGoing through this should point you in the right direction.")
                    print("\tRight now you're probably thinking \"How can this plaque help me\"")
                    print("\tGeniuses like you can solve this puzzle, but you're not sure how!")
                    print("\tBut you haven't thought about it yet. How the first thing you see is what helps the most.")
                    print("\tRemember now, those buttons are what you need to look at.")
                    print("You may read this as many times as you'd like before checking your answer.")

                elif choice == '1':
                                          
                    print("\nYou press the blue button.")
                    print("The button makes a distinct honking noise.")
                                          
                    buttons.append('B')

                elif choice == 2:
                                          
                    print("\nYou press the red button.")
                    print("The button makes a shrill yelling noise, as if it's crying out in pain!")
                                                  
                    buttons.append('R')

                elif choice == '3':
                                          
                    print("\nYou press the green button.")
                    print("The button goes \"AWOOOOOOOOOGA!\"")
                                          
                    buttons.append('G')

                elif choice == '4' and buttons != solution:
                                          
                    print("\nYou check to see if you're correct.")
                    print("After ticking for a bit, the machine makes a loud")
                    print("sound that just makes you feel bad. Guess you got")
                    print("it wrong. As the mechanism turns, you here it crumble")
                    print("a bit more.")
                                          
                    i += 1
                                          
                    del buttons[:]
                    #Once the player guesses wrong, it increments i. Once i is greater than 3,
                    #You lose. It also clears the button presses.

                elif choice == 4 and buttons == solution:
                                          
                    print("\nYou check to see if you're correct.")
                    print("After ticking for a bit, the machine makes a loud sound that")
                    print("is similar to a bell ringing. It makes you feel pretty good ")
                    print("about yourself! You think you got it right! The machine ")
                    print("confirms this for you seconds later. You hear a loud")
                    print("snapping sound coming from the trap mechanism. It doesn't")
                    print("appear to be funcioning anymore. The cages all draw open,")
                    print("and you are free. You suck in that fine sewer air, and have")
                    print("renewed determination for leaving this crazy place.")
                                          
                    freedom = True
                                          
                    change_room_status()
                                          
                    break

                else:
                                          
                    print("\nYou completely whiff and miss pressing a button. Whoops!")
                    print("At least you weren't penalized for it!")

            except KeyboardInterrupt:
                                          
                print("No no no, those are the wrong buttons. You're supposed to hit")
                print("buttons IN THE GAME not on your real keyboard.")

        if freedom == False:
                                          
            print("\nOh no, you messed up 3 times! The mechanism breaks and the")
            print("doors stay locked. You are trapped in here with no chance of")
            print("escape. The loud clang you heard when the doors dropped was")
            print("the last sound you heard.")
            print("\n\n\t\tTHE END!\n\n")
            sys.exit(0)

    else:
                                          
        print("\nYou return to the room that locked you in and forced you")
        print("to press a bunch of buttons in order. Good times... good")
        print("times... Thankfully you won't have to do that again! You")
        print("are now free to come and go as you please since the trap")
        print("mechanism is broken! Hooray!")
                                              
def north1west2():
    
    if check_visited_status() == False:
                                          
        print("\nA bright light shines behind some sewer rags that are hanging")
        print("from the celing. You push past them to see an old man with a long")
        print("dirty beard sitting on a giant pile of trash. He catches eye of")
        print("you entering your domain and begins to talk to you. \"Ah you must")
        print("be the child who fell down here.\" He says very matter-of-fact-ly.")
        print("\"I have the answers you seek child. Here is everything you must do")
        print("to escape this sewer. I have lived here for many, many years, even")
        print("helped build this place with my own two hands. I know all of its")
        print("secrets.")
        print("\nHere's what you need to do:")
        print("The exit is in the northeast corner of the sewers. You will not")
        print("be able to exit though without passing by an evil sewer witch.")
        print("She has been down here as long as I can remember and can only be")
        print("convinced not to kill you by saying her favorite number. I don't")
        print("remember what it is, but I believe the sewer itself does. Try")
        print("searching to the south to find the answer. Once you do all of this,")
        print("the path to leaving will be open to you.\"")
        print("\nSopmething about this old man and what he has said makes you trust")
        print("him. You now know everything you must do to leave.")
        print("\n\t1. Get the witch's favorite number to the south.")
        print("\t2. Say it to her so you may pass.")
        print("\t3. Leave this trash heap. The exit is in the north-east.")
                          
        change_room_status()

    else:

        print("The man that was here is gone. Only your memory of your encounter")
        print("remains. You look around the room for any sign of the wise old")
        print("dude. All you can find is a list that he left behind. You read it:")
        print("\n\tJust in case you forgot what I told you:")
        print("\t1. Get the witch's favorite number to the south.")
        print("\t2. Say it to her so you may pass.")
        print("\t3. Leave this trash heap. The exit is in the north-east.")
        print("\nYou remember what you must do to leave and set out to do it.")
                                              
def north2west1():

    if check_visited_status() == False:
                                          
        print("\nLike most places in the sewer, this location is occupied with")
        print("an old man. This particular old man has a short grey beard, a")
        print("cowboy hat and boots, and talks like he's from Texas.\"WHOOOOOEEEY")
        print("BOY! YOU CHECK OUT THAT FANCY ARCADE THERE TO THE SOUTH EAST! BOY")
        print("HOWDY IT IS PRETTY GREAT!\". You\'re confused as to why he's")
        print("screaming at you like this, and why there are sparks flying from")
        print("every joint in this man's body. All of a sudden, you here a loud")
        print("POP and the man is now hunched over... a black cloud of smoke starts")
        print("coming from his hat. \"aaaaaaaaaa\" are the robot's dying words. You")
        print("say a few words yourself in rememberance of the cowboy robot who")
        print("scared you. You continue on your way, unsure of the point of this stop.")
                          
        change_room_status()

    else:
                                          
        print("\nThe smoldering body of the cowboy robot still lies here. You can")
        print("still see the error code of 109 in his eyes. You even remember his")
        print("famous last words \"aaaaaaaaaaaa\". Advice to live by, for sure.")
        print("Pretend to tip your invisible hat and hit the old dusty trail.")

def north2west2():

    #Instant death room I used as a wall.

    print("\nYou reach a corner of the sewer. You slowly move your flashlight back")
    print("and forth to get an idea of your surroundings. Several objects littering")
    print("the ground catch your eye. They appear to be... bones?!? That's no good.")
    print("You begin to turn around. You start to run but you")
    print("quickly bump into something. That wasn't there before... oh no...")
    print("it's a SEWER MUTANT.")
    print("\nThe sewer mutant sniffs you, realizes you're edible and eats you in")
    print("one bite.")
    print("\n\n\t\tTHE END\n\n")

def south1east1():

    if check_visited_status() == False:
                                          
        print("\nYou enter a brightly lit section of the sewer. This is way different")
        print("from everywhere else that you've been so far. Two women, dressed in")
        print("goggles that you can't see through and lab coats, approach you. \"Hello")
        print("young person... why are you here... can you not escape like us?\"")
        print("Great... looks like they're stuck too. They tell you that they accidently")
        print("turned one of the exits in this place into a wurm hole to a random section")
        print("of the sewer instead of to a parallel dimension. Guess you'll have to look")
        print("out for that. You decide you should leave these two alone.")
                          
        change_room_status()

    else:
                                          
        print("\nYou are back with the two goggle-clad scientists. Great. Maybe their")
        print("experiment gone awry is the reason you're back here? You hope not, and")
        print("remember to look out for a wormhole.")
                                          
def south1east2():
                                          
    blinded = False
                                          
    mutantalive = True
                                          
    behindhim = False

    if check_visited_status() == False:
                                          
        print("\nOH NO! A SEWER MUTANT ATTACK! You don't want to go down without")
        print("a fight. You decide to make it one. You scream \"It's go time you")
        print("green pice of garbage!\" at the monster! With some quick thinking you")
        print("think you can make it out of this alive. Hopefully your fighting")
        print("skills are better than your one-liners. Yeesh.")

        while mutantalive != False:

            print("\nWhat do you want to do?")
            print("1. Punch him in the spleen.")

            if blinded == True:
                                          
                print("2. Bonk the mutant on the head with a rock.")
                                          
            else:
                                          
                print("2. Blind the mutant with your flashlight")

            if behindhim == True:
                                          
                print("3. Push the mutant over.")

            else:
                                          
                print("3. Run behind the mutant.")

            print("4. Run away scared")

            try:
                                          
                option = input("What are you going to? ")

                if option == '1':
                                          
                    print("\nYou fool! Sewer mutants don't have spleens! The sewer mutant is unphased by your attack")
                    print("And strikes you down with one blow!")
                    print("\n\n\t\tTHE END!\n\n")
                                          
                    sys.exit(0)

                elif option == '2' and blinded == False:
                                          
                    print("\nYou whip out your trusty flashlight and blind the mutant! Good work!")
                    print("The sewer mutant swats around now, unsure of what to do.")
                                          
                    blinded = True

                elif option == '2' and blinded == True and behindhim == False:
                                          
                    print("\nYou run into the mutant's face to him him in the head with a rock. His blind")
                    print("swinging though hits you in the head and kills you instantly! Whoops!")
                    print("\n\n\t\tTHE END!\n\n")
                                          
                    sys.exit(0)

                elif option == '2' and blinded == True and behindhim == True:
                                          
                    print("\nYou bonk the mutant in the back of the head! This kills the mutant instantly!")
                    print("You see the look on the mutant's face. It was one of shock and surprise at its defeat.")
                                          
                    mutantalive = False
                                          
                    break

                elif option == '3' and behindhim == False and blinded == False:
                                          
                    print("\nYou run behind the mutant... but he can clearly see your plan. That didn't work")
                    print("so well. At least you're not dead.")

                elif option == '3' and behindhim == False and blinded == True:
                                          
                    print("\nYou easily make your way around the blinded mutant. Now is the perfect opportunity")
                    print("for an attack!")
                                          
                    behindhim = True

                elif option == '3' and behindhim == True:
                                          
                    print("\nYou giggle and push the mutant over. Just like when you were in middle school!")
                    print("Unfornately that doesn't really seem to do anything. The mutant just gets back up.")
                    print("He still can't see though so he can't kill you. It's the little things in life.")

                elif option == '4':
                                          
                    print("\nYou realize how stupid of a plan this is and decide to run away.")
                    print("The mutant has other plans though and kills you instantly. There are no such")
                    print("things as sewer cowards around here!")
                    print("\n\n\t\tTHE END!\n\n")
                                          
                    sys.exit(0)

                else:
                    print("\nI don't know what you were trying to do, but it didn't work. Try something else.")

            except KeyboardInterrupt:
                                          
                print("The sewer mutant is so confused by what you're saying that he just kills you!")
                print("\n\n\t\tTHE END!\n\n")
                                          
                sys.exit(0)

        print("\nYou are victorious! You can now be on your merry way!")
                                          
        change_room_status()

    else:
                                          
        print("\nYou enter the area where you fought that sewer mutant. His")
        print("corpse is still lying on the ground. Don't worry it's not gonna")
        print("get you! This area is pretty boring now. You leave as quick")
        print("as you came.")
                                              
def south2east1():

    if check_visited_status() == False:

        print("\nYou come across an old man. Long robes, bald head, meditating")
        print("quietyly... this looks like a master of kung fu. The old man")
        print("sees you. He seems to sense you're not from around here.")
        print("\"You there. You look like you could use a lesson in defending")
        print("yourself. Sewer God forbid you happen To run into a mutant down")
        print("here, you need to know that their weakness is the back of their")
        print("head. Strike them there and they will fall. Now be on your way")
        print("I am busy here.\" You thank him for the advice and continue on your way.")
                          
        change_room_status()

    else:

        print("\nYou come back to the kung fu master for more training. Unfortunately,")
        print("he has imparted on you all the knowledge he had. You don't really")
        print("want to pester him any further so you just walk away sadly instead.")

def south2east2():

    print("\nYou arrive in what seems to be a corner in the sewers with what")
    print("appears to be... a ladder! Finally your journey has come to an end.")
    print("You make your way over to the ladder and climb up it, carefully")
    print("pushing away the manhole cover. It's dark, but hey you've been down")
    print("here awhile. It must be night time. You jump out and begin.... falling!?")

    print("\nTurns out you just jumped through a wormhole. You're now in a random room in the sewer! Enjoy!")

    time.sleep(15)
    #Used to give the player a moment to read the above text so they know what is going on.
    
    random_coordinate1 = randint(-1, 1)        
    random_coordinate2 = randint(-1, 1)
    #This won't let the player get to any room with a 2 or -2 in its coordinates.
    #That way the player won't accidently win the game
                                          
    coordinates['northsouth'] = random_coordinate1
    coordinates['eastwest'] = random_coordinate2
    #Needed so that after the random room is completed, the game doesn't think you're still in this room.
                                          
    room_coordinate = "{},{}".format(random_coordinate1, random_coordinate2)
    current_room = rooms[room_coordinate]

    exec('{}'.format(current_room))
                                          
def south1west1():
                                          
    win = False
                                          
    cheat = False
                                          
    #These are needed to change the player's options based on what has happened
    #While interacting with the upcoming character.

    if check_visited_status() == False:

        print("\nAs you turn the corner into this area, a man who was running from")
        print("something bumps into you knocking you both to the ground. You each")
        print("pick yourselves up and brush off the sewer dirt. The man begins")
        print("yelling \" HEY MAN I'M WALKIN HERE! WATCH YERSELF YA DINGUS!\" You")
        print("apologize for some reason even though it wasn't your fault. You ask")
        print("this guy what he's running from. The man explains: \" I just")
        print("escaped from sewer jail. Bada bing bada boom!")
        print("Don't go to the south unless you wanna get locked up,")
        print("ya dig?\" You heed his warning. \"So long as I'm here, wanna play")
        print("a little game chummmmmmmmm?\" you say okay as he finishes saying chump.")
        print("\nLets play a little 3 card sewer monty. Find the ace and win a prize!")
        print("The man quickly shuffles 3 cards and then lays them flat on the ground.")

        while win != True:

            try:
                print("Which will you pick?:")
                print("1. left")
                print("2. center")
                print("3. right")
                                          
                pick = input("\nWhat is your choice? ")

                if pick == '1' and cheat == False:

                    print("\nHeh heh heh, sorry that's a 2 a clubs. I outta club you!")
                    print("Eyyy tough guy I'll give you one more shot.")
                    print("Weird, you could have sworn the ace was there...")
                                          
                    cheat = True

                elif pick == '2' and cheat == False:

                    print ("\nSorry! That was the 3 a diamonds! I knew you were a chump!")
                    print ("Ey tough guy I'll give you one more shot.")
                    print ("Weird, you could have sworn the ace was there...")
                                          
                    cheat = True

                elif pick == '3' and cheat == False:

                    print("\nOOOOOH NOPE THAT'S WRONG! You have no clue what you're doing, do ya?")
                    print("Eyyyy tough guy I'll give you one more shot.")
                    print("Weird, you could have sworn the ace was there...")
                                          
                    cheat = True

                elif cheat == True:

                    print("\nSorry buddy but you're wrong again! Looks like I win!")
                                          
                    win = True

                else:

                    print("\nEy dumb dumb that's not even a choice. Wanna try a real option?!")

            except KeyboardInterrupt:

                print("\nHey man, instead of being clever, could you just pick a card? Please and thanks.")

        print("\nYou're 99% sure this guy cheated you.")
        print("You can:")
        print("1. Forget about it and just give him a handful of junk from your bag.")
        print("2. Call him out on his cheat.")

        try:

            choice = input("What would you like to do about it? ")

            if choice == '1':

                print("\nYou know he cheated but you know what, you're not worried about it. You didn't even")
                print("bet anything on the game. It does look like he expected to win SOMETHING though. You hand")
                print("an old plastic spoon from your lunch. He looks very accomplished now.")
                print("\"Pleasure doing business with you friendo! Heh heh heh.\" The man walks away.")
                print("What a jerk. No wonder he was in sewer jail. You decide that leaving is more important.")
                                          
                change_room_status()

            elif choice == '2':

                print("\nYou call him out on his really obvious cheat. You wonder if anyone actually falls for it.")
                print("\"EEYYYYY THAT WAS COMPLETELY LEGIT YOU SUCKER!\" He yells. All of a sudden the dude bops")
                print("you over the head and knocks you out! Looks like your adventure ends here... ")
                print("\n\n\t\tTHE END!\n\n")
                                          
                sys.exit(0)

            else:

                print("\nYou say random gibberish! It really confuses this guy. \"Don't know why I always")
                print("meet the weirdos\". The dude shakes his head as he walks away, leaving you alone. You decide")
                print("head out as well.")
                                          
                change_room_status()

        except KeyboardInterrupt:
                                          
            print("\n\"Eyyy tough guy? You think this ctrl c stuff is funny")
            print("This guy just knocks you out you for no reason! Great... just great.")
            print("You lose for basically no reason.")
            print("\n\n\t\tTHE END\n\n")
                                          
            sys.exit(0)

    else:
                                          
        print("\nYou turn a familiar corner in the sewer, but this time you don\'t bump into that")
        print("sewer rapscallion this time. Darn, you probably would have won 3 card sewer monty")
        print("too this time. Yov've spent a long time practicing. Well, without him here it's")
        print("pretty boring. You leave.")

def south2west1():

    inventory = []                          
    minutes = 0
    #Both of these are used for the below puzzle.
    #Inventory holds 3 strings used for this puzzle.
    #When minutes is above 5, the player loses
                                          
    win = False

    print("\nA sewer guard has taken you! He doesn't think you're friendly at all. The")
    print("big beefy sewer guard throws you in SEWER JAIL!!! Another prisoner is there")
    print("with you. You decide to talk to him.")

    print("\"They got you too huh?\" The sewer man says to you while sobbing. \"Every 10")
    print("minutes they kill all the prisoners they have because of how small the cage")
    print("is... and 5 minutes have passed already!\"")

    print("Frantically you begin to formulate a plan to escape! You see the keys sitting")
    print("on a nearby table. I guess the sewer guard isn't too bright. You start looking")
    print("around for anything you can use to get out of here. You see some things around")
    print("you that look promising, and maybe there's something in your backpack that")
    print("could be of use?")

    while minutes < 5:
                                          
        print("\nHere's what you can check.")
        print("1. The rock lying on the ground.")
        print("2. The discolored brick in the wall")
        print("3. The foul-smelling pile of garbage")
        print("4. Some old bones from a poor, dead sewer person.")
        print("5. The strange looking cage bars")
        print("6. The other person locked in here with you.")
        print("7. Your backpack")

        if len(inventory) == 3:

            print("8. Combine your items to escape.\n")

        else:

            print("8. Try to reach the keys on the table.\n")

        try:

            choice = input("What do you want to do? ")
                                          
            if choice == '1':

                print("\nYou pick up the rock. It's just a rock.")
                print("Dude, it's a rock. What did you think it would do?")

            elif choice == '2':

                if 'Gum' not in inventory:

                    print("\nYou poke the discolored brick in the wall. It seems loose. You pull")
                    print("it from the wall and discover a pack of gum hidden in the wall!")
                    print("You don't ask any questions and decide to keep the gum for")
                    print("yourself. It could be useful!")
                                          
                    inventory.append("Gum")

                else:

                    print("\nThere's nothing else behind the brick!")
                    print("Believe me, you would have taken it if there was.")

            elif choice == '3':

                print("\nYou stare at the big pile of garbage, take a deep breath, and dive right")
                print("in. Rusty cans, shoes without laces, and as many sewer pastries as you")
                print("can eat. Unfotunately, nothing you can use. You also now look like a sewer")
                print("hobo. Great.")

            elif choice == '4':

                if 'Femur' not in inventory:

                    print("\nYou dig around in the old bones for some reason. You find a femur")
                    print("though. A really long one too. Hey, maybe that can help you escape")
                    print("somehow. You decide to keep it.")
                    inventory.append("Femur")

                else:

                    print("\nYou waste a minute constructing and playing a bone xylophone.")
                    print("I guess you had some fun in your final moments at least.")

            elif choice == '5':

                print("\nYou decide to examine the cage bars. They look pretty flimsy. You ")
                print("begin kicking, punching, and pulling on them, but to no avail. Turns")
                print("out the the sewer people have some good handywork, and sewer metal is")
                print("stronger than you thought. Damn crafty sewer people! You curse their")
                print("name in anger!")

            elif choice == '6':

                print("\nYou press the sewer man for more information. \"If I knew a way out,")
                print("don\'t you think I would have done it by now?\" He cries. \"I heard a ")
                print("legend once of a man who escaped sewer prison by combining seemingly ")
                print("random items to get out of here. I think his name was sewer MacGyver\"")
                print("\nWell that was a waste of time.")

            elif choice == '7':

                if "String" not in inventory:

                    print("\nYou decide you dig around in your bag for anything that might help")
                    print("you get out of here. You sift through the books, snacks, notebooks")
                    print("and other crap you were carrying around. The only thing that seems")
                    print("like it could be useful is the ball of string you had on you from")
                    print("your sewing class. You think you can probably make use of that.")

                    inventory.append("String")

                else:
                    print("You take out the nintendo DS in your bag and play for a minute.")
                    print("That was fun! Now you have one less minute to live!")

            elif choice == 8 and not(len(inventory) == 3):

                print("\nYou can see the keys to the prison on the table, too far from your")
                print("reach to grab. If only you had some sort of... primitive fishing rod")
                print("or something like that. Those keys would be your in a heartbeat! Alas,")
                print("all this thinking about how things could be has wasted some of your")
                print("living time. Whoops.")

            elif choice == 8 and len(inventory) == 3:

                print("\nYou think that the things you've found can help you escape this place!")
                print("You take a piece of gum and begin to chew it. While doing that")
                print("you tie the string to the femur. Once tied together, you take out your")
                print("gum and put it on the other end of the string. Voila! You now have a")
                print("sweet key grabbing device! You cast your line and manage to get the ")
                print("keys on your first try! (You weren't really trying on your previous ")
                print("ten attempts.) You quickly unlock the door and make your escape with")
                print("the other prisoner! He tells you that to the west there is a beautiful")
                print("sewer oasis. That might be a promising lead to an exit. You decide to")
                print("ditch the sewer man. He smells a little TOO much like sewers.")
                                          
                win = True

                break

            else:

                print("\nWHY ARE YOU SCREWING AROUND? YOU JUST WASTED A MINUTE")

            if len(inventory) == 3:
                print("Gum, string, a femur... maybe you can use these to escape...")

            minutes += 1

            if minutes == 1:

                print("{} minute has passed.\n".format(minutes))

            elif minutes <= 5 and minutes != 1:

                print("\n{} minutes have passed.\n".format(minutes))

        except KeyboardInterrupt:
                                          
            print("In your frantic panic you don't type a number and just type gibberish")
            print("instead! Get back in there and type a number, tiger!")

    if win == False:
                                          
        print("Times up!!!!!")
        print("NOW YOU PRISONERS DIE! screams the guard. He takes the keys off")
        print("the table and unlocks the door. You try to run away but it's no use.")
        print("\n\n\t\tTHE END\n\n")
                          
        sys.exit(0)

def south1west2():

    yes = ('Yes', 'yes', 'YES', 'Y',  'y')

    no = ('No', 'NO', 'no', 'n', 'N')

    if check_visited_status() == False:
        print("\nThere's nothing really here. You're thankful for that. You think you deserve a few easy")
        print("rooms. Seriously there's nothing.")

        believe = input("You believe me right? ")

        if believe in yes:

            print("Good! See there's nothing here. You can go on your way champ!")

        elif believe in no:

            print("Fine. Feel free to go somewhere else.")

        else:

            print("I didn't understand what you said, so I'll take it as an insult.")
            print("You lose. \n\n\t\tTHE END!\n\n")
                                          
            sys.exit(0)

        change_room_status()

    else:
        print("\nYou liked the room with nothing in it so much that you came back to it!")
        print("Guess you just needed a break huh? Why not just save, quit, and go relax?")
        print("You deserve it, champ.")

def south2west2():

    if check_visited_status() == False:

        print("\nYou seem to be in a corner of the sewer way. Water drips from the walls")
        print("and celing and slowly spashes onto the ground. There isn't much to see here,")
        print("but it's quiet and peaceful for once down here. It might be alright to take")
        print("a break here and take in the scenery. What do you want to do?")

        print("1. Take a rest and absorb your surroundings.")
        print("2. Press on and keep trying to escape.")

        try:
            choice = input("What would you like to do? ")

            if choice == '1':

                print("You decide to sit and meditate for a bit. You shine your flashlight")
                print("around the dark area and take everything in. For some reason you notice")
                print("the number 109 carved into the corner of the wall. Everything else though")
                print("seems right at home with a sewer. After your short break you decide it'scenery")
                print("time to move on with a clear head and more determination to leave than when")
                print("you started your break.")
                                          
                change_room_status()

            elif choice == '2':

                print("\nYou decide to keep going. You'll rest when you're dead.")
                print("DUN DUN DUNNN")
                                          
                change_room_status()

            elif choice == '3':

                print("\nA SEWER MUTANT GRABS YOU AND RIPS YOU TO SHREDS!!!")
                print("THATS WHAT YOU GET FOR BEING CLEVER!!!")
                print("THE END!")
                                          
                sys.exit(0)    

            else:

                print("That choice didn't make any sense, and I'm not going to")
                print("question it. You're free to go.")

        except KeyboardInterrupt:

            print("Geeze, you don't have to patronize me, pal. Can't you just")
            print("Type a number and cooperate? Well whatever you can just move on")
            print("I don't really care.")

    else:

        print("So you came back to the oasis huh? Just couldn't resist the siren")
        print("song of the sewer oasis, huh? WELL you are in luck my friend. This is")
        print("what I wanted you to get out of this: the number 109. Think about that.")
        print("Noodle it for a bit. Where would that make sense?")

if __name__ == '__main__':

    start_game()
    play()
