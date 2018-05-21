__author__ = """Robert Trout (robert.trout@sjsu.edu)"""

import numpy, re, math, sys, argparse, os, operator

def count(fn, v):
	out = numpy.zeros(len(v))
	g = open(fn)
	for line in g:
		for w in line.strip().split():
			if w in v: out[v.index(w)] += 1
	g.close()
	return out

def openFileNames(pathToFile):
	m = []
	lst = os.listdir(pathToFile)
	lst.sort()
	for filename in lst:
		file = str(pathToFile + filename)
		m.append( count(file, v))
	numFiles = len(os.listdir(pathToFile))
	m = numpy.array(m)
	return m, numFiles, lst

def tfidf(m, n_doc):
	for j in range(m.shape[1]): 
		df = len(m[:, j].nonzero()[0]) 
		if df > 0: m[:, j] *= numpy.log10(n_doc/float(df))
	return m

def cosine_similarity(v1, v2):
	numerator = numpy.dot(v1, v2)
	denominator = numpy.linalg.norm(v1)*numpy.linalg.norm(v2)
	return numerator / denominator

def getVocab(inputStream):
	f = open(inputStream)
	vocab = []
	for line in f:
		word = line.strip().split()
		vocab.extend(word)
	vocab.sort()
	f.close()
	return vocab

def getPathToFolder(string):
	uneditPathList = string.split('/')
	s = '/'.join(uneditPathList[:-1]) + '/'
	t = uneditPathList[-1]
	return s, t


def computeWrdComp(T_k, qrywRow, v, iQryWrd):
	lstCompare = []

	for i in range(len(v)):
		T_i = T_k[i, :]
		if (i == iQryWrd):
			continue
		else:
			cmpre = cosine_similarity(qrywRow.A1, T_i.A1)
			tpleCmpre = (v[i], cmpre)
			lstCompare.append(tpleCmpre)

	lstCompare.sort(key=operator.itemgetter(1), reverse=True)
	return lstCompare[:10]

def computeQryComp(D_k, q_k, lFiles):
	lstCompare = []
	for i in range(len(lFiles)):
		d = D_k[:, i]

		cmpre = cosine_similarity(q_k.A1, d.A1)
		lstCompare.append((cmpre,lFiles[i]))
	lstCompare.sort(reverse=True)

	return lstCompare[:10]

def svdWork(U, s, VT, k):
	S_k = numpy.matrix(numpy.diag(s[:k]))

	U_k = U[:, :k]
	VT_k = VT[:k, :]

	T_k = U_k * S_k 
	D_k = S_k * VT_k

	return S_k, U_k, VT_k, T_k, D_k

def svd(m, k, queryWord, v, lFiles, qry):
	iQryWrd = v.index(args.queryWord)
	traM = numpy.transpose(m)

	U, s, VT = numpy.linalg.svd(traM, full_matrices=False)

	S_k, U_k, VT_k, T_k, D_k = svdWork(U, s, VT, k)
	

	qrywRow = T_k[iQryWrd, :]

	ttwc = computeWrdComp(T_k, qrywRow, v, iQryWrd)
	ttwclist = createVector(v, traM, k, S_k, U_k, D_k, lFiles, qry)

	return ttwc, ttwclist

def createVector(v, traM, k, S_k, U_k, D_k, lFiles, qry):
	qryLst = qry.strip().split()
	qryListInd = []

	m = numpy.transpose(traM)
	n_doc = m.shape[0]
	q = numpy.zeros(len(v))

	for i in qryLst:
		qryListInd.append(v.index(i))

	dfList = []
	for i in qryListInd:
		dfList.append(len(m[:, i].nonzero()[0]))

	for i in range(len(qryListInd)):
		q[qryListInd[i]] = numpy.log10(n_doc/float(dfList[i]))

	q = numpy.matrix([q]).transpose()
	
	q_k = S_k.I * U_k.T * q

	return computeQryComp(D_k, q_k, lFiles)

def createVectorOfVocab(m, numTop, indexOfFile):
	vtcSmple = m[indexOfFile,:]
	dictSmpleV = dict(zip(v, vtcSmple))
	topWords = sorted(dictSmpleV.items(), key=operator.itemgetter(1), reverse=True)
	return topWords[:numTop]

def convertForExport(numTop, fileName, queryWord, twr, ttwc, ttwclist, qry):
	twrl = []
	ttwcl = []
	ttqList = []

	for i in range(len(twr)):
		twrl.append(twr[i][0])

	for i in range(len(ttwc)):
		ttwcl.append(ttwc[i][0])

	for i in range(len(ttwclist)):
		ttqList.append(ttwclist[i][1])

	senTW = "Top {} words in {}: {}".format(numTop, fileName, twrl)
	senTC = "Top ten words like {}: {} ".format(queryWord, ttwcl)
	senTQ = 'Top ten documents like qry "{}": {}'.format(qry, ttqList)

	return senTW, senTC, senTQ


def printToScreen(senTW, senTC, senTQ):
	print senTW
	print senTC
	print senTQ


def exportToFile(senTW, senTC, senTQ):
	f = open('testOutput.txt', 'w')
	f.write(senTW + "\n")
	f.write(senTC + "\n")
	f.write(senTQ + "\n")
	f.close()

class CustomAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, " ".join(values))


if __name__ == '__main__':

	parse = argparse.ArgumentParser()
	parse.add_argument('--sample', dest='sampleFile', action='store', default=None)
	parse.add_argument('--top', dest='topWords', action='store', default=None)
	parse.add_argument('--k', dest='kValue', action='store', default=None)
	parse.add_argument('--queryWord', dest='queryWord', action='store', default=None)
	parse.add_argument('--vocab', dest='vocabLocation', action='store', default=None)
	parse.add_argument('-query', '--query', action=CustomAction, type=str, nargs='+', help='list = [title, HTML]')

	args = parse.parse_args()
	qry=  args.query

	pathToFile, fileName =  getPathToFolder(args.sampleFile)
	numTop = int(args.topWords)
	numK = int(args.kValue)

	v = getVocab(args.vocabLocation)
	m, numFiles, lFiles = openFileNames(pathToFile)
	indexOfFile = lFiles.index(fileName)

	m = tfidf(m, numFiles)
	
	twr = createVectorOfVocab(m, numTop, indexOfFile)
	
	ttwc, ttwclist = svd(m, numK, args.queryWord, v, lFiles, qry)

	senTW, senTC, senTQ = convertForExport(numTop, fileName, args.queryWord, twr, ttwc, ttwclist, qry)

	printToScreen(senTW, senTC, senTQ)
	exportToFile(senTW, senTC, senTQ)
	




		




	

