##########################################################
#
# Abstract Cleaner
# June 2017 K. Herman (herman@physik.hu-berlin.de)
# REQUIRES python3. It's been >10 years, people!
#
#########################################################

import os
import sys
import csv
import re

def checker(tempList, toRemove):
	remove = re.compile(toRemove)
	newList = [val for val in tempList if remove.match(val) == None ]
	return newList

def authorScraper(tempList):
	author = 'Error'
	auth = re.compile('\\\\author\{')

	for entry in tempList:
		if auth.match(entry):
			author = entry.split()[0]+ ' ' + entry.split()[1]
			author = re.sub('\\\\author{', "", author)
			author = re.sub(r'}%', "", author)
			break
	return author

def cleaner(fileName):

	content = open(fileName).readlines()

	temp1 = checker(content, "\\\\documentclass\{abstractYRW\}")
	temp0 = checker(temp1, "\\\\end\{document\}")
	temp = checker(temp0, "\\\\begin\{document\}")

	author = authorScraper(temp)
	abstractAuthor = [author+' ', '\\input{clean_'+fileName+'}']

	newFile = open("clean_"+fileName, 'w', newline = '\r\n')
	for row in temp:
		newFile.write(row)
	newFile.close()


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
			print('quitting')
			sys.exit()

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
