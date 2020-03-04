import PyPDF2
import prettytable
import math
from collections import Counter
import os
from PyPDF2 import PdfFileMerger, PdfFileReader
import nltk

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

path = "F:\playsfinal"
dir_list = os.listdir(path)
lemmatizer = WordNetLemmatizer()

merger = PdfFileMerger()

Query = input("Enter the query\n")
finalQuery = Query.split(" ")
docFreq = Counter(finalQuery)


def union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


def sortedSentence(Sentence):
    # Splitting the Sentence into words
    words = Sentence.split(" ")
    words.sort()
    newSentence = " ".join(words)
    return newSentence


def punctuation(string):
    # punctuation marks
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")
    return string


documentString = ""
pdfFileObj = open(dir_list[0], 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

i = 0
while i < pdfReader.numPages:
    pageObj = pdfReader.getPage(i)
    documentString = documentString + pageObj.extractText()
    i = i + 1

# print(documentString)

documentString2 = ""
pdfFileObj = open(dir_list[1], 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

i = 0
while i < pdfReader.numPages:
    pageObj = pdfReader.getPage(i)
    documentString2 = documentString2 + pageObj.extractText()
    i = i + 1

# print(documentString2)

documentString3 = ""
pdfFileObj = open(dir_list[2], 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

i = 0
while i < pdfReader.numPages:
    pageObj = pdfReader.getPage(i)
    documentString3 = documentString3 + pageObj.extractText()
    i = i + 1

# print(documentString3)

finalQuery = lemmatizer.lemmatize(punctuation(Query))
finalString = lemmatizer.lemmatize(punctuation(documentString.lower()))
finalString2 = lemmatizer.lemmatize(punctuation(documentString2.lower()))
finalString3 = lemmatizer.lemmatize(punctuation(documentString3.lower()))

queryAndDoc = union(punctuation(finalQuery).split(" "), punctuation(finalString).split(" "))
queryAndDoc2 = union(punctuation(finalQuery).split(" "), punctuation(finalString2).split(" "))
queryAndDoc3 = union(punctuation(finalQuery).split(" "), punctuation(finalString3).split(" "))

sortedQueryAndDoc = sorted(set(queryAndDoc))
sortedQueryAndDoc2 = sorted(set(queryAndDoc2))
sortedQueryAndDoc3 = sorted(set(queryAndDoc3))

dct = {}
for word in sortedQueryAndDoc:
    dct.update({str(word).lower(): []})

dct2 = {}
for word in sortedQueryAndDoc2:
    dct2.update({str(word).lower(): []})

dct3 = {}
for word in sortedQueryAndDoc3:
    dct3.update({str(word).lower(): []})

d = 0
docID = 0
termFreq = Counter(finalQuery.split(" "))
documentFrequency = Counter(punctuation(finalString).split())
documentFrequency2 = Counter(punctuation(finalString2).split())
documentFrequency3 = Counter(punctuation(finalString3).split())

print(documentFrequency)

for d in dct:
    if d in finalString:
        dct[d].append((1, documentFrequency[d.lower()]))
    if d in finalString2:
        dct[d].append((2, documentFrequency2[d.lower()]))
    if d in finalString3:
        dct[d].append((3, documentFrequency3[d.lower()]))

for d in dct2:
    if d in finalString:
        dct2[d].append((1, documentFrequency[d.lower()]))
    if d in finalString2:
        dct2[d].append((2, documentFrequency2[d.lower()]))
    if d in finalString3:
        dct2[d].append((3, documentFrequency3[d.lower()]))

for d in dct3:
    if d in finalString:
        dct3[d].append((1, documentFrequency[d.lower()]))
    if d in finalString2:
        dct3[d].append((2, documentFrequency2[d.lower()]))
    if d in finalString3:
        dct3[d].append((3, documentFrequency3[d.lower()]))

i = 0
tfList = []
tfList2 = []
tfList3 = []

dfList = []
dfList2 = []
dfList3 = []

idfList = []
weightedList = []
tfIdfList = []

idfList2 = []
weightedList2 = []
tfIdfList2 = []

idfList3 = []
weightedList3 = []
tfIdfList3 = []

tfListDoc1 = []
weightedListDoc1 = []

tfListDoc2 = []
weightedListDoc2 = []

tfListDoc3 = []
weightedListDoc3 = []

for i in dct:
    dfList.append(dct[i].__len__())
    if termFreq[i.lower()] == 0:
        tfList.append(0)
    else:
        tfList.append(1 + math.log(termFreq[i.lower()], 10))

for i in dct2:
    dfList2.append(dct2[i].__len__())
    if termFreq[i.lower()] == 0:
        tfList2.append(0)
    else:
        tfList2.append(1 + math.log(termFreq[i.lower()], 10))

for i in dct3:
    dfList3.append(dct3[i].__len__())
    if termFreq[i.lower()] == 0:
        tfList3.append(0)
    else:
        tfList3.append(1 + math.log(termFreq[i.lower()], 10))

for j in dct:
    if documentFrequency[j.lower()] == 0:
        tfListDoc1.append(0)
    else:
        tfListDoc1.append(1 + math.log(documentFrequency[j.lower()], 10))

for k in dct2:
    if documentFrequency2[k.lower()] == 0:
        tfListDoc2.append(0)
    else:
        tfListDoc2.append(1 + math.log(documentFrequency2[k.lower()], 10))

for l in dct3:
    if documentFrequency3[l.lower()] == 0:
        tfListDoc3.append(0)
    else:
        tfListDoc3.append(1 + math.log(documentFrequency3[l.lower()], 10))

idf = 0
for i in dct:
    if dfList[idf] != 0:
        idfList.append(math.log((3 / dfList[idf]), 10))
    else:
        idfList.append(0)
    idf = idf + 1

idf = 0
for i in dct2:
    if dfList2[idf] != 0:
        idfList2.append(math.log((3 / dfList2[idf]), 10))
    else:
        idfList2.append(0)
    idf = idf + 1

idf = 0
for i in dct3:
    if dfList3[idf] != 0:
        idfList3.append(math.log((3 / dfList3[idf]), 10))
    else:
        idfList3.append(0)
    idf = idf + 1

tfidf = 0
for i in dct:
    tfIdfList.append(tfList[tfidf] * idfList[tfidf])
    tfidf = tfidf + 1

tfidf = 0
for i in dct2:
    tfIdfList2.append(tfList2[tfidf] * idfList2[tfidf])
    tfidf = tfidf + 1

tfidf = 0
for i in dct3:
    tfIdfList3.append(tfList3[tfidf] * idfList3[tfidf])
    tfidf = tfidf + 1

print(tfIdfList)

count = 0
routeSum = 0
routeSum2 = 0
routeSum3 = 0

countDoc = 0
routeSumDoc1 = 0

countDoc2 = 0
routeSumDoc2 = 0

countDoc3 = 0
routeSumDoc3 = 0

while count < idfList.__len__():
    routeSum = routeSum + math.pow(tfIdfList[count], 2)
    count = count + 1

count = 0
while count < idfList2.__len__():
    routeSum2 = routeSum2 + math.pow(tfIdfList2[count], 2)
    count = count + 1

count = 0
while count < idfList3.__len__():
    routeSum3 = routeSum3 + math.pow(tfIdfList3[count], 2)
    count = count + 1

while countDoc < tfListDoc1.__len__():
    routeSumDoc1 = routeSumDoc1 + math.pow(tfListDoc1[countDoc], 2)
    countDoc = countDoc + 1

while countDoc2 < tfListDoc2.__len__():
    routeSumDoc2 = routeSumDoc2 + math.pow(tfListDoc2[countDoc2], 2)
    countDoc2 = countDoc2 + 1

while countDoc3 < tfListDoc3.__len__():
    routeSumDoc3 = routeSumDoc3 + math.pow(tfListDoc3[countDoc3], 2)
    countDoc3 = countDoc3 + 1

normalise = math.sqrt(routeSum)
normalise2 = math.sqrt(routeSum2)
normalise3 = math.sqrt(routeSum3)

normaliseDoc1 = math.sqrt(routeSumDoc1)
normaliseDoc2 = math.sqrt(routeSumDoc2)
normaliseDoc3 = math.sqrt(routeSumDoc3)

count = 0
for i in dct:
    if normalise != 0:
        weightedList.append(tfIdfList[count] / normalise)
    else:
        weightedList.append(0)
    count = count + 1

count = 0
for i in dct2:
    if normalise2 != 0:
        weightedList2.append(tfIdfList2[count] / normalise2)
    else:
        weightedList2.append(0)
    count = count + 1

count = 0
for i in dct3:
    if normalise3 != 0:
        weightedList3.append(tfIdfList3[count] / normalise3)
    else:
        weightedList3.append(0)
    count = count + 1

count = 0
for i in dct:
    if normaliseDoc1 != 0:
        weightedListDoc1.append(tfListDoc1[count] / normaliseDoc1)
    else:
        weightedListDoc1.append(0)
    count = count + 1

count = 0
for i in dct2:
    if normaliseDoc2 != 0:
        weightedListDoc2.append(tfListDoc2[count] / normaliseDoc2)
    else:
        weightedListDoc2.append(0)
    count = count + 1

count = 0
for i in dct3:
    if normaliseDoc3 != 0:
        weightedListDoc3.append(tfListDoc3[count] / normaliseDoc3)
    else:
        weightedListDoc3.append(0)
    count = count + 1

finalWeightListDoc1 = []
finalWeightListDoc2 = []
finalWeightListDoc3 = []

count = 0
for i in dct:
    finalWeightListDoc1.append(weightedList[count] * weightedListDoc1[count])
    count = count + 1

count = 0
for i in dct2:
    finalWeightListDoc2.append(weightedList2[count] * weightedListDoc2[count])
    count = count + 1

count = 0
for i in dct3:
    finalWeightListDoc3.append(weightedList3[count] * weightedListDoc3[count])
    count = count + 1

total1 = 0
total2 = 0
total3 = 0
count = 0
for i in finalWeightListDoc1:
    total1 = total1 + finalWeightListDoc1[count]
    count = count + 1

count = 0
for i in finalWeightListDoc2:
    total2 = total2 + finalWeightListDoc2[count]
    count = count + 1

count = 0
for i in finalWeightListDoc3:
    total3 = total3 + finalWeightListDoc3[count]
    count = count + 1

x = prettytable.PrettyTable(["word", "tf-raw", "tf-weight", "posting list", "df", "idf", "tf-idf", "normalised weight"])
count = 0
for i in dct:
    x.add_row([i, termFreq[i.lower()], tfList[count], dct[i], dfList[count], idfList[count], tfIdfList[count],
               weightedList[count]])
    count = count + 1

print("Input Query is : " + Query)
print(x)

print("doc1 finalized weight")
print(total1)
print("doc2 finalized weight")
print(total2)
print("doc3 finalized weight")
print(total3)
