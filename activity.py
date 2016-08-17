from datetime import datetime


def activity_stats(events):
    latest_data_ts = int(datetime.strptime("2016-08-08", "%Y-%m-%d").timestamp())
    latest_activity_ts = events[-1].timestamp
    r = {}
    r["last_activity_ts"] = latest_activity_ts
    last_activity_days = r["last_activity_days"] = int((latest_data_ts - latest_activity_ts) / 3600 / 24)
    active = r["active"] = last_activity_days < 5

    return r
