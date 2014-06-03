import sys
from builtins import print
import os
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


    termPrio = dict()
    for classification in classes:
        training(termPrio, classification, allFiles, learnWords.get(classification), learnFilesForClass[classification])

        print(termPrio)



def training(termPrio, classification, allFiles, learnWords, learnFiles):
    prio = dict()
    prio[classification] = len(learnFiles)/allFiles
    tokenCount = countTokensForClass(learnWords, classification)

    #rechne die TermPrio aus also condprob
    for token in tokenCount:
        if classification in termPrio:
            termPrio[token][classification] = tokenCount.get(token).get(classification)/len(learnWords)
        else:
            #wenn classe noch nicht drin ist, muss sie erstellt werden
            classDict = dict()
            classDict[classification] = tokenCount.get(token).get(classification)/len(learnWords)
            termPrio[token] = classDict

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