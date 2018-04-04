class DumpStation(threading.Thread):

	address = ''
	garbageType = -1
	garbageForCheck = []
	garbageCondition = threading.Condition()

	def __init__(self, address, garbageType):
		super().__init__()
		self.address = address
		self.garbageType = garbageType
		self.currentUsr = ''
		self.state = 0
		self.garbageCondition = threading.Condition()

	def dump(self, usrName, passWord):
		usr = returnUsr(usrName) # implement returnUsr in database related, return dictionary
		if(usrName.type == 2 and hashlib.sha224(passWord.encode('utf-8')).hexdigest() == usr['encrypt']):
			if self.garbageCondition.acquire():
				self.garbageForCheck += car.garbage
				self.garbageCondition.release()
			if(self.garbageType == 0):
				damageCarCenter.free(usrName)
			if(self.garbageType == 1):
				organCarCenter.free(usrName)
			if(self.garbageType == 2):
				inorgCarCenter.free(usrName)
			return 1
		else:
			# the password and the username is not correct
			return 0

	def check(self):
		# keep checking if garbageForCheck contains any garbage
		# if so, check them
		while(True):
			if len(garbageForCheck) and self.carCondition.acquire():
				result = exam(garbageForCheck[0])
				upload(result)
				if (len(garbageForCheck) == 1):
					garbageForCheck = []
				else:
					garbageForCheck = garbageForCheck[1:]
				self.carCondition.release()
			time.sleep(2.1)

	def exam(garbage):
		if (self.garbageType == 0):
			if not damageGarbageLike(garbage):
				flag = 1
			else:
				flag = 0
		if (self.garbageType == 1):
			if not organGarbageLike(garbage):
				flag = 1
			else:
				flag = 0
		if (self.garbageType == 2):
			if not inorgGarbageLike(garbage):
				flag = 1
			else:
				flag = 0
		if (flag):
			raisePenalty(garbage.info)
		else:
			raiseReward(garbage.info)

	def raisePenalty(usrName):
		pass

	def raiseReward(usrName):
		pass