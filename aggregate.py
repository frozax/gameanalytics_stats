def count_by_value(res, client_stats, key):
    """group by value of stat value stored in 'key'
    """
    stat = str(client_stats.get(key, "-"))
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
        k, v = func(client_stats)
        if k not in res:
            res[k] = v
        else:
            res[k] += v
    return res


def sound_state(client_stats):
    return client_stats.get("initial_version", "-") + " " + client_stats.get("sound", "-")


def completed_any_pack_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " " + ("yes" if client_stats.get("completed_packs", 0) > 0 else "no")


def retry_yes_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " yes", client_stats.get("retry_yes", 0)


def retry_no_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " no", client_stats.get("retry_no", 0)


def completed_at_least_n_levels(n):
    def completed_at_least(client_stats):
        return "yes" if client_stats.get("completed_levels", 0) >= n else "no"
    return completed_at_least


def pct_completed_with_hints(client_stats):
    if client_stats.get("completed_levels", 0) < 10:
        return None
    hint = client_stats.get("levels_with_hints", 0)
    no_hint = client_stats.get("levels_without_hints", 0)
    return "%0.1f" % (hint / (no_hint + hint))


CONFS = [
    ("tuto_last_event", count_by_value, ("tuto_last_event",)),
    ("days_before_purchase", count_by_value, ("days_before_purchase",)),
    ("levels_completed_before_purchase", count_by_value, ("levels_completed_before_first_purchase",)),
    ("completed_any_pack_per_version", count_by_lambda, (completed_any_pack_per_version,)),
    ("rate_later_before_ok", count_by_value, ("rate_later_before_ok",)),
    ("rate_open_before_ok", count_by_value, ("rate_open_before_ok",)),
    ("rate_ok", count_by_value, ("rate_ok",)),
    ("rate_later", count_by_value, ("rate_later",)),
    ("sound", count_by_lambda, (sound_state,)),
    ("retry_per_version", sum_by_func, ([retry_yes_per_version, retry_no_per_version],)),
    ("pct_of_levels_completed_with_hints", count_by_lambda, (pct_completed_with_hints,)),
]
for l in range(2, 5 + 1):
    CONFS.append(("at_least_%d_levels_completed" % l, count_by_lambda, (completed_at_least_n_levels(l),)))


def aggregate_cd(res, client_stats):
    if res is None:
        res = {"hints": {}}
    for key, func, args in CONFS:
        res[key] = func(res.get(key), client_stats, *args)
    hints = client_stats.get("hints", {})
    if client_stats.get("completed_levels", 0) >= 10:
        for k, v in hints.items():
            if k not in res["hints"]:
                res["hints"][k] = [0, 0]
            res["hints"][k][0 if v else 1] += 1

    return res


def aggregate_second_pass(res):
    for k in res["hints"]:
        hint, no_hint = res["hints"][k]
        res["hints"][k].append(hint / (hint + no_hint))
