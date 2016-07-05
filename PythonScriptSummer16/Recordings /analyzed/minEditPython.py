class MinEdit():
	#method to calculate the minimum edit distance between two strings of words
	def minEditDistance(expected, interpreted):
		#may want this to take in multiple lines, would split allow new lines as well?
		eArray = expected.split()
		iArray = interpreted.split()
		eLen = len(eArray)
		iLen = len(iArray)

		#create a 2d array to hold the edit distance with 
		distance = []
		for i in range(eLen+2):
			distance.append([])

		#for each row, set it from 0 to e length
		for i in range(0, eLen + 1):
			distance[i][0] = i
		for j in range(0, iLen + 1):
			distance[0][j] = j

		#go through and determine the distance between each word
		for i in range(1, eLen + 1):
			for j in range(1, iLen + 1):
				#if the two words are equal
				if eArray[i-1] is iArray[j-1]:
					#the distance is the same as the previous words
					distance[i][j] = distance[i-1][j-1]
				else:
					#find the cost of substituting, inserting, and deleting
					sub = distance[i-1][j-1] + 2
					insert = distance[i-1][j] + 1
					delete = distance[i][j-1] + 1
					#the distance is whichever is  smallest
					distance[i][j] = min(sub, insert, delete);
		#return the last value
		return distance[eLen][iLen];
