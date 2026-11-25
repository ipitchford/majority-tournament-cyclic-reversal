# SPDX-License-Identifier: MIT
"""Declared tolerance for the Monte Carlo study: identical counts; every log ratio within 0.01 of results/small_reversals.json."""
import json, sys
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2])); bad = []
for n, x in a['small_n'].items():
    y = b['small_n'][n]
    if x['classes'] != y['classes'] or x['reversals'] != y['reversals'] or abs(x['min_log_ratio_higher_lin_over_lower_lin'] - y['min_log_ratio_higher_lin_over_lower_lin']) > 0.01:
        bad.append(n)
for n, x in a['blocks'].items():
    y = b['blocks'][n]
    if x['compositions'] != y['compositions'] or abs(x['best_log_ratio_more_cyclic_over_less'] - y['best_log_ratio_more_cyclic_over_less']) > 0.01:
        bad.append('blocks ' + n)
if len(a['pairs']) != len(b['pairs']):
    bad.append('pairs')
for x, y in zip(a['pairs'], b['pairs']):
    if abs(x['log_ratio_mean'] - y['log_ratio_mean']) > 0.01:
        bad.append(str(x['more_cyclic_blocks']))
print('all log ratios within 0.01:', not bad, bad)
sys.exit(1 if bad else 0)
