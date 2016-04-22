# Used to create docToPost.json for indexing into Solr

import re, cgi, sys, json, math

jsonFile = sys.argv[1]
jsonFile = jsonFile[2:]
cid = str.rstrip(jsonFile, ".json")
jsonFilePointer = open(jsonFile, 'r')
values = json.load(jsonFilePointer)
jsonFilePointer.close()

htmlBody = values["html"]
#file = open("hopeThisWorks.json", 'w')
#writeString = "[{\n\"html\":\"" + htmlBody + "\"\n}]"
#file.write(writeString)
#file.close()


file = open("docToPost.json", 'w')
htmlBody =  json.dumps(htmlBody)
tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
no_tags = tag_re.sub('', htmlBody)
ready_for_web = cgi.escape(no_tags)
writeString = "\"html\":" + ready_for_web

baseIndex = 0;
endIndex = 20000;
noQuotesString = ready_for_web[1:-1]
chunkCount = len(noQuotesString) / 20000
if len(noQuotesString) % 20000 != 0:
	chunkCount = chunkCount + 1

file.write("[\n{\n")
for counter in range(0, chunkCount):
	if counter != chunkCount - 1:
		if noQuotesString[endIndex - 1] == "\\":
			endIndex = endIndex + 1
	file.write("\"html" + str(counter) + "\":\"" + noQuotesString[baseIndex:endIndex] + "\",\n")
	file.write("\"html" + str(counter) + "_txt_en\":\"" + noQuotesString[baseIndex:endIndex] + "\",\n")
	baseIndex = endIndex
	endIndex = endIndex + 20000;
file.write("\"courtid\":" + str(cid))
file.write("\n}\n]\n")
	

#file.write(writeString)
file.close()
