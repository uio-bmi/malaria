#!/usr/bin/env bash                                                                                                                                                                                             
cat ../domain_names.txt | while read line
do
    vg view -Jv $line.incremented.json.processed > $line.incremented.vg.processed
done
