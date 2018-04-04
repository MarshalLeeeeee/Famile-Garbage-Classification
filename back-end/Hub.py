class Hub:
	# Hub read from the timestamp, but will not write to it
	# Hub write to errorFlag

	timeGap = 10.0
	timeLast = {}

	def __init__(self, timeGap = 10.0):
		super().__init__()
		self.timeGap = timeGap
		self.timeLast = {}

	def listen(self):
		# receive from each collector
		# and update timeLast, whose key is the address of the collector

	def timeGapSet(self, timegap):
		self.timeGap = timegap