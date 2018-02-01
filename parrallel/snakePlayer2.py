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
		#distance to wall
		self.direction
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
		foodahead = [int(self.getAheadLocation()in self.food),int(self.get2headLocation(self.body[0],2) in self.food)]
		state = [int(self.direction==a) for a in [0,1,2,3]] + foodahead+ self.sonar()
		#print (state)
		return  state

	def sonar(self):
		theMap = numpy.zeros((14,14))
		for part in self.body:
			theMap[part[0],part[1]]+=1
		x = self.body[0][0]
		y = self.body[0][1]
		A = [theMap[min(x+1,13),y],theMap[max(x-1,0),y],
theMap[x,min(y+1,13)],theMap[x,max(y-1,0)],

theMap[min(x+2,13),y],theMap[max(x-2,0),y],
theMap[x,min(y+2,13)],theMap[x,max(y-2,0)],

theMap[min(x+1,13),min(y+1,13)],theMap[max(x-1,0),min(y+1,13)],theMap[min(x+1,13),max(y-1,0)],theMap[max(x-1,0),max(y-1,0)]]
		B = [x+1==14,x-1==-1,y+1==14,y-1==-1,
x+2==14,x-2==-1,y+2==14,y-2==-1,
0,0,0,0]
		
		
		return [int(max(a,b)) for a,b in zip(A,B)]


	def snakeHasCollided(self):
		self.hit = False
		if self.body[0] in self.body[1:]: self.hit = True
		if self.body[0][0] == 0 or self.body[0][0] == (YSIZE-1) or self.body[0][1] == 0 or self.body[0][1] == (XSIZE-1): self.hit = True
		return( self.hit )
