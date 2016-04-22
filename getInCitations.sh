#!/bin/bash

for file in ./*.json
do
	echo -e "Getting incoming citations from $file\n"
	sudo python getInCitation.py $file
done
