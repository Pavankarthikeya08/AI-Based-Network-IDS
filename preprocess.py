#!/usr/bin/env python3
import argparse
import pandas as pd
from utils import FEATURE_COLS

parser = argparse.ArgumentParser()
parser.add_argument('--in', dest='inp', required=True)
parser.add_argument('--out', required=True)
args = parser.parse_args()

df = pd.read_csv(args.inp)
cols = [c for c in FEATURE_COLS if c in df.columns]
df = df[cols + ['label']] if 'label' in df.columns else df[cols]
for c in cols:
    df[c] = df[c].fillna(0)
df.to_csv(args.out, index=False)
print('Saved cleaned CSV to', args.out)
