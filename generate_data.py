
fasta_file=$1
domain_predictions=$2
n_train=$3
n_test=$4
n_graph=$5

DATA_PATH="n_train=${n_train}n_test=${n_test}n_graph=${n_graph}"
mkdir -p data/$DATA_PATH

echo "Data path: $DATA_PATH"


python3 malaria/data_generation/main.py $1 $2 $3 $4 $5


# Align to graph
echo "Aligning"
python3 align_to_graph.py $DATA_PATH/dbla_test.fasta $DATA_PATH/dbla.vg $DATA_PATH/graph_alignments.json
python3 align_to_graph.py $DATA_PATH/dbla_train.fasta $DATA_PATH/dbla.vg $DATA_PATH/graph_alignments_train.json
python3 align_to_graph.py $DATA_PATH/cidra_train.fasta $DATA_PATH/cidra.vg $DATA_PATH/graph_alignments_train_cidra.json
