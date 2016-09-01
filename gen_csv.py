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


def value_to_range(d, step=10, max_=None, zero_is_alone=False):
    over_max = False
    if max_ is not None and d >= max_:
        over_max = True
        d = max_
    start_range = d - d % step
    if zero_is_alone and start_range == 0:
        return "0"
    if over_max:
        return "%d+" % start_range

    end_range = start_range + (step - 1)
    return ("%d..%d" % (start_range, end_range))


def values_to_ranges():
    for agg_key, step, max_range, zero_is_alone in [("days_before_purchase", 10, None, False),
                                     ("levels_completed_before_purchase", 20, 260, False),
                                     ("rate_later_before_ok", 5, None, False),
                                     ("rate_open_before_ok", 10, None, False),
                                     ("pct_of_levels_completed_with_hints", 10, 100, True),
                                     ("pct_of_levels_completed_with_undos", 10, 100, True),
                                     ("pct_of_levels_completed_with_retries", 10, 100, True),
                                     ]:
        dbp = agg[agg_key]
        ignored_keys = ["-", "not enough levels completed", "invalid version"]
        max_value = max([int(a) for a in dbp.keys() if a not in ignored_keys])
        ranges, values = [], []

        for v in range(max_value + 1):
            r = value_to_range(v, step=step, max_=max_range, zero_is_alone=zero_is_alone)
            if r not in ranges:
                ranges.append(r)
                values.append(0)
            values[ranges.index(r)] += dbp.get(str(v), 0)

        csv_writer.writerows([[agg_key], ranges, values, []])


def rate():
    rcs = agg["rate_click_summary"]
    csv_writer.writerows([["Rating: option chosen"],
                          ["None", rcs.get("no_click", 0)],
                          ["Later", rcs.get("later", 0)],
                          ["Later & OK", rcs.get("later_ok", 0)],
                          ["OK", rcs.get("ok", 0)],
                          []])



def retry():
    rpv = agg["retry_per_version"]
    csv_writer.writerows([["Retry per version"],
                          ["version", "yes", "no"],
                          ["1.3", rpv["1.3 yes"], rpv["1.3 no"]],
                          ["1.0", rpv["dev yes"], rpv["dev no"]],
                          []])

tuto()
completed_at_least()
specific_packs_completed()
values_to_ranges()
rate()
retry()
