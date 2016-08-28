#́!/usr/bin/env python
import json
import argparse
from progress import counter

from clientdata import client_data_generator
from aggregate import aggregate_cd, aggregate_second_pass


parser = argparse.ArgumentParser(description="stats")
subparsers = parser.add_subparsers(dest="command")
ga_parser = subparsers.add_parser("ga-data")
ga_parser.add_argument("ga_file")
ga_parser.add_argument("stats_file")
remove_ids_parser = subparsers.add_parser("remove-ids")
remove_ids_parser.add_argument("ga_file")
remove_ids_parser.add_argument("ids_file")
remove_ids_parser.add_argument("ga_without_ids_file")
stats_parser = subparsers.add_parser("stats-agg")
stats_parser.add_argument("stats_file")
stats_parser.add_argument("final_file")
args = parser.parse_args()

if args.command == "ga-data":
    nbc = 0
    cdg = client_data_generator(args.ga_file)
    fstats = open(args.stats_file, "wt")
    for c in counter.Counter('Processing: ').iter(cdg):
        c.compute_stats()
        d = c.stats
        d.update({"id": c.id})
        fstats.write(json.dumps(d) + "\n")
        nbc += 1
        if nbc > 150:
            break
    fstats.close()
elif args.command == "remove-ids":
    ignored_ids = []
    for ignored_id in open(args.ids_file):
        ignored_ids.append(ignored_id.strip())
    fga = open(args.ga_file)
    fga_no_ids = open(args.ga_without_ids_file, "wt")
    for line in fga:
        parsed = json.loads(line)
        client_id = parsed[0]
        if client_id not in ignored_ids:
            fga_no_ids.write(line)
        else:
            print("ignored " + client_id)
elif args.command == "stats-agg":
    res = None
    for l in open(args.stats_file):
        res = aggregate_cd(res, json.loads(l))
    aggregate_second_pass(res)
    json.dump(res, open(args.final_file, "wt"), sort_keys=True, indent=2)
