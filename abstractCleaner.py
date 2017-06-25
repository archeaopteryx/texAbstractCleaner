##########################################################
#
# Abstract Cleaner
# June 2017 K. Herman (herman@physik.hu-berlin.de)
# REQUIRES python3. It's been >10 years, people!
#
#########################################################

import os
import csv
import re

def checker(tempList, toRemove):
	for entry in tempList:
		if any(toRemove in val for val in entry):
			tempList.remove(entry)
			break
	return tempList

def authorScraper(tempList):
	author = 'Error'
	for entry in tempList:
		if any('\\author{' in val for val in entry):
			author = re.sub(r'\\author{', "", entry[0])
			author = re.sub(r'}%', "", author)
			author = re.sub('\t', "", author)
			break
	return author

def cleaner(fileName):

	remove0 = "documentclass{abstractYRW.cls}"
	remove1 = "begin{document}"
	remove2 = "end{document}"
	temp = []

	with open(fileName, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			temp.append(row)

	temp2 = checker(temp, remove2)
	temp1 = checker(temp2, remove1)
	temp = checker(temp1, remove0)

	author = authorScraper(temp)
	abstractAuthor = [author, 'clean_'+fileName]

	with open("clean_"+fileName, 'w', newline = "") as f:
		writer = csv.writer(f)
		for row in temp:
			writer.writerow(row)

	temp = []
	return abstractAuthor

def main():
	absAuthorList = []
	absFiles = [f for f in os.listdir() if f.endswith("tex")]
	absFiles = sorted(absFiles)

	if any('clean_' in abstract for abstract in absFiles):
		runBool = False
		run = input("It looks like you've already run the script. Are you sure you want to continue? y/N (default is No):   ")
		if run.lower().startswith("y"):
			runBool = True
		if runBool == False:
			exit()

	for abstract in absFiles:
		nextAuthor = cleaner(abstract)
		absAuthorList.append(nextAuthor)

	overWriteBool = input("Do you want to delete the original tex files? The new files will be named 'clean' + originalFilename. y/N:    ")
	if overWriteBool.lower().startswith('y'):
		for f in absFiles:
			os.remove(f)

	with open("ListOfAbstracts.txt", 'w', newline = "") as f:
		writer = csv.writer(f)
		for row in absAuthorList:
			writer.writerow(row)

	print('finished!')

if __name__ == "__main__":
	main()



