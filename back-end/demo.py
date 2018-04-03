import dump_station
import threading
import time
import hashlib

################################
################################
##  #  #                #  #  ##
##   ##                  ##   ##
##  #  #                #  #  ##
##            ###             ##
##            ###             ##
##                            ##
##      ##            ##      ##
##       ##          ##       ##
##        ##        ##        ##
##         ##########         ##
################################
################################

timeStampCondition = threading.Condition()
errorFlagCondition = threading.Condition()
garbageDamageFullCondition = threading.Condition()
garbageOrganFullCondition = threading.Condition()
garbageInorgFullCondition = threading.Condition()
#crewCondition = threading.Condition()
#carCondition = threading.Condition()

# each collector send message to tell the hub if it is still in connection
# keys are the address of the collector
timeStamp = {} 

# record the address of collectors if some collector is broken
errorFlag = []

# a list record the address of collectors that requires garbage cars
garbageDamageFull = []
garbageOrganFull = []
garbageInorgFull = []

class Hub(threading.Thread):
	# Hub read from the timestamp, but will not write to it
	# Hub write to errorFlag

	timeGap = 10.0
	timeLast = {}

	def __init__(self, timeGap = 10.0):
		super().__init__()
		self.timeGap = timeGap
		self.timeLast = {}

	def run(self):
		global timeStampCondition, errorFlagCondition, timeStamp, errorFlag
		while(True):
			if timeStampCondition.acquire():
				for collector in timeStamp:
					self.timeLast[collector] = timeStamp[collector]
				timeStampCondition.release()
			currTime = time.time()
			if errorFlagCondition.acquire():
				for collector in self.timeLast:
					if(currTime - self.timeLast[collector] > self.timeGap and collector not in errorFlag):
						errorFlag.append(collector)
				errorFlagCondition.release()
			time.sleep(timeGap/5.0)

	def timeGapSet(self, timegap):
		self.timeGap = timegap

hub = Hub()
hub.start()
		
class CrewCenter(threading.Thread):

	crew = []
	freeCrew = []
	busyCrew = []
	crewCondition = threading.Condition()

	def __init__(self):
		super().__init__()
		self.crew = []
		self.freeCrew = []
		self.busyCrew = []
		crewCondition = threading.Condition()

	def run(self):
		global errorFlagCondition, errorFlag
		while(True):
			if errorFlagCondition.acquire() and self.crewCondition.acquire():
				errorlen = len(errorFlag)
				freeNum = len(freeCrew)
				if(freeNum > errorlen):
					busyCrew += freeCrew[:errorlen]
					freeCrew = freeCrew[errorlen:]
					errorFlag = []
				else:
					busyCrew += freeCrew
					freeCrew = []
					errorFlag = [freeNum:]
				self.crewCondition.release()
				errorFlagCondition.release()
			time.sleep(2.0)


	def addCrew(self, c):
		if c not in self.crew and self.crewCondition.acquire():
			self.crew.append(c)
			self.freeCrew.append(c)
			self.crewCondition.release()
			return 1
		else:
			return 0

	def deleteCrew(self, c):
		if (c not in self.crew or c in self.busyCrew):
			return 0
		else
			if self.crewCondition.acquire():
				self.crew.remove(c)
				self.freeCrew.remove(c)
				self.crewCondition.release()
				return 1

	def free(self, c):
		if c in self.busyCrew and self.crewCondition.acquire():
			self.busyCrew.remove(c)
			self.freeCrew.append(c)
			self.crewCondition.release()
			return 1
		else:
			return 0

crewCenter = CrewCenter()
crewCenter.start()

class Collector(threading.Thread):

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

	def run(self):
		global timeStampCondition, timeStamp
		while(1):
			if timeStampCondition.acquire():
				timeStamp[address] = time.time()
				timeStampCondition.release()
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

	def QTgenerate(self, garbageType):
		if(self.state != 1):
			return [-1,'']
		else:
			self.usedSpace[garbageType] += 1
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
			self.usedSpace[garbageType] = 0


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

	def run(self):
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
			time.sleep(2.0)

damageCarCenter = CarCenter(0)
organCarCenter = CarCenter(1)
inorgCarCenter = CarCenter(2)

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

	def run(self):
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

