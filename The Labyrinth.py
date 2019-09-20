#-----------------Import Modules-------------------------
import sys
import os
import random
import time
import keyboard
import msvcrt
#------------------Define Clear-----------------------------
cls = lambda: os.system('cls')
wait = lambda x: time.sleep(x)
#--------------Title Formatting and Display----------------
with open(r"Title Design.txt") as title:
  print(title.read())
input("\n\t\t\t\t\t\tPress enter to begin!")
cls()
#-------------------------Enemy Class---------------------------
class Enemies:
  class_name = ""
  _desc = ""
  enemy_type = {}
  enemy_list = []
  def __init__(self, name):
    self.name = name
    self.enemy_type[self.class_name] = self
    self.enemy_list.append(self.class_name)
  def get_desc(self):
    return enemy_string + ": " + enemy_desc
  def get_healthbar(self):
    return "Health: " + "|" * round(enemy_health / 10)
class Goblin(Enemies):
  def __init__(self, name):
    self.class_name = "Goblin"
    self._desc = "A short but agile and aggressive creature"
    self.health = 100
    self.strength = 50
    super().__init__(name)
class Bear(Enemies):
  def __init__(self, name):
    self.class_name = "Bear"
    self._desc = "A large omnivorous mammal with a large apetite"
    self.health = 150
    self.strength = 100
    super().__init__(name)
class Orc(Enemies):
  def __init__(self, name):
    self.class_name = "Orc"
    self._desc = "It's green, it's mean, and it's got a giant sword"
    self.health = 200
    self.strength = 250
    super().__init__(name)
class Wolf(Enemies):
  def __init__(self, name):
    self.class_name = "Wolf"
    self._desc = "A natural born predator"
    self.health = 150
    self.strength = 200
    super().__init__(name)
class Human(Enemies):
  def __init__(self, name):
    self.class_name = "Human"
    self._desc = "A weak but intelligent creature capable of wielding variety of tools"
    self.health = 100
    self.strength = 50
    super().__init__(name)
#------------------------Player Class-----------------------
class Player:
  def __init__(self, name):
    self.username = name
    self.health = 1000
    self.strength = 50
#-----------------------Message Printing-------------------------
def timed_printing(msg):
  for i in range(len(list(msg))):
    if msvcrt.kbhit():
      skip = keyboard.read_hotkey()
      if skip == "enter":
        print(msg[i:])
        break
    print(msg[i], end= "")
    time.sleep(0.05)
  print(".")
  return
#-------------------------Player Initialization--------------------------
timed_printing("Hello there, adventurer. I suppose you're here to find the treasure located on the 30th floor of the labyrinth")
wait(0.5)
timed_printing("Well, you should know that the labyrinth is very dangerous. It's filled with dangerous monsters")
wait(0.5)
timed_printing("Not a single one has even made it seen the 30th floor let alone bring back the treasure alive")
wait(0.5)
timed_printing("If you insist on going, I will not stop you")
wait(2)
cls()
wait(0.2)
username = input(timed_printing("What is your name, adventurer?"))
player = Player(username)
player_health = player.health
player_strength = player.strength
timed_printing("Good luck, {}. Walk to begin your adventure in the Labyrinth".format(username))
wait(2)
cls()
#---------------------------Enemy Initialization--------------------------
goblin = Goblin("Goblin")
bear = Bear("Bear")
orc = Orc("Orc")
wolf = Wolf("Wolf")
human = Human("Human")
#--------------Map Initialization Backups and Updates----------------
map_ = r"Labyrinth Maps\Small Maps\Map 001"
map_file = open(map_, "a")
counter = 1
def map_backup():
  global map_file 
  if backup_mode == True:
    backup_map_file = map_file
  else:
    map_file = backup_map_file
  return
def map_update():
  global map_
  global backup_mode
  global map_file
  global counter
  backup_mode = False
  map_backup()
  map_file.close()
  map_ = list(map_)
  if counter == 10:
    map_.remove("0")
    map_.remove(str(counter))
    map_.append(str(counter + 1))
    "".join(map_)
    map_file = open(map_, "r+a")
    backup_mode = True
    map_backup()
    counter += 1
    return
#-------------------------Battle Setup----------------------------
def encounter_setup(enemy):
  """Prepares the battle by initializing
  enemy stat variables, creating
  a string of the enemy class, and
  randomly deciding who moves first"""
  global encounterON
  global turn
  #---------------Enemy Stat Initialization-----------------
  global enemy_string
  global enemy_desc
  global enemy_health
  enemy_health = Enemies.enemy_type[enemy].health
  enemy_strength = Enemies.enemy_type[enemy].strength
  enemy_desc = Enemies.enemy_type[enemy]._desc
  enemy_string = Enemies.enemy_type[enemy].class_name
  if enemy_string[0] in ["A", "E", "I", "O", "U"]:
    article = "an"
  else:
    article = "a"
  print("You encountered {} {}!".format(article, enemy))
  encounterON = True
  turn = random.choice(["Player", "Enemy"])
  encounter(enemy)
