from pprint import pprint
import json
import sys
from numpy import *
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib
import pylab as pl

def view(fname):
	with open(fname) as jFile:
		data = json.load(jFile)

def getPoints(fname):
	with open(fname) as jFile:
		data = json.load(jFile)

	attPeriod = []
	defPeriod = []
	attPayoff = []
	defPayoff = []

	profiles = data['profiles']
	
	for pr in profiles:
		if int((((pr['symmetry_groups'])[1])['strategy'].split('-'))[1]) == 3:
			continue
		for items in pr['symmetry_groups']:
			if(items['role'] == 'ATT'):
				attPeriod.append(int((items['strategy'].split('-'))[1]))
				attPayoff.append(float(items['payoff']))
			elif(items['role'] == 'DEF'):
				defPeriod.append(int((items['strategy'].split('-'))[1]))
				defPayoff.append(float(items['payoff']))

	ratio = [(t[0]/t[1]) for t in zip(defPayoff, attPayoff)]
	# pprint(ratio)
	for item in zip(attPeriod, defPeriod, ratio):
		print item
	fig = pl.figure()
	ax = p3.Axes3D(fig)
	ax.scatter3D(attPeriod, defPeriod, ratio)
	ax.set_xlabel('Attacker Period')
	ax.set_ylabel('Defender Period')
	ax.set_zlabel('Def payoff / Att payoff')

	pl.show()

	# pprint(defPeriod)
	# pprint(defPayoff)	



if __name__ == '__main__':
	getPoints(sys.argv[1])

