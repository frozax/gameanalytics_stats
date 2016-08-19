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
    r["latest_completed_level"] = r["latest_completed_pack"] = "none"
    r["completed_packs"] = r["completed_levels"] = 0
    for e in reversed(events):
        if e.level_completed_event():
            r["completed_levels"] += 1
            if not level_found:
                r["latest_completed_level"] = ' '.join(e.name[2:4])
                level_found = True
        elif e.pack_completed_event():
            r["completed_packs"] += 1
            if not pack_found:
                r["latest_completed_pack"] = e.name[2]
                pack_found = True

    return r
