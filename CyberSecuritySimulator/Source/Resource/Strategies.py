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

	def periodic(self, info):
		timePeriod = 2
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

	def periodic(self, info):
		timePeriod = 4
		nextReimage = info['currentTime'] + timePeriod

		defendOrder = sorted(info['resourceInfo'].items(), key = lambda x: x[1]['Probes till now'])
		nextAction = (nextReimage, defendOrder[-1])
		return nextAction