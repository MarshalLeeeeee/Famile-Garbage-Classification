class CarCenter(threading.Thread):

	garbageType = 0
	cars = []
	freeCars = []
	busyCars = []
	carCondition = threading.Condition()

	def __init__(self, garbageType):
		super().__init__()
		self.cars = []
		self.freeCars = []
		self.busyCars = []
		self.garbageType = garbageType
		self.carCondition = threading.Condition()

	def addCar(self, c):
		if(c not in self.cars and self.carCondition.acquire()):
			self.cars.append(c)
			self.freeCars.append(c)
			self.carCondition.release()
			return 1
		else:
			return 0

	def deleteCar(self, c):
		if(c in self.freeCars and self.carCondition.acquire()):
			self.freeCars.remove(c)
			self.cars.remove(c)
			self.carCondition.release()
			return 1
		else:
			return 0

	def free(self, c):
		if(c in self.busyCars and self.carCondition.acquire()):
			self.busyCars.remove(c)
			self.freeCars.append(c)
			self.carCondition.release()
			return 1
		else:
			return 0

	def dispatch(self):
		# always receiving the message from the collector
		# if some collector are full of garbage, then dispatch cars
		while(True):
			if(self.garbageType == 0):
				global garbageDamageFull, garbageDamageFullCondition
				freeNum = len(freeCars)
				fullNum = len(garbageDamageFull)
				if garbageDamageFullCondition.acquire() and self.carCondition.acquire():
					if(freeNum > fullNum):
						busyCars += freeCars[:fullNum]
						freeCars = freeCars[fullNum:]
						garbageDamageFull = []
					else:
						busyCars += freeCars
						freeCars = []
						garbageDamageFull = [freeNum:]
					self.carCondition.release()
					garbageDamageFullCondition.release()
			if(self.garbageType == 1):
				global garbageOrganFull, garbageOrganFullCondition
				freeNum = len(freeCars)
				fullNum = len(garbageOrganFull)
				if garbageOrganFullCondition.acquire() and self.carCondition.acquire():
					if(freeNum > fullNum):
						busyCars += freeCars[:fullNum]
						freeCars = freeCars[fullNum:]
						garbageOrganFull = []
					else:
						busyCars += freeCars
						freeCars = []
						garbageOrganFull = [freeNum:]
					self.carCondition.release()
					garbageOrganFullCondition.release()
			if(self.garbageType == 2):
				global garbageInorgFull, garbageInorgFullCondition
				freeNum = len(freeCars)
				fullNum = len(garbageInorgFull)
				if garbageInorgFullCondition.acquire() and self.carCondition.acquire():
					if(freeNum > fullNum):
						busyCars += freeCars[:fullNum]
						freeCars = freeCars[fullNum:]
						garbageInorgFull = []
					else:
						busyCars += freeCars
						freeCars = []
						garbageInorgFull = [freeNum:]
					self.carCondition.release()
					garbageInorgFullCondition.release()