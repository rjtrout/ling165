"""Functions for LING165 Lab4"""

__author__ = "Hahn Koo (hahn.koo@sjsu.edu)"

def exhaust_align(s, e):
	"""List all possible ways to align words from s to e.

	Args:
	- s: a list of words
	- e: a list of words
	Returns:
	- a list of index pairs
	-- index pair (i, j) means s[i] --> e[j]  
	"""
	ns = len(s); ne = len(e)
	out = [[]]
	for j in range(ne):
		temp = []
		for x in out:
			for k in range(ns):
				temp.append(x+[(k, j)])
		out = temp + []
	return out

def plot_resto(resto_dict):
	"""Plot how P(*|resto) changes over time.
	(Requires matplotlib)

	Args:
	- resto_dict: a dictionary
	-- resto_dict[ew] = a list of P(ew|resto)'s from iterations
	Returns:
	- None (just plots a graph)
	"""
	from matplotlib import pyplot as plt
	fig = plt.figure()
	ax = plt.axes()
	keys = resto_dict.keys()
	x = range(len(resto_dict[keys[0]]))
	for ew in keys:
		resto_ew = ax.plot(x, resto_dict[ew], label=ew)
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels, loc=5)
	plt.title('Change in P(*|resto) over time')
	plt.xlabel('iterations')
	plt.savefig('resto.png')
	plt.show()
