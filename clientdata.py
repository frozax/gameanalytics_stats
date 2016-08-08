import os

class ClientData:
    def raw(self):
        return "cd"


def client_data_generator(file_with_client_data):
    for line in open(file_with_client_data):
        yield ClientData()
