import json, sys

jsonFile = sys.argv[1]
jsonFile = jsonFile[2:]
cid = str.rstrip(jsonFile, ".json")
jsonfp = open(jsonFile, 'r')
values = json.load(jsonfp)
jsonfp.close()

citationArray = values["opinions_cited"]
for citation in citationArray:
	citeid = citation[50:-1]
	infilefp = open(citeid + ".txt", 'a+')
	infilefp.write(cid + "\n")
	infilefp.close()
