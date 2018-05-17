#!/usr/bin/env bash                                                                                                                                                                                             
# Usage: ./predict_graph.sh /home/ivar/data/malaria/pfemp_sequences/150genes/dbla_test.fasta /home/ivar/data/malaria/pfemp_sequences/150genes/dbla.vg

awk '/^>/{print s? s"\n"$0:$0;s="";next}{s=s sprintf("%s",$0)}END{if(s)print s}' $1 > one_line.tmp
> "alignments.json"
cat one_line.tmp | while read -r ONE; do
    read -r TWO
    # SPlit on space
    IFS=' ' read -r id string <<< "$ONE"
    # Remove ">"
    id2="${id//>}"

    echo "Aligning"
    vg align -Q $id2 -s $TWO $2 | vg view -aj - >> alignments.json  #| grep -o -P '.{0,0}identity.{0,7}'
done

python3 correlation.py alignments.json

