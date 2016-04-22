#!/bin/bash

for file in ./*.json
do
  sudo python sanitizer.py $file
  echo -e "\n\t\tRUNNING bin/post ON $file\n"
  /data/solr-5.4.1/bin/post -c anothaOne_shard1_replica1 docToPost.json -commit no
done
echo -e "\t************************************\n"
echo -e "\t*DON'T FORGET TO COMMIT THE CHANGES*\n"
echo -e "\t************************************\n"
