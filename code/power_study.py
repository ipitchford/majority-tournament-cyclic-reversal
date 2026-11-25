"""Reproduce the manuscript's Monte Carlo sensitivity check.

The normal model is the fixed-n Gaussian electorate limit. The table does not
simulate individual ballots. The label order, packing, link, and threshold are
fixed for each design. Independent seeded streams are used for each row.
"""
import math
import numpy as np
from scipy.special import ndtr, expit
from probit_test import probit_log_e


def experiment(n, sd, model, repetitions=256):
    sequence = np.random.SeedSequence([731204, n, round(100*sd), int(model == 'probit')])
    rng = np.random.Generator(np.random.PCG64(sequence))
    i, j = np.triu_indices(n, 1)
    count = 0
    for _ in range(repetitions):
        strength = rng.normal(0, sd, n)
        gap = strength[i] - strength[j]
        prob = ndtr(gap) if model == 'probit' else expit(1.7 * gap)
        edges = np.zeros((n,n), dtype=bool)
        edges[i,j] = rng.random(i.size) < prob
        edges[j,i] = ~edges[i,j]
        count += probit_log_e(edges) >= math.log(20)
    return count


if __name__ == '__main__':
    print('n,sd,model,rejections,repetitions', flush=True)
    for n, sd in [(90,1.0), (180,1.0), (360,1.0), (600,1.0), (360,0.5), (360,1.5)]:
        for model in ['logit','probit']:
            print(f'{n},{sd:.1f},{model},{experiment(n,sd,model)},256', flush=True)
