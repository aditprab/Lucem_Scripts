import csv
import json
import re
import sys

pagerankfp = open("pageranks.txt", 'r')

notFoundCounter = 0

csvreader = csv.reader(open("facetData/supremeCourtDataNewCol.csv", 'r+'), delimiter = ',')
lines = [l for l in csvreader]

for line in pagerankfp:
    
    temp = re.split(":", line)
    courtid = temp[0]

    #get json file assosciated with courtId. 

    jsonFile = "scotus/" + courtid + ".json"
    jsonfp = open(jsonFile, 'r')
    data = json.load(jsonfp)
    jsonfp.close()

    html = data["html"]
    if(len(html) == 0):
        continue

    #get caseCite assosciated with courtId.
    caseCite = data["caseCite"]
   

    #look for line in the csv array  with this caseCite.
    foundFlag = False
    
    for index,data in enumerate(lines):
            if(data[6] == caseCite):
                 foundFlag = True
                 break 

    if(foundFlag == False):
        notFoundCounter = notFoundCounter + 1

    else:
        #found it. line has data.
        print "Line was found. Adding courtId " + courtid + " to line " + str(index) + " which has caseCite " + caseCite
        lines[index][53] = courtid
    


#do one more loop through the array and fill in all the ones without courtId with NULL
for index, data in enumerate(lines):
        if(not data[53]):
            lines[index][53] = "NULL" 
 
writer = csv.writer(open("facetData/supremeCourtDataNewColOutput.csv", "w"))
writer.writerows(lines)
