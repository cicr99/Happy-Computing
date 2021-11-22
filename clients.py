from services import is_change,  is_repair

class Client:
    def __init__(self, service, idx) -> None:
        self.service = service
        self.idx = idx


class Queue:
    def __init__(self) -> None:
        self.repairs = []
        self.changes = []
        self.sells = []

    def add_client(self, client: Client):
        if is_change(client.service):
            self.changes.append(client)
        elif is_repair(client.service):
            self.repairs.append(client)
        else:
            self.sells.append(client)

    def remove_repair(self) -> Client:
        client = self.repairs[0]
        self.repairs = self.repairs[1:]
        return client
    
    def remove_change(self) -> Client:
        client = self.changes[0]
        self.changes = self.changes[1:]
        return client
    
    def remove_sell(self) -> Client:
        client = self.sells[0]
        self.sells = self.sells[1:]
        return client
