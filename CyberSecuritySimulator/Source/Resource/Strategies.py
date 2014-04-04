import random

class AgentStrategies(object):
	"""
		Base class for defining the agent strategies. Derive
		the defender and attacker strategy classes from this.
	"""

	def __init__(self, params):
		self.params = params

	def getStrategy(self, strategy):
		if hasattr(self, strategy):
			return getattr(self, strategy)

class AttackerStrategies(AgentStrategies):
	"""
		Defines the agent strategies
	"""

	def __init__(self, params):
		super(AttackerStrategies, self).__init__(params)

	def periodic(self, info, period):
		timePeriod = period
		nextAttack = info['currentTime'] + timePeriod

		attackOrder = sorted(info['resourceInfo'].items(), key = lambda x: x[1]['Probes till now'])

		namesList = []
		for k,v in info['resourceInfo'].iteritems():
			namesList.append(k)

		random.seed()
		index = random.randint(0, len(namesList)-1)
		#print "Random server is " + namesList[index]
		#Delete the entries where the attacker already has ciontrol 
		nextAction = (nextAttack, attackOrder[index])
		return nextAction


class DefenderStrategies(AgentStrategies):
	"""
		Defines the defender strategies
	"""
	def __init__(self, params):
		super(DefenderStrategies, self).__init__(params)

	def periodic(self, info, period):
		"""
		info = { 
			currentTime: v,
			resourceInfo:{
				name: report
			}
		}
		"""
		timePeriod = period
		nextReimage = info['currentTime'] + timePeriod

		defendOrder = sorted(info['resourceInfo'].items(), key = lambda x: x[1]['Probes till now'])
		nextAction = (nextReimage, defendOrder[-1])
		return nextAction

	def periodicRand(self, info, period):
		timePeriod = period
		nextReimage = info['currentTime'] + timePeriod

		resList = info['resourceInfo'].items()

		random.seed()
		index = random.randint(0, len(resList)-1)

		nextAction = (nextReimage, resList[index])
		return nextAction

	# def periodicInt(self, info, threshold):
		



