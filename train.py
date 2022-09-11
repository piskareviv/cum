import cum
import argparse
import os

parser = argparse.ArgumentParser()


parser.add_argument("--input-dir", type=str)
parser.add_argument("--model", type=str)
args = parser.parse_args()


# model = cum.load_cum(args.model)
model = cum.Cum()
for file in os.listdir(args.input_dir):
    s = open(os.path.join(args.input_dir, file), 'r').read()
    model.fit(s)

cum.save_cum(args.model, model)
