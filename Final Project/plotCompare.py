import numpy as np
import nltk, re, os, pickle, scipy, warnings, sys
from sklearn import feature_extraction
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.externals import joblib
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation


def importPlots(f):
	plots = []
	titles = []
	years = []
	lstFiles = os.listdir(f)
	lstFiles.sort()
	for fileName in lstFiles:
		g = []
		indFile = open(f + fileName)
		h = indFile.readlines()
		if h[0].strip() != "":
			plots.append(h[0].strip())
			titles.append(h[1].strip())
			years.append(h[2].strip())
	return plots, titles, years

def tokenize_stem_and_lemmize(text):

	tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
	stemmer = nltk.stem.snowball.SnowballStemmer("english")
	lemmatizer = nltk.stem.WordNetLemmatizer()
	
	#this is to filter punctuation out, we should test both methods
	filtered_tokens = []
	for token in tokens:
		if re.search('[a-zA-Z]', token):
			filtered_tokens.append(token)
	stems = [stemmer.stem(t) for t in filtered_tokens]

	#stems = [stemmer.stem(t) for t in tokens]
	#lemmas = [lemmatizer.lemmatize(t) for s in stems]
	return stems


def pickling(tfidf_matrix, mainPlots, mainTitles, mainYears, params, tfidf_vectorizer):
	file = open('./pickles/pickleTfidf', 'wb')
	pickle.dump(tfidf_matrix,file)
	file.close()

	file = open('./pickles/picklePlots', 'wb')
	pickle.dump(mainPlots,file)
	file.close()

	file = open('./pickles/pickleTitles', 'wb')
	pickle.dump(mainTitles,file)
	file.close()

	file = open('./pickles/pickleYears', 'wb')
	pickle.dump(mainYears,file)
	file.close()

	file = open('./pickles/pickleParams', 'wb')
	pickle.dump(params,file)

	joblib.dump(tfidf_vectorizer, './pickles/vectorizer.pkl')
	file.close()

def unpickling():
	tfidf_matrix = pickle.load(open('./pickles/pickleTfidf', 'rb'))
	mainPlots = pickle.load(open('./pickles/picklePlots', 'rb'))
	mainTitles = pickle.load(open('./pickles/pickleTitles', 'rb'))
	mainYears = pickle.load(open('./pickles/pickleYears', 'rb'))
	params = pickle.load(open('./pickles/pickleParams', 'rb'))
	tfidf_vectorizer =joblib.load('./pickles/vectorizer.pkl')
	return tfidf_matrix, mainPlots, mainTitles, mainYears, params, tfidf_vectorizer

def importTest(f, tfidf_vectorizer):
	lstFiles = os.listdir(f)
	lstFiles.sort()
	testPlotsTFIDF = []
	testPlot, testTitle, testYear = importPlots(f)
	for i in range(len(testPlot)):
		testPlot[i] = testPlot[i].decode('utf8')
		testTitle[i] = testTitle[i].decode('utf8')

	for i in range(len(testPlot)):
		testPlist = []
		testPlist.append(testPlot[i])
		tfidf_query = tfidf_vectorizer.transform(testPlist)
		testPlotsTFIDF.append(tfidf_query)
	return testPlotsTFIDF, testTitle, testYear

def svdTransform(tfidf_matrix, testPlotsTFIDF):

	testPlotsSVD =[]
	
	if not os.path.isfile("./pickles/pickleSVDMatrix"):
		svd = TruncatedSVD(n_components=1000, n_iter=7, random_state=42)
		svdMatrix = svd.fit_transform(tfidf_matrix)

		file = open('./pickles/pickleSVDMatrix', 'wb')
		pickle.dump(svdMatrix,file)
		file.close
		params = svd.get_params()
		file = open('./pickles/pickleParamsSVD', 'wb')
		pickle.dump(params,file)
		file.close()
		joblib.dump(svd, './pickles/vectorizerSVD.pkl')
		
	else:
		params = pickle.load(open('./pickles/pickleParamsSVD', 'rb'))
		svdMatrix = pickle.load(open('./pickles/pickleSVDMatrix', 'rb'))
		svd =joblib.load('./pickles/vectorizerSVD.pkl')
		svd.set_params(**params)

	for i in range(len(testPlotsTFIDF)):
		testPlist = []
		testPlistOne = (testPlotsTFIDF[i])
		svd_query = svd.transform(testPlistOne)
		testPlotsSVD.append(svd_query)
	return svdMatrix, testPlotsSVD

