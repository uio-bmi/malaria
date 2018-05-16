#!/usr/bin/env bash

n=0
cat ../domain_names.txt | while read line
do
	vg ids -i $n $line.sorted.vg > $line.incremented.vg
	n=$(($n+10000))
done
