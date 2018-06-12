import argparse

def func(s):
    return s*2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("predictor_graph", type=func)
    # parser.add_argument("train_dbla_paths")
    # parser.add_argument("train_cidra_paths")
    # parser.add_argument("-o", "--outfile")
    args = parser.parse_args()
    return args
if __name__ == "__main__":
    main()
    print(args.predictor_graph)
