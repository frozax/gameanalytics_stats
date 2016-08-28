def rate_stats(events):
    r = {}

    names = ["open", "ok", "later"]

    for e in events:
        if len(e.name) > 3 and e.name[2] == "rate":
            if "rate_open" not in r:
                for name in names:
                    r["rate_" + name] = 0
            r["rate_" + e.name[3]] += 1
    if "rate_open" in r:
        r["rate_answered"] = 0
        for name in ["ok", "later"]:
            r["rate_answered"] += r["rate_" + name]
        r["rate_pct_answered"] = r["rate_answered"] / r["rate_open"]

    return r
