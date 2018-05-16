#!/usr/bin/env bash                                                                                                                                                                                             
cat ../domain_names.txt | while read line
do
    vg view -Vj $line.incremented.vg > $line.incremented.json
done
