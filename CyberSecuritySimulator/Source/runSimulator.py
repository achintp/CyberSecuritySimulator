import Simulator
import json

def readJson(jsonFolder):
	with open(jsonFolder + "/simulation_specs.json") as f:
		data = json.load(f)
	#print data

	assign = data["assignment"]
	config = data["configuration"]
	params = {}
	params['startTime'] = int(config["startTime"])
	params['endTime'] = int(config["endTime"])
	params['attackerList'] = assign["attackerList"]
	params['defenderList'] = assign["defenderList"]
	params['ResourceList'] = config["ResourceList"]

	return params

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
	#args = testInput()
	args = readJson("specs")
	runSimulator(args)