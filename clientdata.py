import os
import json


class Event:
    def __init__(self, name, timestamp, session_num):
        self.name = name
        self.timestamp = timestamp
        self.session_num = session_num

    def __repr__(self):
        return "{%s %s %s}\n" % (self.name, self.timestamp, self.session_num)


class ClientData:
    def __init__(self, client_id):
        self.id = client_id
        self.events = []

    def __repr__(self):
        s = "{id: %s}\n" % (self.id)
        for e in self.events:
            s += "  %s" % e
        return s

    def add_event(self, event):
        self.events.append(event)


def client_data_generator(file_with_client_data):
    l = []
    cur_cd = None
    for line in open(file_with_client_data):
        parsed = json.loads(line)
        client_id, ts, event, version, session_num = parsed
        if cur_cd is None or cur_cd.id != client_id:
            if cur_cd:
                yield cur_cd
            cur_cd = ClientData(client_id)
        cur_cd.add_event(Event(event, ts, session_num))
    if cur_cd:
        yield cur_cd