#----------------------Take Input-----------------------
def input_():
  """Takes input from the user, matches it with
  any dictionary pairs and runs the corresponding
  function"""
  global encounterON
  command = input(":: ").split()
  action = command[0]
  if encounterON == True:  #Check if in battle mode or wander mode
    if action in battle_command_list:  #Check for user input in battle command list
      action = battle_command_list[action]
    else:
      print('Unknown action "{}"'.format(action))
      return
  else:
    if action in general_command_list:  #Check for user input in general command list
      action = general_command_list[action]
    else:
      print('Unknown action "{}"'.format(action))
      return
  action()
def walk():
  """Initiates walk mode. Player may
  move in any direction, respecting
  boundaries with an 50% chance of encounter"""
  global map_file
  timed_printing("You have entered walk mode. Use the wasd keys to move and shift to exit walk mode")
  walkmode = True
  while walkmode == True:
    for character in map_file:   
      map_file.read(1)
      wait(0.01)
    movement = keyboard.read_hotkey()
    if (movement.lower() == "w") and (map_file.tell() >= 28):
      map_file.seek(-28, map_file.tell())
      if (map_file.read(1) == "_") or (map_file.read(1) == "|"):
        map_file.seek(28, map_file.tell())
        continue
    else:
      continue
    if round(random.random(), 1) < 0.8:  #Random encounter
      encounter_setup(random.choice(Enemies.enemy_list))  #Random encounter type
    else:
      timed_printing("Nothing happened")
def encounter(enemy):
  """Runs the battle system"""
  global player_health
  global enemy_health
  global turn
  global encounterON
  global enemy_strength
  while (player_health > 0) and (enemy_health > 0):  #Battle continues until one side drops below 1 health
    if turn == "Enemy":
      print("\n-----Enemy Turn-----\n")
      print("{} attacks!".format(enemy))
      player_health -= enemy_strength
      print("You lost {} health.".format(enemy_strength))
      turn = "Player"  #Alternate enemy and player turns
    else:
      print("\n-----Player Turn-----\n")
      print("Attack, Items, Examine, Flee")  #Battle commands
      input_()
      turn = "Enemy"  #Alternate enemy and player turns
  if player_health <= 0:  #Battle End Case 1: Player dies
    with open(r"Game Over Design.txt") as gameover:
      print("\n" * 5)
      sys.exit(gameover.read())  #Exit game and print Game Over text 
  else:  #Battle End Case 2: Enemy dies
    print("{} was defeated".format(enemy))
    print("\n-----Battle End-----\n")
    print("You win!\n\n")
    encounterON = False  #End battle
    input_()  #Return to user input
def attack():
  """Attacks the enemy"""
  global enemy_health
  global enemy_string
  enemy_health_lost = int(player_strength * round(random.uniform(0.9,1.1), 1))  #Determine enemy's lost health
  enemy_health -= enemy_health_lost
  print("You attacked the {}.".format(enemy_string))
  print("The {} lost {} health.".format(enemy_string, enemy_health_lost))  #Print lost health
  return  #Return to battle system definition
def flee():
  """Run away from the battle"""
  global enemy_string
  global encounterON
  print("You fled from the {}.".format(enemy_string))
  encounterON = False  #End battle
  input_()  #Return to user input
def items():
  """Things"""
#----------------------Examine----------------
def examine():
  """View enemy description and health bar"""
  global enemy_string
  global turn
  print("You examined the {}.\n".format(enemy_string))
  print(Enemies.enemy_type[enemy_string].get_desc())
  print(Enemies.enemy_type[enemy_string].get_healthbar())
  print()
  turn = "Player"  #Turn stays on Player
  input_()  #Return to user input
def end():
  sys.exit()
#-------------------------Variable Initialization-----------------------
encounterON = False
turn = ""
enemy_string = ""
enemy_desc = ""
enemy_health = 0
enemy_strength = 0
#----------------------Initialize Backup Map--------------------
backup_mode = True
map_backup()
#------------------------------------Command Lists-------------------------------------------
battle_command_list = {
    "flee": flee, "attack": attack, "end": end, 
    "items": items, "examine": examine
}
general_command_list = {
  "end": end, "walk": walk, "items": items,
}
#-------------
while True:
    input_()
#ADD EQUIPMENT FOR PLAYER AND ENEMIES
#ADD PLAYER UPGRADES
#ADD MORE ADVANCED DAMAGE CALCULATIONS
#ADD LEVELING SYSTEM
#ADD ENEMY STAT RANDOMIZATION AND RAMPING
#ADD MORE COMPLEXITIES TO LOWER FLOOR MAZES
#ADD MULTIPLE FLOORS
#ADD TRAPS
#ADD MAP SYSTEM
#IDENTIFY "X" AS PLAYER ICON