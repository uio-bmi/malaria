DATA_PATH=$1
if [ $# -eq 0 ]
  then
    echo "Specify path to data as first argument"
    exit
fi

RUN_NAME=$1
OUT_DIR=$DATA_PATH/$RUN_NAME

mkdir -p $OUT_DIR

echo "Predicting linear"
./predict_linear.sh $DATA_PATH/dbla_test.fasta $DATA_PATH/dbla_train.fasta $DATA_PATH/cidra_train.fasta > $OUT_DIR/linear_predictions.fasta

echo "Predicting graph"
python3 main.py --dbla_graph $DATA_PATH/dbla.json \
                --dbla_paths $DATA_PATH/graph_alignments_train.json \
                --cidra_paths $DATA_PATH/graph_alignments_train_cidra.json \
                --test_paths DATA_PATH/graph_alignments.json \
                --cidra_seq DATA_PATH/cidra.nobg.sequences \
                -o OUT_DIR/testrun