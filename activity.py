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
    r["undos"] = {}
    r["retries"] = {}
    for e in reversed(events):
        if e.level_completed_event():
            # we know if the previously last level didn't use hints if it's not
            # set
            if latest_level:
                if latest_level not in r["undos"]:
                    r["undos"][latest_level] = False
                if latest_level not in r["hints"]:
                    r["hints"][latest_level] = False
                if latest_level not in r["retries"]:
                    r["retries"][latest_level] = False
            latest_level = e.name[2] + " %02d" % int(e.name[3])
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
            if latest_level:
                r["hints"][latest_level] = True
        elif e.undo():
            if latest_level:
                r["undos"][latest_level] = True
        elif e.retry_confirm():
            if latest_level:
                r["retries"][latest_level] = True

    r["levels_with_hints"] = len([a for a in r["hints"].keys() if r["hints"][a]])
    r["levels_without_hints"] = len([a for a in r["hints"].keys() if not r["hints"][a]])
    r["levels_with_undos"] = len([a for a in r["undos"].keys() if r["undos"][a]])
    r["levels_without_undos"] = len([a for a in r["undos"].keys() if not r["undos"][a]])
    r["levels_with_retries"] = len([a for a in r["retries"].keys() if r["retries"][a]])
    r["levels_without_retries"] = len([a for a in r["retries"].keys() if not r["retries"][a]])

    return r
