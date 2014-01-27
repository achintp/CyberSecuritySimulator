class StateInfo(object):
    """Includes all the state information required for the agents to make decisions"""


class Resource(object):
    """Keeps a track of the server resources being monitored"""
    
    def __init__(self, **kwargs):
        if not(kwargs):
            self.probeCount = 0
            self.compProb = 0
            self.state = 'Healthy'
            self.threshold = 0.9
            self.reImageCount = 0
            self.probesToAttack = []
        else:
            self.probeCount = kwargs[attackCount]
            self.compProb = kwargs[compProb]
            self.state = kwargs[state]

    def probe():
        if(self.state!='Compromised'):
            self.probeCount += 1
            if(self.state == 'Healthy'):
                self.state = 'Probed'
            #Incrementing the probability has to be implemented, placeholder method
            self.compProb += 0.1
            if(threshold <= self.compProb):
                self.state = 'Compromised'
                self.probesToAttack.append(probeCount)  #Keeps a track of the number of probes required to compromise every time

    def reImage():
        self.reImageCount += 1
        self.compProb = 0
        self.state = 'Healthy'
        