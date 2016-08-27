from datetime import datetime


def activity_stats(events):
    latest_data_ts = int(datetime.strptime("2016-08-08", "%Y-%m-%d").timestamp())
    latest_activity_ts = events[-1].timestamp
    r = {}
    r["last_activity_ts"] = latest_activity_ts
    last_activity_days = r["last_activity_days"] = int((latest_data_ts - latest_activity_ts) / 3600 / 24)
    r["active"] = last_activity_days < 5

    return r


def completion_stats(events):
    r = {}

    level_found, pack_found = False, False
    latest_level = None
    r["latest_completed_level"] = r["latest_completed_pack"] = "none"
    r["completed_packs"] = r["completed_levels"] = 0
    r["hints"] = {}
    r["levels_with_hints"] = 0
    r["levels_without_hints"] = 0
    for e in reversed(events):
        if e.level_completed_event():
            # we know if the previously last level didn't use hints if it's not
            # set
            if latest_level and latest_level not in r["hints"]:
                r["hints"][latest_level] = False
                r["levels_without_hints"] += 1
            latest_level = ' '.join(e.name[2:4])
            r["completed_levels"] += 1
            if not level_found:
                r["latest_completed_level"] = latest_level
                level_found = True
        elif e.pack_completed_event():
            r["completed_packs"] += 1
            if not pack_found:
                r["latest_completed_pack"] = e.name[2]
                pack_found = True
        elif e.hint():
            if latest_level and latest_level not in r["hints"]:
                r["hints"][latest_level] = True
                r["levels_with_hints"] += 1

    return r
