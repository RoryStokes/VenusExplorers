import numpy

#dictionary of cardinal directions indexed by their label character
_directions = {"N":numpy.array((0,1)),"S":numpy.array((0,-1)),"E":numpy.array((1,0)),"W":numpy.array((-1,0))}
#2x2 rotation matrices for the 90 degree rotations
_left = numpy.array([[0,-1],[1,0]])
_right = numpy.array([[0,1],[-1,0]])

class Explorer:

	def __init__(self,x,y,facing,bounds):
		#position is stored in a numpy array for efficient modification
		self.pos    = numpy.array((x,y))
		#grid bounds are stored to ensure explorer does not leave grid
		self.bounds = numpy.array(bounds)

		if facing in _directions.keys():
			#sets the direction to a unitary vector in the target direction, fetched from the cardinal direction directory
			self.direction = _directions[facing]

	def turnLeft(self):
		#multiply direction vector by rotation matrix
		self.direction = _left.dot(self.direction)

	def turnRight(self):
		#multiply direction vector by rotation matrix
		self.direction = _right.dot(self.direction)

	def move(self):
		#add the current direction vector to position
		target = self.pos + self.direction

		#test to see if new position is within bounds
		if (target>self.bounds[2:3]).any() or (target<self.bounds[0:1]).any():
			#if not, output an error and make no movement
			print("Error: movement out of bounds")
			return False
		else:
			#if position within bounds, make the movement
			self.pos = target
			return True

	def getX(self):
		#returns the x component of the current position
		return self.pos[0]

	def getY(self):
		#returns the y component of the current position
		return self.pos[1]

	def getFacing(self):
		#fetches the relevant character from the cardinal direction dictionary and returns
		for char, vector in _directions.items():
			if numpy.array_equal(vector, self.direction):
				return char
		#if no matches are found (should not be possible), display an error
		print("Error: facing in non-cardinal direction")
		return False