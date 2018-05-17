# Running: ./predict_linear.sh /home/ivar/data/malaria/pfemp_sequences/150genes/dbla_test.fasta /home/ivar/data/malaria/pfemp_sequences/150genes/dbla.fasta /home/ivar/data/malaria/pfemp_sequences/150genes/cidra.fasta > linear_predictions.fasta

blastn -query $1 -db $2 -outfmt 6 -max_target_seqs 1 > blast_res.tmp 
cut -f1,2 blast_res.tmp > original_to_matched_ids.tmp
cut -f2 blast_res.tmp > matched_ids.tmp
faSomeRecords $3 matched_ids.tmp tmp_predictions

python3 replace_fasta_ids.py original_to_matched_ids.tmp tmp_predictions
