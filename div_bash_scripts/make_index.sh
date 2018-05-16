#!/bin/bash

i=1
IFS='
'
for path in `vg paths -L -v graph.vg`; do
	echo "i: $i"

	if [ -f $path.kmers ]; then
		echo "Kmers already created for $path"
	else	
		vg mod -r $path graph.vg | vg mod -N - > graph_$path.vg && vg kmers --path-only -gB -k 16 -p graph_$path.vg > $path.kmers &
		#vg mod -r $path graph.vg | vg mod -N - > graph_$path.vg && vg kmers --path-only -g -k 256 -p graph_$path.vg > $path.kmers &
		i=$((i+1))
		if (( i > 410 )); then
		    break
		fi	
	fi
done

#Not working: vg index -g graph.gcsa $(for path in `vg paths -L -v graph.vg`; do echo "-i $path.kmers"; done) -p 
#cat *.kmers > all.kmers
#vg index -g graph.gcsa -i all.kmers -X 3 -p graph.vg
