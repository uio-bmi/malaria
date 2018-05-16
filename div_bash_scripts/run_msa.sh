#!/usr/bin/env bash

cat ../domain_names.txt | while read line
do
	echo "Running $line"
	backtranseq $line.fasta  $line.dna.fasta && clustalo -i $line.dna.fasta -v -o $line.msa.fasta &
done
