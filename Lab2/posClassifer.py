__author__ = """Robert Trout (robert.trout@sjsu.edu)"""

import pickle, re, math, sys, argparse


def build_trellis(listofWords, A, B):
	trellis = [{'<s>':[0.0, None]}]
	for w in listofWords[1:]:
		reachables = []
		prev_states = trellis[-1].keys()
		for ps in prev_states:
			reachables += A[ps].keys()
		reachables = set(reachables) # to elimate dups

		column = {}
		for state in reachables:
			if w in B[state]:
				column[state] = [-1e+100, None]

		for state in column:
			for ps in prev_states:
				try:
					score = trellis[-1][ps][0]
					score += math.log(A[ps][state])
					score += math.log(B[state][w])
					if score > column[state][0]:
						column[state][0] = score
						column[state][1] = ps
				except KeyError:
					pass
		trellis.append(column)
	return trellis

def find_path(trellis):
	bestPath = []
	finalPath = []
	bestPath.extend(trellis[-1].keys())
	nextBreadCrumb = trellis[-1]["</s>"][1]
	for i in range(len(trellis)-2,-1,-1):
		bestPath.append(nextBreadCrumb)
		nextBreadCrumb = trellis[i][nextBreadCrumb][1]
	for i in reversed(bestPath):
		finalPath.append(i)
	return finalPath
		
if __name__ == '__main__':

	parse = argparse.ArgumentParser()
	parse.add_argument('--test', dest='testing', action='store', default=None)
	parse.add_argument('--answer', dest='answer', action='store', default=None)
	args = parse.parse_args()

	A = pickle.load(open('A.pickle'))
	B = pickle.load(open('B.pickle'))

	if args.testing:

		f = open(args.testing)
		g = open(args.answer)

		split_lines = []
		split_lines_answers = []
		bestPath_list = []
		answerPath_list = []
		for line in f:
			split_individual_line = []
			split_individual_line.append("<s>")
			split_individual_line.extend(line.split())
			split_individual_line.append("</s>")
			split_lines.append(split_individual_line)

		for i in range(len(split_lines)): # change for len(split_lines)
			trellis = build_trellis(split_lines[i],A,B)
			bestPath = find_path(trellis)
			bestPath_list.append(bestPath)

		for line in g:
			split_individual_line_answer= []
			split_individual_line_answer_list = []
			tags_per_line = []
			split_individual_line_answer.extend(["<s>_#_<s>"])
			split_individual_line_answer.extend(line.split())
			split_individual_line_answer.extend(["</s>_#_</s>"])
			for i in split_individual_line_answer:
				word_and_tag = i.split("_#_")
				split_individual_line_answer_list.append(word_and_tag[1])
			answerPath_list.append(split_individual_line_answer_list)

		totalTags = 0.0
		total_right = 0.0
		total_wrong = 0.0
		percent_right = 0.0

		for i in range(len(bestPath_list)):
			for j in range(len(bestPath_list[i])):
				if bestPath_list[i][j] == "<s>" or bestPath_list[i][j] == "</s>":
					continue
				totalTags += 1
				if bestPath_list[i][j] == answerPath_list[i][j]:
					total_right += 1
				elif bestPath_list[i][j] != answerPath_list[i][j]:
					total_wrong += 1
		percent_right = total_right/totalTags
		accuracyOutput = "Tagging accuracy: " + str(percent_right*100) + "%"

		print accuracyOutput

		f.close()
		g.close()

		f = open('testOutput.txt', 'w')
		f.write(accuracyOutput)

		f.close()
