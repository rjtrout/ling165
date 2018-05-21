__author__ = """Robert Trout (robert.trout@sjsu.edu)"""

import numpy, sys,

str1 = '#' + sys.argv[1]
str2 = '#' + sys.argv[2]

ls1 = len(str1)
ls2 = len(str2)

a = numpy.zeros(shape=(ls1,ls2))

for i in range(1,ls1):
	a[i][0] = i

for i in range(1,ls2):
	a[0][i] = i	

for i in range(1,ls1):
	for j in range(1,ls2):
		if str1[i] == str2[j]:
			cost = 0
		else:
			cost = 1
		a[i,j] = min(a[i-1][j] + 1, a[i][j-1] +1, a[i-1][j-1] + cost)


'''

for i in range(ls2):
	a[ls1-1][i] = i

for i in range(ls1):
	count = abs((ls1-1)-i)
	a[i][0] = count


for j in range(1,ls1):
	for i in range(1,ls2):
		maxNum = 0
		axis0 = abs((ls1-1)-j)
		editDown = a[axis0+1][i]
		if str1[j:j+1] != str2[i:i+1]:
			editDown += 1
		editleft = a[axis0][i-1]
		if str1[j:j+1] != str2[j:i+1]:
				editleft += 1
		editDiag = a[axis0+1][i-1]
		if str1[j:j+1] != str2[i:i+1]:
				editDiag += 1
		maxNum = min(editDown, editleft)
		maxNum = min(maxNum, editDiag)
		a[axis0][i] = maxNum
'''
print a

