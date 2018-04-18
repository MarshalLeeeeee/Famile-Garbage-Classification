class Collector

	address = ''
	state = 0
	# 0: idle state
	# 1: family loggin
	# 2: collector loggin
	# 3: repair max loggin
	space = [100,100,100]
	# in our simulation the space is discrete
	usedSpace = [0,0,0]
	threshold = 0.5
	timeGap = 2.0
	currentUsr = ''
	garbage = [[],[],[]]

	def __init__(self, address, space = [100,100,100], threshold = 0.5, state = 0, debug = False, timeGap = 2.0):
		super().__init__()
		self.address = address
		self.space = space[:3]

		if(threshold > 0 and threshold <= 1):
			self.threshold = threshold
		else:
			self.threshold = 0.5

		if(debug):
			self.state = state
		else:
			self.state = 0

		self.currentUsr = ''
		self.timeGap = timeGap
		garbage = [[],[],[]]
		usedSpace = [0,0,0]

	def send(self):
		# do it periodically
		while(1):
			# send the message to hub
			time.sleep(timeGap)

	def logIn(self, usrName, passWord):
		usr = returnUsr(usrName) # implement returnUsr in database related, return dictionary
		if(hashlib.sha224(passWord.encode('utf-8')).hexdigest() == usr['encrypt']):
			self.state = usr['identity']
			self.currentUsr = usrName
			return 1
		else:
			# the password and the username is not correct
			return 0

	def logOut(self):
		if(state == 3):
			global errorFlagCondition, errorFlag, crewCenter
			if errorFlagCondition.acquire():
				errorFlag[self.address] = False
				errorFlagCondition.release()
			crewCenter.free(account(self.currentUsr))
		self.state = 0
		self.currentUsr = ''

	def QTgenerate(self, garbageType,garbage):
		if(self.state != 1):
			return [-1,'']
		else:
			self.usedSpace[garbageType] += 1
			self.garbage[garbageType] += grabage
			examSpace()
			return [garbageType,self.currentUsr]

	def examSpace(self):
		for i in range(4):
			if(self.usedSpace[i] > self.space[i] *self. threshold):
				callCar(i)

	def callCar(self, garbageType):
		if(garbageType == 0):
			global garbageDamageFull, garbageDamageFullCondition
			if self.address not in garbageDamageFull:
				if garbageDamageFullCondition.acquire():
					garbageDamageFull.append(self.address)
					garbageDamageFullCondition.release()
		if(garbageType == 1):
			global garbageOrganFull, garbageOrganFullCondition
			if self.address not in garbageOrganFull:
				if garbageOrganFullCondition.acquire():
					garbageOrganFull.append(self.address)
					garbageOrganFullCondition.release()
		if(garbageType == 2):
			global garbageInorgFull, garbageInorgFullCondition
			if self.address not in garbageInorgFull:
				if garbageInorgFullCondition.acquire():
					garbageInorgFull.append(self.address)
					garbageInorgFullCondition.release()

	def spaceSet(self,space):
		if(self.state != 3):
			return 0
		for i in range(3):
			if(space[i] < self.usedSpace[i]):
				flag = 0
				break
		if(flag):
			self.space = space[:3]
			examSpace()
			return 1
		else:
			return 0

	def thresholdSet(self, threshold):
		if(self.state != 3):
			return 0
		if(threshold > 0 and threshold <= 1):
			self.threshold = threshold
			examSpace()
			return 1
		else:
			return 0

	def returnSpace(self):
		if(self.state != 3):
			return [-1,-1,-1]
		else:
			return self.space

	def returnUsedSpace(self):
		if(self.state != 3):
			return [-1,-1,-1]
		else:
			return self.usedSpace

	def collectGarbage(self, garbageType):
		if(self.state != 2):
			return 0
		else:
			g = self.garbage[garbageType]
			self.usedSpace[garbageType] = 0
			self.garbage[garbageType] = []
			return g