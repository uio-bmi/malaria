
# ./get_msa_score.sh query_fasta true_sequences_fasta
# Will search pairs
awk '/^>/{print s? s"\n"$0:$0;s="";next}{s=s sprintf("%s",$0)}END{if(s)print s}' $1 > one_line.tmp                                                                                                             
   
   cat one_line.tmp | while read -r ONE; do
       read -r TWO
       # SPlit on space
       IFS=' ' read -r id string <<< "$ONE"
      # Remove ">"
      id2="${id//>}"
      echo $id2 
    
    echo "$id2"
    echo ">${id2}_predicted" > seqs.tmp
    echo $TWO >> seqs.tmp
    samtools faidx $2 $id2 >> seqs.tmp
    clustalo -i seqs.tmp
 
 
 done

