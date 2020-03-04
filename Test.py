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


def punctuation(string):
    # punctuation marks
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")
    return string


documentString = []
finalString = []
documentFrequencyy = []

secondCount = 0
while secondCount < dir_list.__len__():
    Strstr = ""
    pdfFileObj = open(dir_list[secondCount], 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    i = 0
    while i < pdfReader.numPages:
        pageObj = pdfReader.getPage(i)
        Strstr = Strstr + pageObj.extractText()
        i = i + 1
    finalString.append(lemmatizer.lemmatize(punctuation(Strstr.lower())))
    documentFrequencyy.append(Counter(punctuation(finalString[secondCount]).split()))
    secondCount = secondCount + 1

bigCount = 0
while bigCount < dir_list.__len__():
    pdfFileObj = open(dir_list[bigCount], 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    finalQuery = lemmatizer.lemmatize(punctuation(Query))

    queryAndDoc = union(punctuation(finalQuery).split(" "), punctuation(finalString[bigCount]).split(" "))
    sortedQueryAndDoc = sorted(set(queryAndDoc))

    dct = {}
    for word in sortedQueryAndDoc:
        dct.update({str(word).lower(): []})

    d = 0
    docID = 0
    termFreq = Counter(finalQuery.split(" "))

    for d in dct:
        for dctCount in range(0, len(dir_list)):
            if d in finalString[dctCount]:
                dct[d].append((dctCount + 1, documentFrequencyy[dctCount][d.lower()]))

    i = 0
    tfList = []
    dfList = []
    idfList = []
    weightedList = []
    tfIdfList = []

    tfListDoc1 = []
    weightedListDoc1 = []

    for i in dct:
        dfList.append(dct[i].__len__())
        if termFreq[i.lower()] == 0:
            tfList.append(0)
        else:
            tfList.append(1 + math.log(termFreq[i.lower()], 10))

    for j in dct:
        if documentFrequencyy[bigCount][j.lower()] == 0:
            tfListDoc1.append(0)
        else:
            tfListDoc1.append(1 + math.log(documentFrequencyy[bigCount][j.lower()], 10))

    idf = 0
    for i in dct:
        if dfList[idf] != 0:
            idfList.append(math.log((3 / dfList[idf]), 10))
        else:
            idfList.append(0)
        idf = idf + 1

    tfidf = 0
    for i in dct:
        tfIdfList.append(tfList[tfidf] * idfList[tfidf])
        tfidf = tfidf + 1

    count = 0
    routeSum = 0
    countDoc = 0
    routeSumDoc1 = 0

    while count < idfList.__len__():
        routeSum = routeSum + math.pow(tfIdfList[count], 2)
        count = count + 1

    while countDoc < tfListDoc1.__len__():
        routeSumDoc1 = routeSumDoc1 + math.pow(tfListDoc1[countDoc], 2)
        countDoc = countDoc + 1

    normalise = math.sqrt(routeSum)
    normaliseDoc1 = math.sqrt(routeSumDoc1)

    count = 0
    for i in dct:
        if normalise != 0:
            weightedList.append(tfIdfList[count] / normalise)
        else:
            weightedList.append(0)
        count = count + 1

    count = 0
    for i in dct:
        if normaliseDoc1 != 0:
            weightedListDoc1.append(tfListDoc1[count] / normaliseDoc1)
        else:
            weightedListDoc1.append(0)
        count = count + 1

    finalWeightListDoc1 = []

    count = 0
    for i in dct:
        finalWeightListDoc1.append(weightedList[count] * weightedListDoc1[count])
        count = count + 1

    total1 = 0
    count = 0
    for i in finalWeightListDoc1:
        total1 = total1 + finalWeightListDoc1[count]
        count = count + 1

    # if bigCount == 0:
    #     x = prettytable.PrettyTable(
    #         ["word", "tf-raw", "tf-weight", "posting list", "df", "idf", "tf-idf", "normalised weight"])
    #     count = 0
    #     for i in dct:
    #         x.add_row([i, termFreq[i.lower()], tfList[count], dct[i], dfList[count], idfList[count], tfIdfList[count],
    #                    weightedList[count]])
    #         count = count + 1
    #
    #     print(x)

    x = bigCount + 1
    print(str(dir_list[bigCount]) + " score is: " + str(total1))

    bigCount = bigCount + 1
