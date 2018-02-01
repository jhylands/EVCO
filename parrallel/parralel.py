
"""
A parallel version of XOR using neat.parallel.
Since XOR is a simple experiment, a parallel version probably won't run any
faster than the single-process version, due to the overhead of
inter-process communication.
If your evaluation function is what's taking up most of your processing time
(and you should check by using a profiler while running single-process),
you should see a significant performance improvement by evaluating in parallel.
This example is only intended to show how to do a parallel experiment
in neat-python.  You can of course roll your own parallelism mechanism
or inherit from ParallelEvaluator if you need to do something more complicated.
"""

from __future__ import print_function
from numpy import mean,median
import math
import os
import time
import random
import neat
from datetime import datetime 
import pickle
import visualize
from snakePlayer2 import SnakePlayer
import sys

S_RIGHT, S_LEFT, S_UP, S_DOWN = 0,1,2,3
XSIZE,YSIZE = 14,14
NFOOD = 1 


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    genome.fitness = median([runGame(net),runGame(net),runGame(net),runGame(net),runGame(net),runGame(net)])
    return genome.fitness

# This outline function provides partial code for running the game with an evolved agent
# There is no graphical output, and it runs rapidly, making it ideal for
# you need to modify it for running your agents through the game for evaluation
# which will depend on what type of EA you have used, etc.
# Feel free to make any necessary modifications to this section.
def runGame(net):
    snake = SnakePlayer()
    totalScore = 0
    snake._reset()
    food = placeFood(snake)
    timer = 0
    while not snake.snakeHasCollided() and not timer == 2*XSIZE * YSIZE:

        ## EXECUTE THE SNAKE'S BEHAVIOUR HERE ##
        output = net.activate(snake.eyes())
        direction = output.index(max(output))
        snake.direction = direction
        #print(direction)

        snake.updatePosition()

        if snake.body[0] in food:
            snake.score += 1
            food = placeFood(snake)
            timer = 0
        else:    
            snake.body.pop()
            timer += 1 # timesteps since last eaten

        totalScore += snake.score

    snake.fitness = max(snake.score , float(timer)/(XSIZE*YSIZE))
    return snake.fitness

# This function places a food item in the environment
def placeFood(snake):
    food = []
    while len(food) < NFOOD:
        potentialfood = [random.randint(1, (YSIZE-2)), random.randint(1, (XSIZE-2))]
        #
        if not (potentialfood in snake.body) and not (potentialfood in food) and not potentialfood[1]==4:
            food.append(potentialfood)

    snake.food = food  # let the snake know where the food is
    return( food )

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(2, eval_genome)
    start_time = datetime.now() 
    winner = p.run(pe.evaluate, 2000)
    time_elapsed = datetime.now() - start_time 
    print('Run: Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
    
    stats.save_genome_fitness(',','fitness_history' + str(V) + '.csv')

    with open('winner' +str(V) +'.gen','wb') as f:
        pickle.dump(winner,f)


V = sys.argv[1]
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
