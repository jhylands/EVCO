import neat
import os
import pickle
import random 
import curses
import sys
from snakePlayerD import SnakePlayer

S_RIGHT, S_LEFT, S_UP, S_DOWN = 0,1,2,3
XSIZE,YSIZE = 14,14
NFOOD = 1 
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

def displayStrategyRun(net):
    snake = SnakePlayer()

    curses.initscr()
    win = curses.newwin(YSIZE, XSIZE, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)
    win.timeout(120)

    snake._reset()
    food = placeFood(snake)

    for f in food:
        win.addch(f[0], f[1], '@')

    timer = 0
    collided = False
    while not collided and not timer == (XSIZE * YSIZE):

        # Set up the display
        win.border(0)
        win.addstr(0, 2, 'Score : ' + str(snake.score) + ' ')
        win.getch()

        ## EXECUTE THE SNAKE'S BEHAVIOUR HERE ##
        outputer = net.activate(snake.eyes())
        direction = outputer.index(max(outputer))
        snake.direction = direction
        snake.updatePosition()
        if snake.body[0] in food:
            snake.score += 1
            for f in food: win.addch(f[0], f[1], ' ')
            food = placeFood(snake)
            for f in food: win.addch(f[0], f[1], '@')
            timer = 0
        else:    
            last = snake.body.pop()
            win.addch(last[0], last[1], ' ')
            timer += 1 # timesteps since last eaten
        win.addch(snake.body[0][0], snake.body[0][1], 'o')

        collided = snake.snakeHasCollided()
        hitBounds = (timer == ((2*XSIZE) * YSIZE))

    curses.endwin()
    snake.fitness = snake.score + float(timer)/(XSIZE*YSIZE)
    #print collided
    #print hitBounds
    #raw_input("Press to continue...")
    return snake.fitness
V = sys.argv[1]
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
with open('winner' + V +'.gen','rb') as f:
	c = pickle.load(f)

net = neat.nn.FeedForwardNetwork.create(c, config)

displayStrategyRun(net)
