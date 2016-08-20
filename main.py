#́!/usr/bin/env python
import json
import argparse

from clientdata import client_data_generator
from aggregate import aggregate_cd


parser = argparse.ArgumentParser(description="stats")
subparsers = parser.add_subparsers(dest="command")
ga_parser = subparsers.add_parser("ga-data")
ga_parser.add_argument("ga_file")
ga_parser.add_argument("stats_file")
stats_parser = subparsers.add_parser("stats-agg")
stats_parser.add_argument("stats_file")
stats_parser.add_argument("final_file")
args = parser.parse_args()

if args.command == "ga-data":
    nbc = 0
    cdg = client_data_generator(args.ga_file)
    fstats = open(args.stats_file, "wt")
    for c in cdg:
        c.compute_stats()
        d = c.stats
        d.update({"id": c.id})
        fstats.write(json.dumps(d) + "\n")
        nbc += 1
        if nbc > 150:
            break
    fstats.close()
elif args.command == "stats-agg":
    res = None
    for l in open(args.stats_file):
        res = aggregate_cd(res, json.loads(l))
    json.dump(res, open(args.final_file, "wt"), sort_keys=True, indent=2)
