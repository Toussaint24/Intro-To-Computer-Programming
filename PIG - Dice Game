#Pig Dice Game Program by PM. Used to play a game of "Pig".
#-----Import Modules-----
import random
#-----Initialize Variables-----
roll= 0  #Roll the die
playerhold = 0  #Your rolled points
johnhold = 0  #John's rolled points
playerscore = 0  #Player total points
johnscore = 0  #John's total points
johnchoice = 0  #John's choice for ROLL or HOLD
#-----Game of Pig Begins-----
print("You are playing against John Scarne, the creator of Pig.")
while (playerscore < 100 and johnscore < 100):  #Winning score = 100
    #-----Player Turn-----
    playerturn = True
    print("-----Your turn-----")
    playerhold = 0
    while (playerturn == True):
        roll = 0
        playerchoice = input("Would you like to ROLL or HOLD? Your score: {} John's Score: {}".format(playerscore, johnscore)).upper()
        while (playerchoice != "ROLL" and playerchoice != "HOLD"):
            playerchoice = input("You cannot do that! Either ROLL or HOLD. Your score: {} John's Score: {}".format(playerscore, johnscore)).upper()
        if (playerchoice == "ROLL"):
            while (playerchoice == "ROLL") and (roll != 1):
                roll = random.randint(1,6)  #Roll the die for random number 1-6
                if (roll != 1): 
                    print("You rolled a {}.".format(roll))
                    playerhold = playerhold + roll
                    playerchoice = input("Would you like to ROLL or HOLD? Your score: {} John's Score: {}".format(playerscore, johnscore)).upper()
                elif (roll == 1):
                    playerhold = playerhold * 0
                    playerturn = False
                    print("You rolled a 1. Your turn is over.")
        if (playerchoice == "HOLD"):
            playerscore = playerhold + playerscore
            playerturn = False
            print("You will hold.")
        if (playerchoice != "HOLD") and (playerchoice != "ROLL"):
            while (playerchoice != "HOLD") and (playerchoice != "ROLL"):
                playerchoice = input("You cannot do that! Either ROLL or HOLD. Your score: {} John's Score: {}".format(playerscore, johnscore)).upper()
    #-----John Decision-Making-----
    if (playerturn == False):
        print("-----John's Turn-----")
        johnchoice = random.randint(0,10)
        johnhold = 0
        roll = 0
        if (johnchoice < 6):
            while (roll != 1 and johnchoice < 6):
                print("John will roll.")
                roll = random.randint(1,6)
                if (roll == 1):
                    johnhold = johnhold * 0
                    print("John rolled a 1. His turn is over.")
                elif (roll != 1):
                    print("John rolled a {}.".format(roll))
                    johnhold = johnhold + roll
                    johnchoice = random.randint(0,10)
        if (johnchoice >= 6):
            johnscore = johnscore + johnhold
            johnhold = johnhold * 0
            print("John will hold.")
#-----End of the Game-----
if (playerscore >= 100):
    print("You won with {} points!!!".format(playerscore))
elif (johnscore >= 100):
    print("John Scarne won with {} points!!!".format(johnscore))
