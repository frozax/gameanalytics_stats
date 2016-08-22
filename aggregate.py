def count_by_value(res, client_stats, key):
    """group by value of stat value stored in 'key'
    """
    stat = client_stats.get(key, "-")
    if res is None:
        res = {}
    if stat not in res:
        res[stat] = 1
    else:
        res[stat] += 1
    return res

def count_by_lambda(res, client_stats, funcs):
    """group by value returnedby function
    applied to stats. ignore if None
    """
    if not isinstance(funcs, list):
        funcs = [funcs]
    for func in funcs:
        key = func.__name__
        client_stats[key] = func(client_stats)
    return count_by_value(res, client_stats, key)


def sum_by_func(res, client_stats, funcs):
    """sum value returned by funcs
    func must return key, value
    """
    if res is None:
        res = {}
    if not isinstance(funcs, list):
        funcs = [funcs]
    for func in funcs:
        key = func.__name__
        k, v = func(client_stats)
        if k not in res:
            res[k] = v
        else:
            res[k] += v
    return res


def completed_any_pack_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " " + ("yes" if client_stats.get("completed_packs", 0) > 0 else "no")


def retry_yes_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " yes", client_stats.get("retry_yes", 0)


def retry_no_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " no", client_stats.get("retry_no", 0)


def aggregate_cd(res, client_stats):
    if res is None:
        res = {}
    CONFS = [
        ("tuto_last_event", count_by_value, ("tuto_last_event",)),
        ("completed_any_pack_per_version", count_by_lambda, (completed_any_pack_per_version,)),
        ("retry_per_version", sum_by_func, ([retry_yes_per_version, retry_no_per_version],)),
    ]
    for key, func, args in CONFS:
        res[key] = func(res.get(key), client_stats, *args)

    return res
