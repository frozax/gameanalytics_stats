def count_by_value(res, stat):
    """group by value of stat
    """
    if not res:
        res = {}
    if stat not in res:
        res[stat] = 1
    else:
        res[stat] += 1
    return res


def aggregate_cd(res, client_data):
    if res is None:
        res = {}
    CONFS = [("tuto_last_event", count_by_value)]
    for key, func in CONFS:
        res[key] = func(res.get(key), client_data.stats.get(key, "-"))

    return res
