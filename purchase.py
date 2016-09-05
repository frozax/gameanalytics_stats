def purchase_stats(initial_purchase, events):
    r = {}
    r["paying"] = initial_purchase != None
    if initial_purchase:
        ts_first_purchase = initial_purchase.event.timestamp
        ts_first_run = events[0].timestamp
        r["days_before_purchase"] = int((ts_first_purchase - ts_first_run) / 3600 / 24)
        r["levels_completed_before_first_purchase"] = r["packs_completed_before_first_purchase"] = 0
        for i in range(initial_purchase.event_id):
            e = events[i]
            if e.pack_completed_event():
                r["packs_completed_before_first_purchase"] += 1
            elif e.level_completed_event():
                r["levels_completed_before_first_purchase"] += 1

    return r
