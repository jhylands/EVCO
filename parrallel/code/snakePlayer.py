S_RIGHT, S_LEFT, S_UP, S_DOWN = 0,1,2,3
XSIZE,YSIZE = 14,14
NFOOD = 1 # NOTE: YOU MAY NEED TO ADD A CHECK THAT THERE ARE ENOUGH SPACES LEFT FOR THE FOOD (IF THE TAIL IS VERY LONG)
import numpy
# This class can be used to create a basic player object (snake agent)
class SnakePlayer(list):
	global S_RIGHT, S_LEFT, S_UP, S_DOWN
	global XSIZE, YSIZE

	def __init__(self):
		self.direction = S_DOWN
		self.body = [ [4,10], [4,9], [4,8], [4,7], [4,6], [4,5], [4,4], [4,3], [4,2], [4,1],[4,0] ]
		self.score = 0
		self.ahead = []
		self.food = []

	def _reset(self):
		self.direction = S_DOWN
		self.body[:] = [ [4,10], [4,9], [4,8], [4,7], [4,6], [4,5], [4,4], [4,3], [4,2], [4,1],[4,0] ]
		self.score = 0
		self.ahead = []
		self.food = []
		self.last_direction = S_DOWN
		self.time_in_direction=0

	def getAheadLocation(self):
		self.ahead = [ self.body[0][0] + (self.direction == S_DOWN and 1) + (self.direction == S_UP and -1), self.body[0][1] + (self.direction == S_LEFT and -1) + (self.direction == S_RIGHT and 1)] 

	def updatePosition(self):
		self.getAheadLocation()
		self.body.insert(0, self.ahead )

	def eyes(self):
		# map = numpy.zeros((14,14))
		# for part in self.body:
		# 	map[part[0],part[1]]-=1
		# for bit in self.food:
		# 	map[part[0],part[1]]+=5
		# smap = range(0,49)

		# for X in range(0,48):

		# 	x = X%7
		# 	y = X/7-x
		# 	#print [x,y]
		# 	smap[X] = sum([map[x,y],map[abs(x-1),abs(y-1)],map[x,abs(y-1)],map[abs(x-1),y]])
		#wall_in_front = self.body[0][1] ==0 or
#S_RIGHT, S_LEFT, S_UP, S_DOWN = 0,1,2,3
		#distance to wall
		self.direction
		self.time_in_direction = self.time_in_direction+1 if self.last_direction==self.direction else 1
		self.last_direction=self.direction
		distance_to_wall = [self.body[0][0],14-self.body[0][0],self.body[0][1],14-self.body[0][1]]
		#food direction
		x = self.body[0][0]-self.food[0][0]
		y = self.body[0][1]-self.food[0][1]
		goRight = x<0
		goDown = y<0
		if abs(x)>abs(y):
			foodD =  0 if goRight else 1
		else:
			foodD = 3 if goDown else 2
		return  [self.direction==a for a in [0,1,2,3]] + [foodD==a for a in [0,1,2,3]] + distance_to_wall + [self.time_in_direction]

	def snakeHasCollided(self):
		self.hit = False
		if self.body[0] in self.body[1:]: self.hit = True
		if self.body[0][0] == 0 or self.body[0][0] == (YSIZE-1) or self.body[0][1] == 0 or self.body[0][1] == (XSIZE-1): self.hit = True
		return( self.hit )
