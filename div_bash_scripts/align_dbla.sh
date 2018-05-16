#!/usr/bin/env bash                                                                                                                                                                                             
> alignments.txt
> alignments_linear.txt
cat subset4.txt | while read line
do
    echo "Aligning.."
    vg align -s $line DBLa.c.vg | vg view -aj - >> alignments.txt  #| grep -o -P '.{0,0}identity.{0,7}'
    vg align -s $line linear_graph.vg | vg view -aj - >> alignments_linear.txt
done
wait

