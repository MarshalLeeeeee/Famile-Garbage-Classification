class CrewCenter:

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

	def dispatch(self):
		# receive message from Hub
		# the message include the address of the collector with error
		if self.crewCondition.acquire():
			# you may consider the error list length...
			freeNum = len(freeCrew)
			if(freeNum > errorlen):
				busyCrew += freeCrew[:errorlen]
				freeCrew = freeCrew[errorlen:]
				# update the error list
			else:
				busyCrew += freeCrew
				freeCrew = []
				# update the error list
			self.crewCondition.release()

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