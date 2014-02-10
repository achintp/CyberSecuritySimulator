import Simulator

def testInput():
	params = {
			'startTime':0,
			'endTime':100,
			'ResourceList': ['ServerA', 'ServerB', 'ServerC'],
			'attackerList': {'A':'periodic'},
			'defenderList': {'D':'periodic'}
		}
	return params

def runSimulator(params):
	sim = Simulator.SimulateCyberScenario(params)
	sim.Simulate()

if __name__=='__main__':
	args = testInput()
	runSimulator(args)