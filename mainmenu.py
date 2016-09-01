def mainmenu_stats(events):
    r = {}
    r["sound"] = "on_untouched"
    options = ["more_options", "more_games", "twitter", "facebook", "mail", "infos"]
    for o in options:
        r[o] = "no"
    for e in reversed(events):
        if e.name[0] == "ui" and e.name[2] == "sound":
            if r["sound"] == "on_untouched":
                r["sound"] = e.name[3] + " " + e.name[1]
                r["sound_version_latest_event"] = e.version
        elif e.name[:2] == ["ui", "mainmenu"] and e.name[2] in options:
            r[e.name[2]] = "yes"

    return r


def ingamemenu_stats(events):
    r = {}

    for e in events:
        if e.name[:3] == ["ui", "game", "retry"]:
            if e.name[3] != "ask":
                if "retry_yes" not in r:
                    r["retry_yes"] = r["retry_no"] = 0
                r["retry_" + e.name[3]] += 1

    return r
