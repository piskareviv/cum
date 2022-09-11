import random
import cum
import argparse
import os

parser = argparse.ArgumentParser()


parser.add_argument("--prefix",  default="")
parser.add_argument("--model", type=str)
parser.add_argument("--length", type=int)
# parser.add_argument("--seed", type=int, default=-1)
args = parser.parse_args()


seed = random.randint(0, 2**32-1)
model = cum.load_cum(args.model)
res = model.generate(args.prefix, args.length, seed=seed)
print(res)
