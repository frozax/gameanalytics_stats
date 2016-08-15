def tutorial_stats(events):
    r = {}
    tuto_evt = [e for e in events if e.name[0] == "tutorial"]
    for e in reversed(tuto_evt):
        if e.name[-1] == "first":
            r["tuto_last_event"] = '/'.join(e.name[1:-1])
            break

    return r
