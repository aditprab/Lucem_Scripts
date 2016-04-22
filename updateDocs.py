import csv
import json
import re
import sys

def getCaseCite(downloadUrl):
    caseCite = re.findall('[0-9]+\.US\.[0-9]+', downloadUrl)
    if(not caseCite):
        return None
    citeNums = re.findall('[0-9]+', caseCite[0])
    csvFormattedStr = citeNums[0] + " U.S. " + citeNums[1]
    return csvFormattedStr
    
def getDate(caseCite):
    csvfp = open("facetData/supremeCourtData.csv", 'r')
    csvreader = csv.reader(csvfp, delimiter = ',')
    
    for line in csvreader:
        if(line[6] == caseCite):
            csvfp.close()
            return line[4]
    return "null"

nullDateCounter = 0
nullCaseCiteCounter = 0
nullDlUrlCounter = 0
pagerankfp = open("pageranks.txt", 'r')
for line in pagerankfp:
    temp = re.split(":", line)
    courtid = temp[0]
    pagerank = temp[1]

    jsonFile = "scotusStatistics/caseDownloads/" + courtid + ".json"
    jsonfp = open(jsonFile, 'r')
    data = json.load(jsonfp)
    jsonfp.close()

    downloadUrl = data["download_url"]
    if(downloadUrl is not None):
        caseCite = getCaseCite(downloadUrl)
    else:
        caseCite = None
        nullDlUrlCounter += 1

    if(caseCite is not None):
        date = getDate(caseCite)
    else:
        date = "null"
        caseCite = "null"
        nullCaseCiteCounter += 1
    
    data["date"] = date
    data["caseCite"] = caseCite
    data["pagerank"] = pagerank
    if(date == "null"):
        nullDateCounter += 1
    jsonfp = open(jsonFile, "w")
    json.dump(data, jsonfp)
    jsonfp.close()

print "Number of null dates: " + str(nullDateCounter)
print "Number of null case cites: " + str(nullCaseCiteCounter)
print "Number of null download URLs: " + str(nullDlUrlCounter)
pagerankfp.close()
