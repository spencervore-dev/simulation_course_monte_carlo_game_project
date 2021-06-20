# Simulation for miniproject 1 

## Summary
This Code is to simulate the game in problem #9 of miniproject 1
in the ISYE6644 - Simulation course at Georgia Tech.

## How to use

### Environment set up
This code was developed in a Python 3.8.2 environment, so first you will
need to set up one of these. Probably any python close to 3.8ish should work.

Install a few third party libraries once you have your Python 3.8 environment 
using:

pip install -r requirements.txt

I added some notes on how I set up my own development python environment in 
the configure_env.txt file, or you can do something else (like just install 
anaconda and make a virtual environment using that).  

I developed this on a Mac using python virtualenv to build my environment
and the vim text editor.

### Run it
Once you have your python environment set up, you can run this script in 
the terminal by running the play_game.py code as a script like this:

`python play_game.py`

Optionally, you can also pass in a random seed as a command line argument
if you want to get the same result each time:

`python play_game.py 12345`

If there's no seed, the random seed defaults to the system time.

This script will play the game many many times and will generate a plot
of the distribution of cycle times.
