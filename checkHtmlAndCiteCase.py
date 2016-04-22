# Used to add some KV pairs to every json file

import csv
import json
import re
import sys
from bs4 import BeautifulSoup

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

counter = 0
nullDateCounter = 0
nullCaseCiteCounter = 0
nullHtmlCounter = 0
pagerankfp = open("pageranks.txt", 'r')
for line in pagerankfp:
    temp = re.split(":", line)
    courtid = temp[0]
    pagerank = temp[1]

    counter += 1
    if(counter % 200 == 0):
        print counter

    jsonFile = "scotusUpdated/caseDownloads/" + courtid + ".json"
    jsonfp = open(jsonFile, 'r')
    data = json.load(jsonfp)
    jsonfp.close()

    html = data["html"]
    if(len(html) == 0):
        nullHtmlCounter += 1
        continue
    soup = BeautifulSoup(html)
    caseCiteTag = soup.findAll("p", { "class" : "case_cite" } )
    boolFlag = False
    for tag in caseCiteTag:
        caseCite = tag.text
        isItThere = re.findall('[0-9]+ U\.S\. [0-9]+', caseCite)
        if(isItThere):
#            caseCite = None    I have no idea why this line was here during our hackathon. leaving it here just incase commenting it out is bad (highly unlikely)
            boolFlag = True
            break
    if(boolFlag == False):
        caseCite = None

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
print "Number of null download URLs: " + str(nullHtmlCounter)
pagerankfp.close()
