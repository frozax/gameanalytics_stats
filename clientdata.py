import os
import json

class ClientData:
    def __init__(self, client_id):
        self.id = client_id

    def raw(self):
        return "{id: %s}" % (self.id)


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
    if cur_cd:
        yield cur_cd
