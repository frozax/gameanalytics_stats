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


def tuto():
    tle = agg["tuto_last_event"]
    tle["completed/done"] += tle["completed/interactive_doit"]  # happens if double tap at end of tutorial
    del tle["completed/interactive_doit"]
    del tle["-"]
    total = 0
    for k in tle:
        total += tle[k]
    tle["total"] = total

    # Last step of the tutorial
    steps = [("unknown", ["start/intro_thermonumbers", None, None]),
             ("1. Numbers explanation", [None, "back/intro_thermonumbers", "skip/intro_thermonumbers"]),
             ("2. Filling explanation", [None, "back/intro_fillfrombase", "skip/intro_fillfrombase"]),
             ("3. Interaction tap", [None, None, "back/interactive_fill"]),
             ("4. Interaction double-tap", [None, None, "back/interactive_empty"]),
             ("5. Interaction logic", [None, None, "back/interactive_complex"]),
             ("6. Interaction complete level", [None, None, "back/interactive_doit"]),
             ("7. Done", ["completed/done", "back/done", None]),
             ("Total", ["total", None, None])
             ]

    tuto_keys = []
    tuto_values = [[], [], []]

    for name, keys in steps:
        tuto_keys.append("\"%s\"" % name)
        for i, k in enumerate(keys):
            if k:
                tuto_values[i].append(tle[k])
                del tle[k]
            else:
                tuto_values[i].append("")

    csv_writer.writerows([["Tutorial"], tuto_keys, tuto_values[0], tuto_values[1], tuto_values[2], []])
    assert len(tle) == 0

tuto()