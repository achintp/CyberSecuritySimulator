import Resource.StateClasses as StateClasses
import Resource.AgentClasses as AgentClasses
import Resource.Strategies as Strategies
import Resource.Utility as Utility
import copy
import time
from pprint import pprint

class SimulateCyberScenario(object):
	"""
		Simulator class, framework for running games
	"""
	def __init__(self, args):

		"""
			Pass in args as a dict. Include:
			startTime - event horizon start
			endTime - event horizon end
			resourceList - list of resource names
			attackerList - k,v pair of name, strategy
			defenderList - k,v pair of name, strategy
			dtCost - cost of unit downtime
			prCost - cost of unit probe
			DEF - []
			ATT - []
		"""
	#Initialize the state variable. Internally will initialize
	#the resources
		self.params = {}
		self.params['startTime'] = args['startTime']
		self.params['endTime'] = args['endTime']
		self.params['currentTime'] = 0
		self.attackerList = []
		self.defenderList = []
		self.debug = 1
		self.params['resourceReports'] = {}
		self.gameState = 1

		#Construct utility parameters
		self.utilParams = {}
		self.utilParams['dtCost'] = args['dtCost']
		self.utilParams['prCost'] = args['prCost']
		self.utilParams['DEF'] = args['DEF']
		self.utilParams['ATT'] = args['ATT']

		#Initialize the event queue
		f = (self.params['endTime'], 0, -1)
		# self.eventQueue = list(tuple(self.params['endTime'], 0, -1))
		self.eventQueue = [f]
		#Initialize the state variable
		self.state = StateClasses.State(**{'ResourceList':args['ResourceList'], 'alpha':args['alpha']})
		self.params['resourceReports'] = self.state.resourceReportsList

		#Initialize the agents
		for k,v in args['attackerList'].iteritems():
			d = {
				'name':k,
				'strategy':v,
				'resourceList':args['ResourceList'],
				'time': self.params['currentTime']
			}
			self.attackerList.append(AgentClasses.Attacker(**d))

		for k,v in args['defenderList'].iteritems():
			d = {
				'name':k,
				'strategy':v,
				'resourceList':args['ResourceList'],
				'time': self.params['currentTime']
			}
			self.defenderList.append(AgentClasses.Defender(**d))

			#print "Simulator set up. The resources are "
			#for name in args['ResourceList']:
			#	print name
			#print "\nThe players are " + self.attackerList[0].name + " and " +\
			#self.defenderList[0].name

		if(self.debug):
			print self.attackerList
			print self.defenderList

	def askAttacker(self):
		"""
			Asks the attacker about the next attack.
			Adds next event to the eventQueue
			Update the information the agent has and then
			ask for the next action
		"""
		d = dict(self.params['resourceReports'])
		d['time'] = self.params['currentTime']
		for att in self.attackerList:
			att.updateInformation(d)
			nextEvent = att.getAction()
			if nextEvent == -1: return

			for index, items in enumerate(self.eventQueue):
				if items[2] == 0:
					self.eventQueue.pop(index)

			self.eventQueue.append(nextEvent)

		self.sortEventQueue()

		if(self.debug):
			print self.eventQueue

	def askDefender(self):
		"""
			Analogous to attacker 
		"""
		for items in self.eventQueue:
			if(items[2] == 1): 
				#print "Defender Action exists-------------------"
				#print items
				return

		d = dict(self.params['resourceReports'])
		d['time'] = self.params['currentTime']
		for defs in self.defenderList:
			defs.updateInformation(d)
			nextEvent = defs.getAction()
			if nextEvent == -1:
				return
			self.eventQueue.append(nextEvent)

		self.sortEventQueue()
		if(self.debug):
			print self.eventQueue

	def sortEventQueue(self):
		self.eventQueue = sorted(self.eventQueue)

	def executeAction(self):
		"""
			Picks the next action from the event queue and
			executes it.
		"""
		#self.printEvents()
		#Check whether the event horizon has ended
		nextEventTime = self.eventQueue[0][0]
		if(nextEventTime > self.params['endTime']):
			print "Game over"
			self.gameState = 0
			return
		else:
			#remove next event from the queue
			it = self.eventQueue.pop(0)
			if self.debug:
				print "Event popped-------------------"
				print it
				#print it[1][0]

			self.params['currentTime'] = it[0]
			#print "The time is: " + str(self.params['currentTime'])
			if(it[2] == 0 or it[2] == 1):
				res = self.state.getResource(*[it[1][0]])
				r = res[it[1][0]]
			elif(it[2] == 2):
				res = self.state.getResource(*[it[1]])
				r = res[it[1]]
			elif(it[2] == -1):
				#print "Game is over\n\n"
				self.gameState = 0
				return 0
			else:
				raise Exception("Unknown command executed")
			

			if(self.debug):
				print "Resource acquired--------------"
				print r

			if(it[2] == 1):
				#Reimage event, defender action
				#Grab defender, make them execute reimage on
				#mentioned resource
				#print "Reimaging now?----------------------"
				if self.debug:
					print "D is reimaging " + r.name
				d = self.defenderList[0]
				t = d.reImage(r)

				 #remove from attackers control list
				a = self.attackerList[0]
				a.loseControl([it[1][0]])

				 #add downtime event
				waketime = self.params['currentTime'] + t[0]
				self.eventQueue.append((waketime, it[1][0], 2))
				if self.debug:
					print r.name + " is DOWN. Will be up again at " + str(waketime)

				 #modify inactive list of state
				self.state.inactiveResources[it[1][0]] = self.state.activeResources[it[1][0]]
				del self.state.activeResources[it[1][0]]
				self.flushEventQueue(r.name)
				#print self.state.activeResources
				#print self.state.inactiveResources

				self.sortEventQueue()
			elif(it[2] == 0):
				#Probe event followed by attack event
				#Grab attacker, execute probe, then execute attack
				if self.debug:
					print "A is probing and attacking " + r.name
				a = self.attackerList[0]
				# r = self.state.getResource(*list(it[1][0]))
				r = a.probe(r)
				r = a.attack(r)
			elif(it[2] == 2):
				#Downtime over for resource
				if self.debug:
					print it[1] + " is up and running again"
				self.state.activeResources[it[1]] = self.state.inactiveResources[it[1]]
				del self.state.inactiveResources[it[1]]
				#print "Resource Activated---------------------\n\n"
				#print self.state.activeResources
				r.changeStatus(1)

				#print "Resource up and running"
				#print r.report()
			elif(it[2] == -1):
				#print "Game is over"
				self.gameState = 0
				return 0

	def updateInformation(self):
		#print "Updating the state information\n"
		self.state.updateState(self.params['currentTime'])
		info = {}
		# info['resourceInfo'] = self.state.resourceReportsList
		info = self.state.resourceReportsList
		if(self.debug):
			print "Updating resource reports to"
			print self.state.resourceReportsList

		self.params['resourceReports'] = self.state.resourceReportsList
		info['time'] = self.params['currentTime']
		self.attackerList[0].updateInformation(info)
		self.defenderList[0].updateInformation(info)
		self.printEvents()

	def flushEventQueue(self, name):
		#print "Fush " + name
		#rm = False
		for index, items in enumerate(self.eventQueue):
			#print items
			if items[2] == 0:
				if items[1][0] == name:
					#print items, index
					rm = index
		try:
			t = self.eventQueue.pop(rm)
			#print "Removed"
			#print t
		except UnboundLocalError:
			#self.printEvents()
			pass


	def printEvents(self):
		print "\n-----------------------------------------------------------"
		print "The events queue is"
		for events in self.eventQueue:
			print "At time " + str(events[0]),
			if events[2] == 0:
				print self.attackerList[0].name + " will probe " + events[1][0]
			elif events[2] == 1:
				print self.defenderList[0].name + " will reimage " + events[1][0]
			elif events[2] == -1:
				print "Game will end."
			elif events[2] == 2:
				print events[1] + " will reactivate."
		print "-----------------------------------------------------------\n"	


	def Simulate(self):
		#Start the simulation and keeps it running

		while(self.gameState):
			self.updateInformation()
			self.askAttacker()
			self.askDefender()
			self.executeAction()
			#time.sleep(1)
			
			# if self.debug:
			# 	t = raw_input("Press to continue")
		self.params['currentTime'] = self.params['endTime']
		self.updateInformation()

		self.stateHistory = self.state.stateHistory
		u = Utility.Utility(self.utilParams)

		utilFunc = u.getUtility('simpleCIA')
		payoff = utilFunc(self.stateHistory)

		# for k,v in self.stateHistory.iteritems():
		# 	print k,
		# 	print v
		# 	print '\n'

		#pprint(self.stateHistory)

		if(self.debug):
			for k,v in self.stateHistory.iteritems():
				print k
				print v 
				print '\n\n'

		return payoff

















