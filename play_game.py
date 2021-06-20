# Basic script to simulate problem #9 for miniproject 1 in ISYE6644 - Simulation class
# Written by: Spencer Vore & Jessica Warr

import random
import sys
import math
import matplotlib.pyplot as plt
import statistics
import argparse


# Function to take the next turn
def take_turn(player, verbose=False, print_end_state=False):
    '''Takes one turn in the game for specified player.
        player - Name of the player in the global simulation state who
                    is taking the turn.
        verbose - If True, run all print statements.
        print_end_state - If true, print final results of the game to
                    the terminal. (verbose=True overrides false values)
    '''

    if verbose: print(f"PLAYER {player} IS NOW TAKING THEIR TURN.")
    dice_roll = random.randint(1,6)
    if verbose: print(f"\tRolled value of dice is {dice_roll}.")


    # Possibilities for dice rolls
    if dice_roll == 1:
        if verbose: print(f"\tNothing happens during player's turn.")
        pass

    if dice_roll == 2:
        if verbose: print(f"\tPlayer takes all {GameState['pot']} coins in the pot.")
        GameState[player] += GameState['pot']
        GameState['pot'] = 0

    if dice_roll == 3:
        coins_to_take = int(math.floor(GameState['pot'] / 2))
        if verbose: print(f"\tPlayer takes half of the coins (i.e. {coins_to_take}) from the pot.")
        GameState[player] += coins_to_take
        GameState['pot'] -= coins_to_take

    if dice_roll >= 4:
        if verbose: print(f"\tPlayer must put one coin into the pot.")

        # Check if current player has lost the game
        if GameState[player] == 0:
            if verbose or print_end_state:
                print("\n\nEND OF GAME")
                print(f"Player {player} has no coins to put into the pot. They lose. :)")
                print(f"Game ended on cycle number {GameState['cycle_number']}")
                print(f"Final game state is {GameState}.\n\n")
            GameState['game_over'] = True
            return GameState['cycle_number']

        # If player didn't lose, update game state
        GameState[player] -= 1
        GameState['pot'] += 1

    # Validation - check that no coins were lost in the code or fell under the game table
    # NO CHEATING
    assert total_coins == GameState['A'] + GameState['B'] + GameState['pot']

    # Print info about what the dice roll made happen
    if verbose: print(f"\tPlayer {player} now has {GameState[player]} coins "
          f"and the pot now has {GameState['pot']} coins.")

    return GameState['cycle_number']


def play_game(verbose=False, print_end_state=False):
    '''Plays the game once.
        verbose - If True, run all print statements.
        print_end_state - If true, print final results of the game to
                    the terminal. (verbose=True overrides false values)
    '''

    if verbose: print("\nSTARTING GAME SIMULATION")


    # Define initial game state - number of coins in each category
    global GameState
    GameState = {'A': 4, 'B': 4, 'pot': 2, 'cycle_number': 1, 'game_over': False}

    # Calculate total coins in the system for validation
    global total_coins
    total_coins = GameState['A'] + GameState['B'] + GameState['pot']

    # Start taking turns, and never stop until loss condition in take_turn function is reached!
    while GameState['game_over'] == False:
        if verbose: print(f"\nCYCLE NUMBER: {GameState['cycle_number']}")
        if verbose: print(f"\nCurrent Game State is {GameState}\n")
        take_turn('A', verbose, print_end_state)
        if verbose: print(f"\nCurrent Game State is {GameState}\n")
        take_turn('B', verbose, print_end_state)

        # Update turn number
        GameState['cycle_number'] += 1

    return GameState['cycle_number']


def repeat_game(n=10000, verbose=False, print_end_state=True, make_charts=True):
    '''Repeats the game many time (i.e. performs a Monte Carlo Simulation
       to determine the most likely range of possible game outcomes.

        n - Number of games to play in the simulation.
        verbose - If True, run all print statements.
        print_end_state - If true, print final results of the game to
                    the terminal. (verbose=True overrides false values)
    '''

    #List of cycles per game
    cycles = []

    #Loop to play the game
    for i in range(n):
        cycles_in_game = play_game(verbose=verbose, print_end_state=False)
        cycles.append(cycles_in_game)
        if verbose: print(cycles)

    # Find the average of the cycle lengths
    if verbose or print_end_state:
        avg_num_cycles = round(sum(cycles)/len(cycles),2)
        print(f"\n{n} games were played in this simulation")
        print(f"The mean number of cycles is {avg_num_cycles}")
        print(f"The median number of cycles is {statistics.median(cycles)}")
        print(f"The mode of the number of cycles is {statistics.mode(cycles)}")
        print(f"The standard deviation of the number of cycles is {round(statistics.stdev(cycles), 2)}")
        #Just for an idea of the size of the histogram, here's the min and max
        min_cycles = min(cycles)
        print(f"The min number of cycles is {min_cycles}")
        max_cycles = max(cycles)
        print(f"The max number of cycles is {max_cycles}\n")
        print(f"Justin Bieber rocks! =P")

    #Plot a histogram of the cycle lengths
    if make_charts:
        x_tick_spacing = 10
        binwidth = 2
        _ = plt.hist(cycles, bins=range(0, max(cycles) + binwidth, binwidth),
            edgecolor='black', linewidth=0.5)
        plt.title(f"Histogram of Cycle Lengths over {n} games")
        plt.xticks(range(0, max(cycles)+1, x_tick_spacing))
        plt.xlabel("Number of cycles in a game")
        plt.ylabel("Number of games")
        plt.show()

    return


# Command Line Application to control the game simulation
def cli():
    '''Defines logic for command line interface and kicks off simulation based on passed in arguments.'''
    # Initialize CLI
    parser= argparse.ArgumentParser(description="Use this tool to simulate playing \"The Game\". For miniproject 1.")

    # Command line options are defined here 
    parser.add_argument('sim_mode', action='store', choices=['single', 'multi'],
                        help='Either single or multi mode. Single runs a single game. '
                            'multi runs a lot of games.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help="If this flag is set, run command in verbose mode "
                            "and print lots more output to the terminal.")
    parser.add_argument('-r', '--random-seed', action='store', default=None,
                        help='Set random seed for pseudo random number generator in simulation. '
                            'If this is not set, it will just use the default seed (i.e. system time).')
    parser.add_argument('-n', action='store', type=int, default=10000, 
                        help='Number of games to play if running in multi sim-mode.')
    parser.add_argument('--no-charts', action='store_true',
                        help='Set this flag to disable histogram generation when running in multi sim-mode.')

    # Extract command line arguments and execute program based on them
    args = parser.parse_args()
    verbose = args.verbose
    if verbose: print(f"Input arguments passed in are {args}.")

    # Set seed
    seed = args.random_seed
    if seed is None:
        if verbose: print(f"No user seed provided, so using default seed (i.e. system time)")
        random.seed()
    else:
        # import seed from command line tool
        if verbose: print(f"Seed passed into function is {seed}")
        random.seed(seed)

    # Run different functions depending on the simulation mode
    if args.sim_mode == 'single':
        play_game(verbose=verbose, print_end_state=True)
    elif args.sim_mode == 'multi':
        n = args.n
        charts = not args.no_charts
        repeat_game(n=n, verbose=verbose, print_end_state=True, make_charts=charts)

    return


# This is a pretty standard piece of boilerplate python.
# It only runs the program if this script is executed
# as the main program (vs something else)
if __name__ == "__main__":
    cli()
