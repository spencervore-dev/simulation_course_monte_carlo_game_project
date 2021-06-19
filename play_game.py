# Basic script to simulate problem #9 for miniproject 1 in ISYE6644 - Simulation class
# Written by: Spencer Vore & Jessica Warr

import random
import sys
import math
import matplotlib.pyplot as plt

# Function to take the next turn
def take_turn(player):

    #print(f"PLAYER {player} IS NOW TAKING THEIR TURN.")
    dice_roll = random.randint(1,6)
    #print(f"\tRolled value of dice is {dice_roll}.")


    # Possibilities for dice rolls
    if dice_roll == 1:
        #print(f"\tNothing happens during player's turn.")
        pass

    if dice_roll == 2:
        #print(f"\tPlayer takes all {GameState['pot']} coins in the pot.")
        GameState[player] += GameState['pot']
        GameState['pot'] = 0

    if dice_roll == 3:
        coins_to_take = int(math.floor(GameState['pot'] / 2))
        #print(f"\tPlayer takes half of the coins (i.e. {coins_to_take}) from the pot.")
        GameState[player] += coins_to_take
        GameState['pot'] -= coins_to_take

    if dice_roll >= 4:
        #print(f"\tPlayer must put one coin into the pot.")

        # Check if current player has lost the game
        if GameState[player] == 0:
            #print("\n\nEND OF GAME")
            #print(f"Player {player} has no coins to put into the pot. They lose. :)")
            #print(f"Game ended on cycle number {GameState['cycle_number']}")
            #print(f"Final game state is {GameState}.\n\n")
            #sys.exit() #Replace this with return if nesting this into a bigger loop for many games
            GameState['game_over'] = 1
            return GameState['cycle_number']

        # If player didn't lose, update game state
        GameState[player] -= 1
        GameState['pot'] += 1


    # Validation - check that no coins were lost in the code or fell under the game table
    # NO CHEATING
    assert total_coins == GameState['A'] + GameState['B'] + GameState['pot']

    # Print info about what the dice roll made happen
    #print(f"\tPlayer {player} now has {GameState[player]} coins "
          #f"and the pot now has {GameState['pot']} coins.")

    return

# This is the top level part of the script that runs the simulation
# and calls all the helper functions
def play_game():

    #print("\nSTARTING GAME SIMULATION")


    # Define initial game state - number of coins in each category
    global GameState
    GameState = {'A': 4, 'B': 4, 'pot': 2, 'cycle_number': 1, 'game_over': 0}

    # Calculate total coins in the system for validation
    global total_coins
    total_coins = GameState['A'] + GameState['B'] + GameState['pot']

    # Start taking turns, and never stop until loss condition in take_turn function is reached!
    while GameState['game_over'] == False:
        #print(f"\nCYCLE NUMBER: {GameState['cycle_number']}")
        #print(f"\nCurrent Game State is {GameState}\n")
        take_turn('A')
        #print(f"\nCurrent Game State is {GameState}\n")
        take_turn('B')

        # Update turn number
        GameState['cycle_number'] += 1

#This will repeat the simulation a specified number of times
def repeat_game():
    
    #Set number of times to repeat the game
    n = 10000
    
    #List of cycles per game
    cycles = []
    
    #Loop to play the game
    for i in range(n):
        play_game()
        cycles.append(GameState['cycle_number'])
        #print(cycles)
    
    # Find the average of the cycle lengths
    avg_num_cycles = round(sum(cycles)/len(cycles),2)
    print(f"\nThe average number of cycles in {n} games is {avg_num_cycles}\n")
    #Just for an idea of the size of the histogram, here's the min and max
    min_cycles = min(cycles)
    print(f"\nThe min number of cycles in {n} games is {min_cycles}\n")
    max_cycles = max(cycles)
    print(f"The max number of cycles in {n} games is {max_cycles}\n")
    
    #Plot a histogram of the cycle lengths
    _ = plt.hist(cycles, bins='auto')
    plt.title(f"Histogram of Cycle Lengths over {n} games")
    plt.show()

# This is a pretty standard piece of boilerplate python.
# It only runs the program if this script is executed
# as the main program (vs something else)
if __name__ == "__main__":

    # Check if arguments were passed in. If arg, then use first arg as seed.
    # Otherwise, if no argument use system time as seed which is the default for random lib
    if len(sys.argv) <= 1:
        print(f"No user seed provided, so using default seed (i.e. system time)")
        random.seed()
    else:
        # import seed from command line tool
        seed = sys.argv[1]
        print(f"Seed passed into function is {seed}")

        # Set seed
        random.seed(seed)

    # Play the game
    #play_game()
    
    # Repeat game
    repeat_game()