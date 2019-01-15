from Modules import waveForm
from Model import modele

import numpy as numpy
import torch
import pickle
import sys
def nearestNeighbor(dico, wavePosition):

	s = torch.nn.CosineSimilarity(dim=0)
	dist = 1000000
	name = ""
	for key in dico:
		tmp_dist = s(key, wavePosition[0])
		if  tmp_dist < dist:
			dist = tmp_dist
			name = dico[key]

	return name

def getMidiFromWave(folder, file):
	
	window_size = 172

	model2 = torch.load(folder + "model2.data")
	model2.eval()

	dico = pickle.load(open(folder + "dico.data", "rb"))

	w = waveForm.waveForm(file).getCQT()

	CQTs = []
	for i in range(len(w)//172 -1):
		CQTs.append(w[i*window_size : (i+1)*window_size])

	wraps = []
	for elem in CQTs:
		wraps.append(nearestNeighbor(dico, model2.forward(elem)))

	print(wraps)

if __name__ == "__main__":

	if len(sys.argv) == 3 :
		getMidiFromWave(sys.argv[1], sys.argv[2])


	else:
		print("Usage: Python3 WaveToMidi.py <folder for model> <file to convert>")  





