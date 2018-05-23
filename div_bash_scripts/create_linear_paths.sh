#!/bin/bash

i=1
IFS='
'
for path in `vg paths -L -v $1.vg`; do
    graph_peak_caller find_linear_path -g $1.nobg $1.json $path $path.interval & 
done

