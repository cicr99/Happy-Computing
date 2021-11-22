from enum import Enum
from typing import List, Optional, Tuple
from clients import Client, Queue

from workers import Seller, SpecialTech, Tech, Worker
from var_gen import poisson, df_inversion
from services import service_price, service_name


class Event(Enum):
    ClientArrival = 0
    WorkerFinished = 1


class Workshop:
    def __init__(self, max_time, sellers_amount, techs_amount, special_techs_amount) -> None:
        self.q: Queue = Queue()
        self.current_time = 0
        # max time in minutes
        self.max_time = max_time
        self.timeline : List[Tuple(Event, float, Optional[Worker])] = [(Event.ClientArrival, self.gen_arrival(), None)]
        self.workers : List[Worker] = self.add_workers(sellers_amount, techs_amount, special_techs_amount)
        self.client_count = 0
        self.profit = 0

    def run(self):
        while len(self.timeline) > 0:
            event, time, w = self.timeline[0]
            self.timeline = self.timeline[1:]

            assert self.current_time <= time, "Time line was not in ascendent order"
            self.current_time = time

            if event == Event.ClientArrival:
                self.client_count += 1
                client = Client(self.gen_service(), self.client_count)
                # print(f"Client {client.idx} arrived requesting for {service_name[client.service]} at {self.current_time}")
                
                # generate new arrival
                t = self.gen_arrival()
                if t + self.current_time < self.max_time:
                    self.add_to_timeline(Event.ClientArrival, t + self.current_time)

                # check whether there is a worker available
                for worker in self.workers:
                    if worker.try_take_client(client):
                        worker.start_work(client)
                        wt = worker.gen_working_time()
                        self.add_to_timeline(Event.WorkerFinished, self.current_time + wt, worker)
                        break
                else:
                    self.q.add_client(client)
                    # print(f"Client{client.idx} was added to the queue")
            elif event == Event.WorkerFinished:
                client = w.finish_work()
                self.profit += service_price[client.service]
                # print(f"Client{client.idx} paid {service_price[client.service]} for service at {self.current_time}. Current profit is {self.profit}.")

                flag, wt = w.try_get_client_from_queue(self.q)
                if flag:
                    self.add_to_timeline(Event.WorkerFinished, self.current_time + wt, w)
        
        # print("Workshop is closed")
        # print(f"Total profit was {self.profit}")
    
    def gen_arrival(self):
        return poisson(20)
    
    def gen_service(self):
        return df_inversion([0.45, 0.25, 0.1, 0.2])

    def add_to_timeline(self, event: Event, time: int, worker: Optional[Worker] = None):
        new_event = (event, time, worker)
        pos = len(self.timeline) - 1 # last element position
        while pos >= 0:
            l_time = self.timeline[pos][1]
            if time >= l_time:
                break
            pos -= 1
        self.timeline.insert(pos + 1, new_event)

    def add_workers(self, sellers_amount, techs_amount, special_techs_amount):
        worker_list = [Seller(i + 1) for i in range(sellers_amount)]
        worker_list.extend([Tech(i + 1) for i in range(techs_amount)])
        worker_list.extend([SpecialTech(i + 1) for i in range(special_techs_amount)])

        return worker_list