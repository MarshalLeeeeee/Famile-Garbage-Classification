import hashlib

class Collector:

	address = ''
	state = 0
	# 0: idle state
	# 1: family loggin
	# 2: collector loggin
	# 3: repair max loggin
	space = [100,100,100,100]
	# in our simulation the space is discrete
	usedSpace = [0,0,0,0]
	threshold = 0.5
	currentUsr = ''

	def __init__(self, address, space = [100,100,100,100], threshold = 0.5):
		self.address = address
		self.space = space[:4]

		if(threshold > 0 and threshold <= 1):
			self.threshold = threshold
		else:
			self.threshold = 0.5
		self.currentUsr = ''

	def logIn(usrName, passWord):
		usr = returnUsr(usrName) # implement returnUsr in database related, return dictionary
		if(hashlib.sha224(passWord.encode('utf-8')).hexdigest() == usr['encrypt']):
			self.state = usr['identity']
			self.currentUsr = usrName
			return 1
		else
			# the password and the username is not correct
			return 0

	def logOut():
		self.state = 0
		self.currentUsr = ''

	def QTgenerate(garbageType):
		if(self.state != 1):
			return [-1,'']
		else:
			self.usedSpace[garbageType] += 1
			examSpace()
			return [garbageType,self.currentUsr]

	def examSpace():
		for i in range(4):
			if(self.usedSpace[i] > self.space[i] *self. threshold):
				callCar(i)

	def callCar(garbageType):
		return garbageType

	def spaceSet(space):
		if(self.state != 3):
			return 0
		for i in range(4):
			if(space[i] < self.usedSpace[i]):
				flag = 0
				break
		if(flag):
			self.space = space[:4]
			examSpace()
			return 1
		else:
			return 0

	def thresholdSet(threshold):
		if(self.state != 3):
			return 0
		if(threshold > 0 and threshold <= 1):
			self.threshold = threshold
			examSpace()
			return 1
		else:
			return 0

	def retrunSpace():
		if(self.state != 3):
			return [-1,-1,-1,-1]
		else:
			return self.space

	def retrunUsedSpace():
		if(self.state != 3):
			return [-1,-1,-1,-1]
		else:
			return self.usedSpace

	def collectGarbage(garbageType):
		if(self.state != 2):
			return 0
		else:
			self.usedSpace[garbageType] = 0
