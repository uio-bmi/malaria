#!/usr/bin/env bash
cat ../domain_names.txt | while read line
do
   echo $line
   #awk "/^>/ {n++} n>100 {exit} {print}" ../1000genes/${line}_1000_train_dna.fasta_all.fasta > $line.fasta
   head -n 200 ../1000genes/${line}_1000_train_dna.fasta_all.fasta > $line.fasta
done
