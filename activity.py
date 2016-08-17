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
    for e in reversed(events):
        if not level_found and e.name[0:2] == ["level", "end"]:
            r["latest_completed_level"] = ' '.join(e.name[2:4])
            level_found = True
        elif not pack_found and e.name[0:2] == ["pack", "end"]:
            r["latest_completed_pack"] = e.name[2]
            pack_found = True
        if pack_found and level_found:
            break

    return r
