import json
import os
import re

nullCounter = 0
counter = 0
pagerankfp = open("pageranks.txt", 'r')
for line in pagerankfp:
    temp = re.split(":", line)
    courtid = temp[0]
    pagerank = temp[1]

    jsonFile = "scotusStatistics/caseDownloads/" + courtid + ".json"
    jsonfp = open(jsonFile, 'r')
    data = json.load(jsonfp)
    jsonfp.close()

    counter += 1
    html = data["html"]
    if(not html):
        nullCounter += 1
    if(counter % 100 == 0):
        print counter

print str(nullCounter) + " documents have no html value"
pagerankfp.close()
