import json
from tutorial import tutorial_stats
from activity import activity_stats, completion_stats
from mainmenu import mainmenu_stats
from purchase import purchase_stats


class InitialPurchase:
    def __init__(self, event_id, event):
        self.event_id = event_id
        self.event = event

    @property
    def item(self):
        return self.event.name[1]

    def __repr__(self):
        return "%s %s %s" % (self.item, self.event_id, self.event)


class Event:
    def __init__(self, name, timestamp, session_num, version):
        self.name = name.split(':')
        self.timestamp = timestamp
        self.session_num = session_num
        self.version = version

    def level_completed_event(self):
        return self.name[0:2] == ["level", "end"]

    def pack_completed_event(self):
        return self.name[0:2] == ["pack", "end"]

    def __repr__(self):
        return "%s %s %s" % (self.name, self.timestamp, self.session_num)


class ClientData:
    def __init__(self, client_id):
        self.id = client_id
        self.events = []
        self.stats = {}

    def __repr__(self):
        return self._gen_dump_string()

    def _gen_dump_string(self, id_=True, stats=True, events=True):
        s = ""
        if id_:
            s += "{id: %s}\n" % (self.id)
        if stats:
            s += "Stats:\n"
            for stat in self.stats:
                s += "  %s: %s\n" % (stat, self.stats[stat])
        if events:
            s += "Events:\n"
            for e in self.events:
                s += "  %s\n" % e
        return s

    def dump(self, id_=True, stats=True, events=True):
        print(self._gen_dump_string(id_, stats, events))

    def add_event(self, event):
        self.events.append(event)

    def compute_stats(self):
        self.initial_purchase = self.find_initial_purchase()
        self.stats.update(tutorial_stats(self.events))
        self.stats.update(activity_stats(self.events))
        self.stats.update(completion_stats(self.events))
        self.stats.update(mainmenu_stats(self.events))
        self.stats.update(purchase_stats(self.initial_purchase, self.events))
        self.stats["initial_version"] = self.events[0].version

    def find_initial_purchase(self):
        for i, e in enumerate(self.events):
            if e.name[0:2] == ["all", "all_packs"]:
                return InitialPurchase(i, e)
            elif e.name[0] == "pack" and e.name[:4] == "pack":
                return InitialPurchase(i, e)
        return None


def client_data_generator(file_with_client_data):
    cur_cd = None
    for line in open(file_with_client_data):
        parsed = json.loads(line)
        client_id, ts, event_str, version, session_num = parsed
        if cur_cd is None or cur_cd.id != client_id:
            if cur_cd:
                yield cur_cd
            cur_cd = ClientData(client_id)
        cur_cd.add_event(Event(event_str, ts, session_num, version))
    if cur_cd:
        yield cur_cd
