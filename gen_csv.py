#́!/usr/bin/env python
import argparse
import csv
import json
import sys

parser = argparse.ArgumentParser(description="gen csv")
parser.add_argument("agg_file")
args = parser.parse_args()

agg = json.load(open(args.agg_file))

csv_writer = csv.writer(sys.stdout)
csv_writer.writerow(["Test"] * 5)

