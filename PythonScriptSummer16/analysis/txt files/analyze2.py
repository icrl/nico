import os

class analyze():

	#method to calculate the number of words in a phrase	
	def wordCount(phrase):
		split = phrase.split()
		return len(split)
	
	#method to determine if two phrases are the same
	def sameOrNot(expected, interpreted):
		if expected == interpreted:
			return True
		else:
			return False
	
	#method to calculate the minimum edit distance between two strings of words
	def minEditDistance(expected, interpreted):
		#may want this to take in multiple lines, would split allow new lines as well?
		eArray = expected.split()
		iArray = interpreted.split()
		eLen = len(eArray)
		iLen = len(iArray)
		#print("exp length: "+str(eLen)+", int length: "+str(iLen))

		#create a 2d array to hold the edit distance with 
		distance = []
		for i in range(eLen+1):
			#print("create"+str(i))
			distance.append([])

		#print(distance)
		#for each row, set it from 0 to e length
		for i in range(0, eLen + 1):
			#print("rows"+str(i))
			#distance[i][0] = i
			distance[i].append(i)
		for j in range(1, iLen + 1):
			#print("cols"+str(j))
			#distance[0][j] = j
			distance[0].append(j)

		#print(distance)
		#go through and determine the distance between each word
		for i in range(1, eLen + 1):
			for j in range(1, iLen + 1):
				#if the two words are equal
				if eArray[i-1] == iArray[j-1]:
					#the distance is the same as the previous words
					#distance[i][j] = distance[i-1][j-1]
					distance[i].append(distance[i-1][j-1])
					#distance[i][j] = distance[i-1][j-1]
				else:
					#find the cost of substituting, inserting, and deleting
					#sub = distance[i-1][j-1] + 2
					sub = distance[i-1][j-1] + 1
					insert = distance[i-1][j] + 1
					delete = distance[i][j-1] + 1
					#the distance is whichever is  smallest
					#distance[i][j] = min(sub, insert, delete)
					distance[i].append(min(sub, insert,delete))
		#return the last value
		#print(distance)
		return distance[eLen][iLen];

	if __name__=="__main__":
		from sys import argv
		
		global eFileName, iFileName
		#for the files in this folder
		for file in os.listdir("/home/ranjini/Desktop/nico/PythonScriptSummer16/analysis/txt files"):
			#if this is a reference text
			if file.endswith("ref.txt"):
				eFileName = file
				iFileName = file[:-7]+"hyp.txt"

				with open(eFileName) as f:
					eLines = f.readlines()
					#print(len(eLines))
				#import interpreted
				with open(iFileName) as f:
					iLines = f.readlines()
					#print(len(iLines))
				#create a file to write to
				writeFileName = file[:-7] + "analysis.txt"
				f = open(writeFileName, 'w')
				totalWC = 0
				totalDist = 0
				#for each line in the files
				for j in range(0, len(eLines)):		
					#calc word counts
					ewc = wordCount(eLines[j])
					iwc = wordCount(iLines[j])
					#determine if same
					same = sameOrNot(eLines[j], iLines[j])
					#calc distance
					lDist = minEditDistance(eLines[j],iLines[j])
					#add to total
					totalWC += ewc
					totalDist += lDist
					#write the word count (e, i), same/not, and levenshtein distance			
					f.write("Line "+str(j+1)+": wc: "+str(ewc)+", "+str(iwc)+". same: "+str(same)+". distance: "+str(lDist)+"\n")
				#print("wc: "+str(totalWC)+" dist: "+str(totalDist))
				wer = totalDist / (totalWC * 1.0)
				f.write("Word error rate: "+str(wer))
				f.close()
				print("Analyzed files " + eFileName + ", " + iFileName)