def ldaTransform(tfidf_matrix, testPlotsTFIDF):

	testPlotsLDA =[]
	
	if not os.path.isfile("./pickles/pickleLDAMatrix"):
		lda = LatentDirichletAllocation(n_components=300, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
		ldaMatrix = lda.fit_transform(tfidf_matrix)
		file = open('./pickles/pickleLDAMatrix', 'wb')
		pickle.dump(ldaMatrix,file)
		file.close

		params = lda.get_params()
		file = open('./pickles/pickleParamsLDA', 'wb')
		pickle.dump(params,file)
		file.close()

		joblib.dump(lda, './pickles/vectorizerLDA.pkl')
		
	else:
		params = pickle.load(open('./pickles/pickleParamsLDA', 'rb'))
		ldaMatrix = pickle.load(open('./pickles/pickleLDAMatrix', 'rb'))
		lda =joblib.load('./pickles/vectorizerLDA.pkl')
		lda.set_params(**params)

	for i in range(len(testPlotsTFIDF)):
		testPlist = []
		testPlistOne = (testPlotsTFIDF[i])
		lda_query = lda.transform(testPlistOne)
		testPlotsLDA.append(lda_query)
	return ldaMatrix, testPlotsLDA	

def testCosine(testPlotsTFIDF, tfidf_matrix, mainTitles, testTitle):
	for j in range(len(testPlotsTFIDF)):
		listDist = []
		for i in range(tfidf_matrix.shape[0]):
			dist = 1 - cosine_similarity(tfidf_matrix[i],testPlotsTFIDF[j])
			name = mainTitles[i]
			tupNameDist = (dist, name)
			listDist.append(tupNameDist)
		listDist.sort()
		file = open("testRecommend.txt", "a")
		print "Top ten movies like plot: %s" %(testTitle[j])
		file.write("Top ten movies like plot: %s\n" %(testTitle[j]))
		for i in range(5):
			print "Movie " + str(i) + ": " + str(listDist[i][1]) + "." 
			file.write("Movie " + str(i) + ": " + str(listDist[i][1]) + ".\n")
		print
		file.write("\n")
		file.close()

def cosine_similarity2(testPlotsTFIDF, tfidf_matrix, mainTitles, testTitle):
	for j in range(len(testPlotsTFIDF)):
		listDist = []
		for i in range(tfidf_matrix.shape[0]):
			numerator = np.dot(tfidf_matrix[i], testPlotsTFIDF[j].T)
			denominator = np.linalg.norm(tfidf_matrix[i])*np.linalg.norm(testPlotsTFIDF[j])
			dist = 1 - numerator / denominator
			name = mainTitles[i]
			tupNameDist = (dist, name)
			listDist.append(tupNameDist)
		listDist.sort()
		file = open("testRecommend.txt", "a")
		print "Top ten movies like plot: %s" %(testTitle[j])
		file.write("Top ten movies like plot: %s\n" %(testTitle[j]))
		for i in range(5):
			print "Movie " + str(i) + ": " + str(listDist[i][1]) + "."
			file.write("Movie " + str(i) + ": " + str(listDist[i][1]) + ".\n")
		print
		file.write("\n")
		file.close()


def main():
	warnings.filterwarnings("ignore") # got sick of warnings
	plotsLocation = sys.argv[1] # plots to detemine matrix
	plotToCompare = sys.argv[2] # plot you would like to compare
	stopWords = set(nltk.corpus.stopwords.words('english'))

	tfidf_vectorizer = feature_extraction.text.TfidfVectorizer(stop_words=stopWords, use_idf=True, 
														  tokenizer=tokenize_stem_and_lemmize)

	if not os.path.isfile("./pickles/pickleTfidf"):
		mainPlots, mainTitles, mainYears = importPlots(plotsLocation)
		for i in range(len(mainPlots)):
			mainPlots[i] = mainPlots[i].decode('utf8')
			mainTitles[i] = mainTitles[i].decode('utf8')
		
		tfidf_matrix = tfidf_vectorizer.fit_transform(mainPlots)
		params = tfidf_vectorizer.get_params()
		pickling(tfidf_matrix, mainPlots, mainTitles, mainYears, params, tfidf_vectorizer)
		
	else:
		tfidf_matrix, mainPlots, mainTitles, mainYears, params, tfidf_vectorizer = unpickling()
		tfidf_vectorizer.set_params(**params)


	# creating matricies
	testPlotsTFIDF, testTitle, testYear = importTest(plotToCompare, tfidf_vectorizer)
	svdMatrix, svdMatrix_query = svdTransform(tfidf_matrix, testPlotsTFIDF)
	ldaMatrix, testPlotsLDA = ldaTransform(tfidf_matrix, testPlotsTFIDF)

	#Testing
	# testing with Vanilla TFIDF
	print "TFIDF"
	testCosine(testPlotsTFIDF, tfidf_matrix, mainTitles, testTitle)
	# testing with SVD
	print "SVD"
	cosine_similarity2(svdMatrix_query, svdMatrix, mainTitles, testTitle)
	# testing with LDA
	print "LDA"
	cosine_similarity2(testPlotsLDA, ldaMatrix, mainTitles, testTitle)

if __name__ == "__main__":
	main()

