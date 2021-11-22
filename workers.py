from enum import Enum
from typing import Optional

from clients import Client, Queue
from var_gen import normal, exponential
from services  import is_change, is_repair, needs_tech


class Status(Enum):
    Free = 0
    Busy = 1


class Worker:
    def __init__(self, name) -> None:
        self.status = Status.Free
        self.client: Optional[Client] = None
        self.name = name

    def gen_working_time(self):
        pass

    def start_work(self, client: Client):
        self.status = Status.Busy
        self.client = client
        # print(f"{self.name} started working on client {self.client.idx}")
        
    def finish_work(self) -> Client:
        self.status = Status.Free
        # print(f"{self.name} finished working on client {self.client.idx}")
        client = self.client
        self.client = None
        return client

    def try_get_client_from_queue(self, q: Queue):
        pass

    def try_take_client(self, client: Client):
        return self.status == Status.Free


class Seller(Worker):
    def __init__(self, name) -> None:
        super().__init__(f"Seller{name}")

    def gen_working_time(self):
        return normal(5, 2)

    def try_get_client_from_queue(self, q: Queue):
        if len(q.sells) == 0:
            # There are no clients in queue
            return False, 0

        self.start_work(q.remove_sell())
        return True, self.gen_working_time()

    def try_take_client(self, client: Client):
        if super().try_take_client(client):
            return not needs_tech(client.service)
        
        return False


class Tech(Worker):
    def __init__(self, name) -> None:
        super().__init__(f"Tech{name}")

    def gen_working_time(self):
        return exponential(20)

    def try_get_client_from_queue(self, q: Queue):
        if len(q.repairs) == 0:
            # There are no clients in queue
            return False, 0

        self.start_work(q.remove_repair())
        return True, self.gen_working_time()

    def try_take_client(self, client: Client):
        if super().try_take_client(client):
            return is_repair(client.service)

        return False

    
class SpecialTech(Worker):
    def __init__(self, name) -> None:
        super().__init__(f"Special{name}")

    def gen_working_time(self):
        return exponential(15)

    def try_get_client_from_queue(self, q: Queue):
        if len(q.changes) == 0:
            # There are no clients waiting for changes so the tech can do repairs
            if len(q.repairs) == 0:
                # There are no clients in queue
                return False, 0

            self.start_work(q.remove_repair())
            return True, super().gen_working_time()
        
        self.start_work(q.remove_change())
        return True, self.gen_working_time()
        
    def try_take_client(self, client: Client):
        if self.status == Status.Busy:
            return False

        return needs_tech(client.service)