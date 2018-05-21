import math
import lab4
import sys
import matplotlib
matplotlib.use('Agg')

def load_init():
	out = {}
	f = open('initial_probs.txt')
	for line in f:
		s, e, p = line.strip().split('\t')
		p = float(p)
		if not s in out: out[s] = {}
		out[s][e] = p
	f.close()
	return out

def load_data():
	out = []
	f = open('phrase_pairs.txt')
	for line in f:
		s, e = line.strip().split('\t')
		swl = s.split(); ewl = e.split()
		out.append((swl, ewl))
	f.close()
	return out

def E_example(pd, swl, ewl):
	al = lab4.exhaust_align(swl, ewl)
	p_al = []
	for alignment in al:
		prob = 1.0
		for si, ei in alignment:
			spanishW = swl[si]
			englishWord = ewl[ei]
			prob *= pd[spanishW][englishWord]
		p_al.append(prob)
	total = sum(p_al)
	for i in range(len(p_al)):
		p_al[i] /= total
	return al, p_al, total

def M_example(cd, swl, ewl, al, p_al):
	for a, pa in zip(al, p_al):
		for si, ei in a:
			sw = swl[si]
			ew = ewl[ei]
			if not sw in cd: cd[sw] = {} 
			if not ew in cd[sw]: cd[sw][ew] = 0.0
			cd[sw][ew] += pa
	return cd

def M_Final(cd):
	for sword in cd:
		total = sum(cd[sword].values())
		for enword in cd[sword]:
			cd[sword][enword] /= total
	return cd

if __name__ == '__main__':
	pd = load_init()
	D = load_data()
	stop = False
	prev_L = -1e+100; n_iter = 0
	resto_dict = {ew:[pd['resto'][ew]] for ew in pd['resto']}
	while not stop:
		L = 0.0; cd = {}
		for swl, ewl in D:
			al, p_al, total = E_example(pd, swl, ewl)
			L += math.log(total)
			cd = M_example(cd, swl, ewl, al, p_al)
		pd = M_Final(cd)
		n_iter += 1
		L_diff = L - prev_L
		prev_L = L
		for ew in pd['resto']: resto_dict[ew].append(pd['resto'][ew])
		stop = (n_iter >= 100) or (L_diff < 0.01)
		msg = '# Iteration '+str(n_iter)
		msg += ': L='+str(L)
		msg += ', improved by '+str(L_diff)
		msg += ' '*5+'\r'
		sys.stderr.write(msg)
	sys.stderr.write('\n')
	lab4.plot_resto(resto_dict)




