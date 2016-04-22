import csv
import json
import re
import sys
from bs4 import BeautifulSoup

def lookupMeaning(key, value):
    csvfp = open("/data/solr-5.4.1/facetData/dataMeaning.csv")
    csvreader = csv.reader(csvfp, delimiter =",")

    for line in csvreader:
        if((line[0] == key) and (line[1] == value)):
            csvfp.close()
            return line[2]
    csvfp.close()


pagerankfp = open("pageranks.txt", 'r')
for line in pagerankfp:
    temp = re.split(":", line)
    courtid = temp[0]

    jsonFile = "scotusToUpdate/" + courtid + ".json"
    jsonfp = open(jsonFile, 'r')
    data = json.load(jsonfp)
    jsonfp.close()

    html = data["html"]
    if(len(html) == 0):
        continue

    caseCite = data["caseCite"]


    csvfp = open("facetData/supremeCourtData.csv", 'r')
    csvreader = csv.reader(csvfp, delimiter = ',')
    
    foundFlag = False

    for line in csvreader:
        if(line[6] == caseCite):
            #match, pull fields and put into list.
            chiefJustice = line[12]
            petitioner = lookupMeaning("petitioner", line[17])
            respondent = lookupMeaning("respondent", line[19])
            issue = lookupMeaning("issue", line[39])
            issueArea = lookupMeaning("issueArea", line[40])
            foundFlag = True
            break
    
    if(foundFlag == False):
        chiefJustice = "null"
        petitioner = "null"
        respondent = "null"
        issue = "null"
        issueArea = "null"
    
    data["chiefJustice"] = chiefJustice
    data["petitioner"] = petitioner
    data["respondent"] = respondent
    data["issue"] = issue
    data["issueArea"] = issueArea

    jsonfp = open(jsonFile, "w")
    json.dump(data, jsonfp)
    jsonfp.close()

    csvfp.close()

pagerankfp.close() 
