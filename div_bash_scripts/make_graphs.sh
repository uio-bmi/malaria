#!/usr/bin/env bash

cat ../domain_names.txt | while read line
do
	vg construct -M $line.msa.fasta -F fasta -p > $line.vg
done
