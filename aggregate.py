def count_by_value(res, client_stats, key):
    """group by value of stat value stored in 'key'
    """
    stat = client_stats.get(key, "-")
    if not res:
        res = {}
    if stat not in res:
        res[stat] = 1
    else:
        res[stat] += 1
    return res

def count_by_lambda(res, client_stats, func):
    """group by value returnedby function
    applied to stats. ignore if None
    """
    key = func.__name__
    client_stats[key] = func(client_stats)
    return count_by_value(res, client_stats, key)


def completed_any_pack_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " " + ("yes" if client_stats.get("completed_packs", 0) > 0 else "no")


def aggregate_cd(res, client_stats):
    if res is None:
        res = {}
    CONFS = [
        ("tuto_last_event", count_by_value, ("tuto_last_event",)),
        ("completed_any_pack_per_version", count_by_lambda, (completed_any_pack_per_version,))
    ]
    for key, func, args in CONFS:
        res[key] = func(res.get(key), client_stats, *args)

    return res
