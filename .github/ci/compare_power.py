# SPDX-License-Identifier: MIT
"""Declared off-platform tolerance for results/power.csv: same rows and columns, each rejection count within 1."""
import csv, sys
a = list(csv.reader(open(sys.argv[1]))); b = list(csv.reader(open(sys.argv[2])))
ok = len(a) == len(b) and a[0] == b[0] and all(x[:3] == y[:3] and x[4] == y[4] and abs(int(x[3]) - int(y[3])) <= 1 for x, y in zip(a[1:], b[1:]))
print('power.csv within declared tolerance:', ok)
sys.exit(0 if ok else 1)
