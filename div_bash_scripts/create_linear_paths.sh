#!/bin/bash

i=1
IFS='
'
for path in `vg paths -L -v DBLa.c.vg`; do
    graph_peak_caller find_linear_path -g DBLa.nobg DBLa.c.json $path $path.interval & 
done

