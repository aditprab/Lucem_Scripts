#!/bin/bash

for file in ./*.json
do
	echo -e "Getting citations from $file\n"
	sudo python getCitation.py $file
done
