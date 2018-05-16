#!/usr/bin/env bash
cat ../domain_names.txt | while read line
do
   echo $line
   vg mod -c $line.vg > $line.sorted.vg &
done

