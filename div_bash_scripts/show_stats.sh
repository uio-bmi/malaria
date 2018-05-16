#!/usr/bin/env bash

cat ../domain_names.txt | while read line
do
   echo "----- $line -----"
   vg stats --heads $line.incremented.vg.processed
   vg stats --tails $line.incremented.vg.processed
   vg stats -lz $line.incremented.vg.processed
done
