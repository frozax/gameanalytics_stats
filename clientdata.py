import json
from tutorial import tutorial_stats
from activity import activity_stats, completion_stats


class Event:
    def __init__(self, name, timestamp, session_num, version):
        self.name = name.split(':')
        self.timestamp = timestamp
        self.session_num = session_num
        self.version = version

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
        self.stats.update(tutorial_stats(self.events))
        self.stats.update(activity_stats(self.events))
        self.stats.update(completion_stats(self.events))
        self.stats["initial_version"] = self.events[0].version


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
