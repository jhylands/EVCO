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

	def getAheadLocation(self):
		self.ahead = [ self.body[0][0] + (self.direction == S_DOWN and 1) + (self.direction == S_UP and -1), self.body[0][1] + (self.direction == S_LEFT and -1) + (self.direction == S_RIGHT and 1)] 

	def get2headLocation(self,location,steps):
		return [ location[0] + (self.direction == S_DOWN and steps) + (self.direction == S_UP and -steps), location[1] + (self.direction == S_LEFT and -steps) + (self.direction == S_RIGHT and steps)] 

	def updatePosition(self):
		self.getAheadLocation()
		self.body.insert(0, self.ahead )

	def eyes(self):
		return  [self.direction==a for a in [0,1,2,3]] + self.sonar()

	def sonar(self):
		theMap = numpy.zeros((14,14))
		for part in self.body:
			theMap[part[0],part[1]]-=1
		theMap[self.food[0][0],self.food[0][1]]+=1
		
		

		return list(numpy.array(theMap).flatten())


	def snakeHasCollided(self):
		self.hit = False
		if self.body[0] in self.body[1:]: self.hit = True
		if self.body[0][0] == 0 or self.body[0][0] == (YSIZE-1) or self.body[0][1] == 0 or self.body[0][1] == (XSIZE-1): self.hit = True
		return( self.hit )
