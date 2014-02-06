import random
import copy

def enum(**enums):
    """Defines enum types. Use by Obj=enum(dict)"""
    return type('Enum', (), enums)

class State(object):
    """Includes all the state information required for the agents to make decisions"""
 
    def __init__(self, *args, **kwargs):
        try:
            self.debug = kwargs['debug']
        except KeyError:
            self.debug = 0
            pass
        self.currentTime = 0
        self.activeResources = {}
        self.inactiveResources = {}
        self.stateHistory = {}

        #Declare and pass the enumeration objects for the players and the server states
        healthEnum = enum({COMPR=-1, PROBED=0, HEALTHY=1})
        playerEnum = enum({DEF=0, ATT=1})
        self.rArgs = {'healthState':healthEnum, 'players':playerEnum}
        
        #Initialize the resources according to the resource list that has been given
        # for name in kwargs['ResourceList']:
        #     self.rArgs['name'] = name
        #     res = Resource(self.rArgs)
        #     res.report()
        #     self.activeResources[name] = res
        self.addResource(kwargs['ResourceList'])
        if(self.debug):
            for k,v in activeResources.iteritems():
                print k + '\n' + v.report()

    def addResource(self, *args):
        for name in args:
            self.rArgs['name'] = name
            self.activeResources[name] = Resources(self.rArgs)
            self.activeResources[name].report()
        try:
            del rArgs['name']
        except KeyError:
            pass

    def getResource(self, *args):
        result = {}
        for name in args:
            t = self.activeResources.get(name)
            t = t if t else self.inactiveResources.get(name)
            if(t):
                result[name] = t
        if(self.debug):
            for k,v in results.iteritem():
                print k + '\n' + v.report()
        return result

    def recordHistory(self):
        state = {}
        t = {}
        for name, value in self.activeResources.iteritems():
            t[name] = value.report()
        state['activeResources'] = t
        t = {}
        for name, value in self.inactiveResources.iteritems():
            t[name] = value.report()
        state['inactiveResources'] = t
        stateHistory[self.currentTime] = state
        if(self.debug):
            for name,value in stateHistory.iteritems():
                print name, value

    def updateState(self):
        self.recordHistory()
        self.updateTime()
        

class Resource(object):
    """Keeps a track of the server resources being monitored. Initialize by giving enum object of player types and health states in dict
        Initialization: Resource({healthStates:healthEnum, players:playerEnum})
    """
    
    def __init__(self, *args, **kwargs):
        self.name = kwargs(name)
        self.stateEnum = kwargs(healthStates)
        self.playerEnum = kwargs(players)
        self.probesTillNow = 0
        self.probCompromise = 0
        self.reimageCount = 0
        self.totalDowntime = 0
        self.Status = self.stateEnum.HEALTHY
        self.controlledBy = self.playerEnum.DEF

    def report(self):
        return({"Status":self.Status,
                "Probes till now":self.probesTillNow,
                "Probability of Compromise":self.probCompromise,
                "Reimage Count":self.reimageCount,
                "Total Downtime":self.totalDowntime,
                "Control": self.controlledby})

    def getStatus(self):
        return(self.Status)

    def changeStatus(self, status):
        if(status == self.stateEnum.COMPR):
            self.Status = self.stateEnum.COMPR
        elif(status == self.stateEnum.PROBED):
            self.Status = self.stateEnum.PROBED
        else:
            self.Status = self.stateEnum.HEALTHY

    def probe(self):
        self.probesTillNow += 1
        self.incrementProb()

    def attack(self):
        if(isCompromised()):
            self.changeStatus(self.stateEnum.COMPR)
            self.controlledBy = self.playerEnum.ATT
        else:
            self.changeStatus(self.stateEnum.PROBED)

    def incrementProb(self):
        """Increment probability of compromise depending on curve used"""
        #Placholder linear increasing method
        self.probCompromise += 0.1      

    def isCompromised(self):
        #Currently uses a simple random uniform sampling.
        random.seed()
        rand = random.random()
        if rand<self.probCompromise:
            return 1
        else:
            return 0

    def reImage(self):
        self.probCompromise = 0
        self.reimageCount += 1
        self.changeStatus(1)

    