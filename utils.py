import numpy as np
import pandas as pd
import argparse
import os
import csv

outputFile = "PlagarismText"

def docToDict(filename):
    words = {}
    with open(filename) as infile:
        for line in infile:
            line = line.strip()
            word_list = line.split()
            for word in word_list:
                if word in words.keys():
                    words[word] += 1
                else:
                    words[word] = 1
    return words


def dotProduct(words1, words2):
    
    all_words = list(words1.keys())
    all_words.extend(list(words2.keys()))
    
    dot_product = 0
    word1_norm = 0
    word2_norm = 0
    words1_keys = words1.keys()
    words2_keys = words2.keys()
    for word in all_words:
        w1_val = 0
        w2_val = 0
        if word in words1_keys:
            w1_val = words1[word]
        if word in words2_keys:
            w2_val = words2[word]
        dot_product += (w1_val * w2_val)
        word1_norm += w1_val ** 2
        word2_norm += w2_val ** 2
    word1_norm = word1_norm ** 0.5
    word2_norm = word2_norm ** 0.5

    return dot_product/(word1_norm * word2_norm)


def parse():
    parser = argparse.ArgumentParser()
    #flag for directory
    parser.add_argument("--dir", default=False)
    parser.add_argument("--doc1",default=None)
    parser.add_argument("--doc2",default=None)
    parser.add_argument("--out_csv",default=outputFile)
    parser.add_argument("--threshold",default=0.0, type=float)
    
    return parser.parse_args()


def traverseDir(dirname, threshold):
    docNames = [os.path.join(dirname,f) for f in os.listdir(dirname) if f[-4:] == ".txt"]
    print(docNames)
    docWords = [docToDict(f) for f in docNames]
    
    finalMatrix = np.empty((len(docNames), len(docNames)))
    finalMatrix[:] = np.nan
    
    finalOutput = list()
    
    for i in range(len(docNames)):
        j = i + 1
        while j < len(docNames):
            result = dotProduct(docWords[i],docWords[j])
            finalOutput.append([docNames[i],docNames[j],result])
            finalMatrix[j, i] = result
            j += 1
    print(finalOutput)

    #toCSV(docs, finalMatrix)
    #toXLSX(docNames, finalMatrix, threshold)
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


def twoDocs(filename1,filename2):
    words1 = docToDict(filename1)
    words2 = docToDict(filename2)

    return dotProduct(words1,words2)
