import random

def enum(**enums):
    """Defines enum types. Use by Obj=enum(dict)"""
    return type('Enum', (), enums)

class State(object):
    """Includes all the state information required for the agents to make decisions"""


class Resource(object):
    """Keeps a track of the server resources being monitored. Initialize by giving enum object of player types and health states in dict"""
    
    def __init__(self, *args, **kwargs):
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
        if(status<0):
            self.Status = self.stateEnum.COMPR
        elif(status == 0):
            self.Status = self.stateEnum.PROBED
        else:
            self.Status = self.stateEnum.HEALTHY

    def probe(self):
        self.probesTillNow += 1
        incrementProb()

    def attack(self):
        if(isCompromised()):
            changeStatus(-1)
            self.controlledBy = self.playerEnum.ATT
        else:
            changeStatus(0)

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


    