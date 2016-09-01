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
    if "completed/interactive_doit" in tle:
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
                if k in tle:
                    tuto_values[i].append(tle[k])
                    del tle[k]
            else:
                tuto_values[i].append("")

    csv_writer.writerows([["Tutorial"], tuto_keys, tuto_values[0], tuto_values[1], tuto_values[2], []])
    assert len(tle) == 0


def completed_at_least():
    titles = []
    values_tuto_done = []
    values_tuto_not_done = []
    for nblevels in range(5):
        key_format = "at_least_" + str(nblevels + 1) + "_levels_completed_tuto_%sdone"
        titles.append("Completed at least %d levels" % (nblevels + 1))
        for tuto_val, values_array in [("", values_tuto_done), ("not", values_tuto_not_done)]:
            data = agg[key_format % tuto_val]
            values_array.append(data["yes"] / (data["yes"] + data["no"]))
    csv_writer.writerows([["Completed At Least"], titles, values_tuto_done, values_tuto_not_done, []])


def specific_packs_completed():
    pack_names, active, inactive, total = ["pack"], ["active"], ["inactive"], ["total"]
    spc = agg["specific_packs_completed"]
    for pack_name in sorted(spc.keys()):
        p = spc[pack_name]
        pack_names.append(pack_name)
        active.append(p[0])
        inactive.append(p[1])
        total.append(p[0] + p[1])
    csv_writer.writerows([["Specific packs completed"], pack_names, active, inactive, total, []])


def days_levels_before_purchase():
    def value_to_range(d, step=10, max_=None):
        over_max = False
        if max_ is not None and d >= max_:
            over_max = True
            d = max_
        start_range = d - d % step
        end_range = start_range + (step - 1)
        return ("%d..%d" % (start_range, end_range)) if not over_max else ("%d+" % start_range)

    for agg_key, step, max_range in [("days_before_purchase", 10, None), ("levels_completed_before_purchase", 20, 260)]:
        dbp = agg[agg_key]
        max_value = max([int(a) for a in dbp.keys() if a != "-"])
        ranges, values = [], []

        for v in range(max_value + 1):
            r = value_to_range(v, step=step, max_=max_range)
            if r not in ranges:
                ranges.append(r)
                values.append(0)
            values[ranges.index(r)] += dbp.get(str(v), 0)

        csv_writer.writerows([[agg_key], ranges, values, []])


tuto()
completed_at_least()
specific_packs_completed()
days_levels_before_purchase()
