set -e  # Exit on any error

DATA_PATH=$1
if [ $# -eq 0 ]
  then
    echo "Specify path to data as first argument"
    exit
fi

MODEL=$3
echo "Using model $MODEL"

RUN_NAME=$2
OUT_DIR=$DATA_PATH/${MODEL}_${RUN_NAME}
echo "Putting results in $OUT_DIR"

mkdir -p $OUT_DIR

echo "Predicting graph"
python3 main.py --dbla_graph $DATA_PATH/dbla.json \
                --dbla_paths $DATA_PATH/graph_alignments_train.json \
                --cidra_paths $DATA_PATH/graph_alignments_train_cidra.json \
                --test_paths $DATA_PATH/graph_alignments.json \
                --cidra_seq $DATA_PATH/cidra.nobg.sequences \
                -o $OUT_DIR/graph.out \
                --classifier $MODEL


python3 check_align.py $OUT_DIR/graph.outpredicted_cidra_sequences_$MODEL.fasta $DATA_PATH/linear_predictions.fasta $DATA_PATH/cidra_test.fasta
