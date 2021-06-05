# Basic script to simulate problem #9 for miniproject 1 in ISYE6644 - Simulation class
# Written by: Spencer Vore

import random
import sys
import math

# Function to take the next turn
def take_turn():

    print(f"\nTURN NUMBER: {GameState['turn_number']}")
    dice_roll = random.randint(1,6)
    print(f"\tRolled value of dice for player {GameState['whos_turn']} is {dice_roll}.")

    # Possibilities for dice rolls
    if dice_roll == 1:
        print(f"\tNothing happens during player {GameState['whos_turn']}'s turn.")

    if dice_roll == 2:
        print(f"\tPlayer {GameState['whos_turn']} takes all {GameState['pot']} coins in the pot.")
        GameState[GameState['whos_turn']] += GameState['pot']
        GameState['pot'] = 0


    if dice_roll == 3:
        coins_to_take = int(math.floor(GameState['pot'] / 2))
        print(f"\tPlayer {GameState['whos_turn']} takes half of the coins (i.e. {coins_to_take}) from the pot.")
        GameState[GameState['whos_turn']] += coins_to_take
        GameState['pot'] -= coins_to_take

    if dice_roll >= 4:
        print(f"\tPlayer {GameState['whos_turn']} must put one coin into the pot.")
        GameState[GameState['whos_turn']] -= 1
        GameState['pot'] += 1

    # Validation - check that no coins were lost in the code or fell under the game table
    assert total_coins == GameState['A'] + GameState['B'] + GameState['pot']

    # Print info about what the dice roll made happen
    print(f"\tPlayer {GameState['whos_turn']} now has {GameState[GameState['whos_turn']]} coins "
          f"and the pot now has {GameState['pot']} coins.")

    # Check if current player has lost the game
    if GameState[GameState['whos_turn']] < 0:
        print("\n\nEND OF GAME")
        print(f"Player {GameState['whos_turn']} has no coins to put into the pot since their coin "
              f"account balance is now negative. They lose.  :)")
        print(f"Game ended on turn number {GameState['turn_number']}")
        print(f"Final game state is {GameState}.\n\n")
        sys.exit()

    # Update who's turn is next
    if GameState['whos_turn'] == 'A':
        GameState['whos_turn'] = 'B'
    else:
        GameState['whos_turn'] = 'A'

    # Update turn number
    GameState['turn_number'] += 1


# This is the top level part of the script that runs the simulation
# and calls all the helper functions
def main():

    print("STARTING GAME SIMULATION")

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


    # Define initial game state - number of coins in each category
    global GameState
    GameState = {'A': 4, 'B': 4, 'pot': 2, 'whos_turn': 'A', 'turn_number': 1}

    # Calculate total coins in the system for validation
    global total_coins
    total_coins = GameState['A'] + GameState['B'] + GameState['pot']

    # Start taking turns, and never stop until loss condition in take_turn function is reached!
    while True:
        print(f"\nCurrent Game State is {GameState}")
        take_turn()

# This is a pretty standard piece of boilerplate python.
# It only runs the program if this script is executed
# as the main program (vs something else)
if __name__ == "__main__":
    main()
