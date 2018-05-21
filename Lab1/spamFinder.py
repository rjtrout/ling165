__author__ = """Robert Trout (robert.trout@sjsu.edu)"""

import argparse, math


def train(labelsAndSubjects):
	spamList =[]
	hamList = []
	numHam = 1 # starting off with one extra for <UNK> later 
	numSpam = 1
	for x in labelsAndSubjects: # send spam words to spamList and ham words to hamList
		if x[0] == "0":
			hamList.extend(x[1].strip().split())
			numHam += 1
		elif x[0] == "1":
			spamList.extend(x[1].strip().split())
			numSpam += 1
	return spamList, hamList, numHam, numSpam


def checkFrequency(arrayOfWords):
	frequencyDict = {}
	for x in arrayOfWords:
		if x in frequencyDict:
			frequencyDict[x] += 1
		else:
			frequencyDict[x] = 2 # adding two to every word for laplace smoothing later
	frequencyDict['<UNK>'] = 1
	return frequencyDict

def changeToPercentage(dictOfFreq):
	frequencyDict = {}
	totalWords= float(sum(dictOfFreq.values()))
	for x in dictOfFreq:
		frequency = dictOfFreq[x]
		frequencyDict[x] = frequency/totalWords
	return frequencyDict


if __name__ == '__main__':

	parse = argparse.ArgumentParser()
	parse.add_argument('--train', dest='training', action='store', default=None)
	parse.add_argument('--test', dest='testing', action='store', default=None)
	a = parse.parse_args()

	if a.training:
		labelsAndSubjects = []
		f = open(a.training)
		for line in f:
			ll = line.strip().split('\t')
			labelsAndSubjects.append(ll)
		spamList, hamList, numHam, numSpam = train(labelsAndSubjects)
		spamFrequeny = checkFrequency(spamList)
		hamFrequency = checkFrequency(hamList)

		probOverallHam = float(numHam) / (numHam + numSpam)
		probOverallSpam = float(numSpam) / (numHam + numSpam)

		spamProb = changeToPercentage(spamFrequeny)
		hamProb = changeToPercentage(hamFrequency)

		f.close()
	
	if a.testing:
		# initializing everything, have some extra value in case wanted
		labeledSpam = 0.0
		trueSpam = 0.0
		labeledHam = 0.0
		trueHam = 0.0
		correctSpam = 0.0
		correctHam = 0.0
		incorrectSpam = 0.0
		incorrectHam = 0.0
		totalTests = 0.0
		recall = 0.0
		precision = 0.0

		f = open(a.testing)
		for line in f:
			totalTests += 1

			#using a different method of splitting as before, can't decide which I like more
			ll = line.strip().split()
			label = ll[0]
			words = ll[1:]

			# needs to be reset at the beginning of each round; I forgot to do this earlier, big headache
			hamLogs = 0.0
			spamLogs = 0.0

			#used to determine recall, etc., later
			if label == "0":
				trueHam += 1
			elif label == "1":
				trueSpam += 1
			for x in words:
				try:
					spamLogs += math.log(spamProb[x])
				except:
					spamLogs += math.log(spamProb['<UNK>'])
				try:
					hamLogs += math.log(hamProb[x])
				except:
					hamLogs += math.log(hamProb['<UNK>'])

			spamLogs += math.log(probOverallSpam)
			hamLogs += math.log(probOverallHam)	

			if hamLogs > spamLogs:
				labeledHam += 1
				if label == "0":
					correctHam += 1
				elif label == "1":
					incorrectHam += 1
			elif spamLogs > hamLogs:
				labeledSpam += 1
				if label == "0":
					incorrectSpam += 1
				if label == "1":
					correctSpam += 1

		recall = correctSpam/(correctSpam + incorrectHam)
		precision = correctSpam/labeledSpam

		recallOutput = "recall = " + str(recall*100) + "%"
		precisionOutput = "precision = " + str(precision*100) + "%"

		print recallOutput
		print precisionOutput

		f.close()

		f = open('testOutput.txt', 'w')
		f.write(recallOutput + "\n")
		f.write(precisionOutput)

		f.close()

		







