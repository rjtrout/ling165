___author___ = """Robert Trout(robert.trout@sjsu.edu)"""

import sys, itertools
from random import shuffle

def readSource(f, nGramNum, tokens):
	"""Splits source material up and appends to main list
	"""
	for line in f:
		ll = []
		gram = []
		for i in range(nGramNum):
			ll.append('<s>')
		ll.extend(line.split())
		for i in range(nGramNum):
			ll.append('</s>')
		linelen = len(ll)
		for i in range(1,(linelen - nGramNum)):
			singleTok = []
			for j in range(nGramNum):
				singleTok.append(ll[(i + j)])
			gram.append(singleTok)
		tokens.extend(gram)
	tokens.sort()

def generateSentences(nGram, nGramNum):
	"""Takes list of ngrams and size of ngrams to generate a single setence.
	"""
	sentence = []
	for i in range(nGramNum):
		sentence.append('<s>')
	shuffle(nGram)
	while True:
		for i in range(len(nGram)):
			if nGram[i][0] == sentence[-1]:
				sentence.extend(nGram[i][-(nGramNum-1):])
				if nGram[i][-1] == "</s>":
					return sentence

def elimBoundry(sentence, nGramNum):
	"""Eliminates boundry markers so they don't appear in output
	"""
	i = 0
	while i < (len(sentence)):
		if sentence[i] == "<s>" or sentence[i] == "</s>":
			del sentence[i]
			i = i - 1
		i += 1
	return sentence

def printSentences(numSentences):
	"""Prints sentences to console and text file
	"""

	f = open('sentenceOutput.txt', 'w')
	for i in range(numSentences):
		strSentence = ''
		sentence = generateSentences(tokens, nGramNum)
		sentence = elimBoundry(sentence, nGramNum)
		strSentence = ' '.join(sentence)
		f.write(strSentence + "\n")
		print strSentence + "\n"
	f.close()

		
if __name__ == '__main__':

	tokens = []

	# setting up arguments
	fileToOpen = str(sys.argv[1])
	nGramNum = int(sys.argv[2])
	numSentences = int(sys.argv[3])

	f = open(fileToOpen)
	readSource(f, nGramNum, tokens)
	f.close()
	tokens = list(tokens for tokens,_ in itertools.groupby(tokens))
	printSentences(numSentences)


