import json, sys

jsonFile = sys.argv[1]
jsonFile = jsonFile[2:]
cid = str.rstrip(jsonFile, ".json")
jsonfp = open(jsonFile, 'r')
values = json.load(jsonfp)
jsonfp.close()

filename = cid + ".txt"
filefp = open(filename, 'w')

citationArray = values["opinions_cited"]
for citation in citationArray:
	citeid = citation[50:-1]
	filefp.write(str(citeid) + "\n")
#	print str(citeid)

filefp.close()
