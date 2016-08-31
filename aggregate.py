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


def rate_was_oked_at_least_once(client_stats):
    return "yes" if client_stats.get("rate_ok", 0) > 0 else "no"


def rate_was_open_at_least_once(client_stats):
    return "yes" if client_stats.get("rate_open", 0) > 0 else "no"


def completed_any_pack_per_version(client_stats):
    return client_stats.get("initial_version", "-") + " " + ("yes" if client_stats.get("completed_packs", 0) > 0 else "no")


def retry_yes_per_version(client_stats):
    if client_stats.get("completed_levels", 0) < 10:
        return "not enough levels completd", 1
    return client_stats.get("initial_version", "-") + " yes", client_stats.get("retry_yes", 0)


def retry_no_per_version(client_stats):
    if client_stats.get("completed_levels", 0) < 10:
        return "not enough levels completd", 1
    return client_stats.get("initial_version", "-") + " no", client_stats.get("retry_no", 0)


def completed_at_least_n_levels(n, tuto_done):
    def completed_at_least(client_stats):
        client_tuto_done = client_stats.get("tuto_last_event") == "completed/done"
        if tuto_done != client_tuto_done:
            return "not_proper_tuto_done_value"
        if not client_stats.get("started_at_least_one_level", False):
            return "never_tried_playing"
        return "yes" if client_stats.get("completed_levels", 0) >= n else "no"

    return completed_at_least


def pack_completed_active(active):
    def pack_completed(client_stats):
        if active != client_stats.get("active"):
            return "not_active_state"
        return client_stats.get("completed_packs")
    return pack_completed


def pct_completed_with_hints(client_stats):
    if client_stats.get("completed_levels", 0) < 10:
        return "not enough levels completd"
    hint = client_stats.get("levels_with_hints", 0)
    no_hint = client_stats.get("levels_without_hints", 0)
    return "%0.2f" % (hint / (no_hint + hint))


def pct_completed_with_undos(client_stats):
    if client_stats.get("completed_levels", 0) < 10:
        return "not enough levels completd"
    if client_stats.get("initial_version", "-") != "1.3":
        return "invalid version"
    undo = client_stats.get("levels_with_undos", 0)
    no_undo = client_stats.get("levels_without_undos", 0)
    return "%0.2f" % (undo / (no_undo + undo))


def pct_completed_with_retries(client_stats):
    if client_stats.get("completed_levels", 0) < 10:
        return "not enough levels completd"
    undo = client_stats.get("levels_with_retries", 0)
    no_undo = client_stats.get("levels_without_retries", 0)
    return "%0.2f" % (undo / (no_undo + undo))


CONFS = [
    ("tuto_last_event", count_by_value, ("tuto_last_event",)),
    ("days_before_purchase", count_by_value, ("days_before_purchase",)),
    ("levels_completed_before_purchase", count_by_value, ("levels_completed_before_first_purchase",)),
    ("completed_any_pack_per_version", count_by_lambda, (completed_any_pack_per_version,)),
    ("rate_later_before_ok", count_by_value, ("rate_later_before_ok",)),
    ("rate_open_before_ok", count_by_value, ("rate_open_before_ok",)),
    ("rate_ok", count_by_value, ("rate_ok",)),
    ("rate_later", count_by_value, ("rate_later",)),
    ("rate_was_open_at_least_once", count_by_lambda, (rate_was_open_at_least_once,)),
    ("rate_was_oked_at_least_once", count_by_lambda, (rate_was_oked_at_least_once,)),
    ("sound", count_by_lambda, (sound_state,)),
    ("retry_per_version", sum_by_func, ([retry_yes_per_version, retry_no_per_version],)),
    ("pct_of_levels_completed_with_hints", count_by_lambda, (pct_completed_with_hints,)),
    ("pct_of_levels_completed_with_undos", count_by_lambda, (pct_completed_with_undos,)),
    ("pct_of_levels_completed_with_retries", count_by_lambda, (pct_completed_with_retries,)),
]
for l in range(1, 5 + 1):
    for tuto_done in [True, False]:
        CONFS.append(("at_least_%d_levels_completed_tuto_%s" % (l, "done" if tuto_done else "notdone"), count_by_lambda, (completed_at_least_n_levels(l, tuto_done),)))
for ui_elem in ["mail", "facebook", "twitter", "more_games", "infos", "more_options"]:
    CONFS.append(("clicked_on_%s" % ui_elem, count_by_value, (ui_elem,)))
for active in [True, False]:
    CONFS.append(("pack_completed_%s" % ("active" if active else "notactive"), count_by_lambda, (pack_completed_active(active),)))


def aggregate_cd(res, client_stats):
    if res is None:
        res = {"hints": {}, "undos": {}, "retries": {}}
    for key, func, args in CONFS:
        res[key] = func(res.get(key), client_stats, *args)
    if client_stats.get("completed_levels", 0) >= 10:
        for main_key, req_ver in [("hints", None), ("undos", "1.3"), ("retries", None)]:
            if req_ver and client_stats.get("initial_version", "-") != req_ver:
                continue
            dic = client_stats.get(main_key, {})
            for k, v in dic.items():
                if k not in res[main_key]:
                    res[main_key][k] = [0, 0]
                res[main_key][k][0 if v else 1] += 1

    return res


def aggregate_second_pass(res):
    for main_key in ["hints", "undos", "retries"]:
        for k in res[main_key]:
            hint, no_hint = res[main_key][k]
            res[main_key][k].append(hint / (hint + no_hint))
