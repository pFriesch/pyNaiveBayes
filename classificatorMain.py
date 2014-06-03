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
    classes = getClasses(dir)

    for classification in classes:
        learnDirectory = "data/"+str(classification)+"/train"
        learnFiles = os.listdir(learnDirectory)

        learnWords = dict()
        learnWords[classification] = getLearnWords(learnFiles, learnDirectory)

        for word in learnWords.values():
           print(word)


def getClasses(dir):
    classes = os.listdir(dir)
    return classes

def getLearnWords(learnFiles, learnDirectory):

    learnWords = list()
    for file in learnFiles:
        learnWords.append(splitFile(str(learnDirectory)+"/"+str(file)))

    return learnWords

def splitFile(file):
    #Lese Datei und splitte
    #TODO: Sport/train/s031.txt hat ein fehlerhaftes Zeichen!!!
    with open(file, 'r', errors="ignore") as f:
        words = f.read().split(' ')

    #entferne (. , ")  TODO: Ist das richtig? Steht nirgends
    wordList = list()
    for word in words:
        wordList.append(word.replace('.', '').replace(',', '').replace("\"", ""))

    return wordList

#def train():



if __name__ == "__main__": main(sys.argv)