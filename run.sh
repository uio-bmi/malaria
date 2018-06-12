DATA_PATH=$1
if [ $# -eq 0 ]
  then
    echo "Specify path to data as first argument"
    exit
fi

OUT_DIR=$1

mkdir -p $OUT_DIR

# Align to graph
echo "Aligning"
python3 align_to_graph.py $DATA_PATH/dbla_test.fasta $DATA_PATH/dbla.vg $OUT_DIR/graph_alignments.json
python3 align_to_graph.py $DATA_PATH/dbla_train.fasta $DATA_PATH/dbla.vg $OUT_DIR/graph_alignments_train.json
python3 align_to_graph.py $DATA_PATH/cidra_train.fasta $DATA_PATH/cidra.vg $OUT_DIR/graph_alignments_train_cidra.json

echo "Predicting linear"
./predict_linear.sh $DATA_PATH/dbla_test.fasta $DATA_PATH/dbla_train.fasta $DATA_PATH/cidra_train.fasta > $OUT_DIR/linear_predictions.fasta

echo "Predicting graph"
python3 main.py $DATA_PATH/dbla.json $DATA_PATH/cidra.json $OUT_DIR/graph_alignments.json $OUT_DIR/graph_alignments_train.json $OUT_DIR/graph_alignments_train_cidra.json