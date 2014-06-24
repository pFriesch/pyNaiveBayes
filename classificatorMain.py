from collections import OrderedDict
import sys
from builtins import print
import os
import collections
import math


__author__ = 's0540030,s0540040,s0539748'

# Wir Klassifizieren Texte, das geht so:
# Wir übergeben einen Ordner wo Beispieltexte drin sind,
# wir lernen mit den Texten die Worthäufigkeit für das Thema.
# Dann lassen wir den Klassifikator auf die richtigen Texte los
# und da wir die Worthäufigkeit für jedes Thema haben, sollte der Klassifikator alles richtig einordnen

def main(argv):
    dir = "data"
    allFiles = 0
    classes = getClasses(dir)
    learnFilesForClass = dict()
    learnWords = dict()

    for classification in classes:
        learnDirectory = "data/"+str(classification)+"/train"
        learnFilesForClass[classification] = os.listdir(learnDirectory)
        allFiles += len(learnFilesForClass[classification])

        learnWords[classification] = getLearnWords(learnFilesForClass[classification], learnDirectory)

    prio = dict()
    termPrio = dict()
    for classification in classes:
        training(prio, termPrio, classification, allFiles, learnWords.get(classification), learnFilesForClass[classification])

    for item in termPrio.items():
        print(item)
    print("-----")
    #testing
    classesResult = dict()
    for classification in classes:
        filesDir = dict()
        filesDir[classification] = os.listdir("data/"+classification+"/test/")
        classesResult[classification] = dict()
        for file in filesDir[classification]:
            sum = test(prio, termPrio, "data/"+classification+"/test/"+str(file), classification)
            classesResult[classification][file] = max(sum, key=sum.get)
    for result in classesResult.items():
        resultOrdered = collections.OrderedDict(sorted(result[1].items()))
        print(resultOrdered)


def test(prio, termPrio, testDoc, testGroup):
    wordList = list()
    wordList = splitFile(testDoc)
    sum = dict()
    for word in wordList:
        if word in termPrio.keys():
            groupPrio = termPrio.get(word)
            for group in groupPrio.keys():
                if group in sum:
                    sum[group] += math.log10(groupPrio.get(group))
                else:
                    sum[group] = math.log10(prio.get(group))
                    sum[group] += math.log10(groupPrio.get(group))
    return sum


def training(prio, termPrio, classification, allFiles, learnWords, learnFiles):
    prio[classification] = len(learnFiles)/allFiles
    tokenCount = countTokensForClass(learnWords, classification)

    #rechne die TermPrio aus also condprob
    for token in tokenCount:
        #wenn classe noch nicht drin ist, muss sie erstellt werden
        if token not in termPrio:
            classDict = dict()
            classDict[classification] = tokenCount.get(token).get(classification)/len(learnWords)
            termPrio[token] = classDict
        else:
            termPrio[token][classification] = tokenCount.get(token).get(classification)/len(learnWords)
    return termPrio


def countTokensForClass(learnWords, classification):
    tokenCount = dict()

    for word in learnWords:
        if classification in tokenCount:
            tokenCount[word][classification] = learnWords.count(word)
        else:
            classDict = dict()
            classDict[classification] = learnWords.count(word)
            tokenCount[word] = classDict

    return tokenCount


def getClasses(dir):
    classes = os.listdir(dir)
    return classes


def getLearnWords(learnFiles, learnDirectory):

    learnWords = list()
    for file in learnFiles:
        learnWords.extend(splitFile(str(learnDirectory)+"/"+str(file)))

    return learnWords


def splitFile(file):
    #Lese Datei und splitte
    with open(file, 'r', errors="ignore", encoding='utf-8') as f:
        words = f.read().split(' ')

    #entferne Sonderzeichen
    wordList = list()
    for word in words:
        wordList.append(word.replace('.', '').replace(',', '').replace("\"", "").replace("\n", "").replace("(", "").replace(")", ""))

    return wordList

if __name__ == "__main__": main(sys.argv)