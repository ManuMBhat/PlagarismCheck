import numpy as np
import pandas as pd
from stemmer import PorterStemmer
import argparse
import os
import csv

outputFile = "Plagarised"

class DocumentPair:

    def __init__(self, fileA, fileB):
        self.__allWords = set()
        self.__wordsA = dict()
        self.__wordsB = dict()

        with open(fileA, 'r') as document:
            for line in document:
                words = line.strip().split()
                for word in words:
                    p = PorterStemmer()
                    word = p.stem(word, 0, len(word)-1)
                    if word in self.__wordsA.keys():
                        self.__wordsA[word] += 1
                    else :
                        self.__wordsA[word] = 1

        with open(fileB, 'r') as document:
            for line in document:
                words = line.strip().split()
                for word in words:
                    p = PorterStemmer()
                    word = p.stem(word, 0, len(word)-1)
                    if word in self.__wordsB.keys():
                        self.__wordsB[word] += 1
                    else :
                        self.__wordsB[word] = 1

        self.__allWords = set(self.__wordsA.keys()) | set(self.__wordsB.keys())
        self.__table = {t[1] : t[0] for t in enumerate(self.__allWords)}

    def getAllWords(self):
        return self.__allWords

    def dotProduct(self):
        wordMat = np.zeros((2, len(self.__allWords)))

        for key in self.__wordsA:
            wordMat[0, self.__table[key]] = self.__wordsA[key]
        for key in self.__wordsB:
            wordMat[1, self.__table[key]] = self.__wordsB[key]

        dot = wordMat[0].dot(wordMat[1])
        normA = np.linalg.norm(wordMat[0])
        normB = np.linalg.norm(wordMat[1])

        return dot / (normA * normB)


def parse():
    parser = argparse.ArgumentParser()
    #flag for directory
    parser.add_argument("--dir", default=False)
    parser.add_argument("--doc1", default=None)
    parser.add_argument("--doc2", default=None)
    parser.add_argument("--out", default=outputFile)
    parser.add_argument("--csv", action='store_true')
    parser.add_argument("--xlsx", action='store_true')
    parser.add_argument("--html", action='store_true')
    parser.add_argument("--threshold", default=0.0, type=float)
    
    return parser.parse_args()


def traverseDir(dirname, flags, threshold):
    docNames = [os.path.join(dirname, f) for f in os.listdir(dirname) if f[-4:] == ".txt"]
    
    finalMatrix = np.empty((len(docNames), len(docNames)))
    finalMatrix[:] = np.nan
    
    finalOutput = list()
    
    for i in range(len(docNames)):
        j = i + 1
        while j < len(docNames):
            pair = DocumentPair(docNames[i], docNames[j])
            result = pair.dotProduct()
            finalOutput.append([docNames[i], docNames[j], result])
            finalMatrix[j, i] = result
            j += 1
    
    print(finalOutput)

    if flags[0]:
        toCSV(docNames, finalMatrix)
    if flags[1]:
        toXLSX(docNames, finalMatrix, threshold)
    if flags[2]:
        toHTML(docNames, finalMatrix, threshold)

    return finalOutput

def toXLSX(docs, finalMatrix, threshold):
    '''Highlights plagarised document pairs and exports as .xlsx'''

    docs = [filename.split('/')[-1] for filename in docs]
    plagarismDf = pd.DataFrame(data=finalMatrix, index=docs, columns=docs)
    
    highlight_plagarised = lambda val : 'background-color: red' if val > threshold else ''
    styledPlagarismDf = plagarismDf.style.applymap(highlight_plagarised)
    styledPlagarismDf.to_excel(outputFile + '.xlsx', engine='openpyxl')


def toHTML(docs, finalMatrix, threshold):
    '''Highlights plagarised document pairs in percentage and exports as .html'''
    
    docs = [filename.split('/')[-1] for filename in docs]
    plagarismDf = pd.DataFrame(data=finalMatrix, index=docs, columns=docs)

    highlight_plagarised = lambda val : 'background-color: red' if val > threshold else ''
    styledPlagarismDf = plagarismDf.style.applymap(highlight_plagarised).format("{:.1%}", na_rep="-")

    with open(outputFile + ".html", "w") as htmlfile:
        htmlfile.write(styledPlagarismDf.render())


def toCSV(docs, finalMatrix):
    docs = [filename.split('/')[-1] for filename in docs]
    with open(outputFile + '.csv', 'w', newline='') as csvfile:
        outputwriter = csv.writer(csvfile, delimiter=',')
        outputwriter.writerow(['File'] + docs)
        for i in range(len(docs)):
            outputwriter.writerow([docs[i]] + list(finalMatrix[i, :]))
