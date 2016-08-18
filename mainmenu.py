def mainmenu_stats(events):
    r = {}
    r["sound"] = "on_untouched"
    options = ["more_options", "more_games", "twitter", "facebook", "mail"]
    for o in options:
        r[o] = "no"
    for e in reversed(events):
        if e.name[:3] == ["ui", "mainmenu", "sound"]:
            if r["sound"] == "on_untouched":
                r["sound"] = e.name[3]
        elif e.name[:2] == ["ui", "mainmenu"] and e.name[2] in options:
            r[o] = "yes"

    return r