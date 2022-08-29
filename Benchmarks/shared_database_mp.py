import sys
from multiprocessing import Process, Pipe, Manager, Lock
from time import sleep
from random import randint
from itertools import combinations

"""Class WorkingProcess - represents processes that will access the database"""
class WorkingProcess:
    def __init__(self, p_id: int, no_processes: int):
        self.p_id = p_id
        self.loc_clock = randint(0, no_processes)
        self.p_pipes = []
        self.postponed_processes = []

    """Create a message to send to other processes"""
    def create_msg(self, msg_type: int):
        return "{0},{1},{2}".format(self.p_id, self.loc_clock, msg_type)

    """Unpack message received from other processes in form of string to list of values"""
    def unpack_msg(self, msg: str):
        response = msg.split(',')
        return [int(elem) for elem in response]

    """Process main logic - Ricart-Agrawala algorithm for mutual exclusion"""
    def access_data(self, no_processes: int, shared_memory: dict, lock: Lock):
        # sleep(randint(100, 2001) * 0.001)
        for _ in range(5):
            T_i = self.loc_clock

            for pipe in self.p_pipes:
                msg = self.create_msg(0)
                pipe.send(msg)

            no_received_responses = 0
            while no_received_responses < no_processes - 1:

                for pipe in self.p_pipes:
                    while True:
                        msg = pipe.recv()
                        if msg is not None:
                            break

                    response = self.unpack_msg(msg)
                    self.loc_clock = max(self.loc_clock, response[1]) + 1

                    if response[2] == 1:
                        no_received_responses += 1
                    else:
                        if (response[1] >= T_i) and (response[0] > self.p_id):
                            self.postponed_processes.append(self.p_pipes.index(pipe))
                        else:
                            msg = self.create_msg(1)
                            pipe.send(msg)

            lock.acquire()
            #print("Process {} is accessing the database.".format(self.p_id))

            helper = shared_memory[self.p_id]
            helper[0] = self.loc_clock
            helper[1] += 1
            shared_memory[self.p_id] = helper

            for i in range(no_processes):
                continue
                #print("Data for process {0}: local_clock = {1}, entries = {2} ".format(i, shared_memory[i][0],
                #                                                                       shared_memory[i][1]))

            #print("Process {} is leaving the database.".format(self.p_id))
            sleep(randint(100, 2001) * 0.001)
            lock.release()

            if len(self.postponed_processes) != 0:
                for proc in self.postponed_processes:
                    msg = self.create_msg(1)
                    self.p_pipes[proc].send(msg)
                self.postponed_processes = []

            sleep(randint(100, 2001) * 0.001)


"""Class Database - represents the shared database and holds the main script execution flow"""
class Database:
    def __init__(self, no_processes: int):
        self.no_processes = no_processes
        self.all_pipes = []

    """Creating unique pairs of processes and connecting each pair with a pipe"""
    def connect_processes(self, processes: list):
        for pair in combinations(processes, 2):
            fst_pipe, snd_pipe = Pipe()
            processes[pair[0].p_id].p_pipes.append(fst_pipe)
            processes[pair[1].p_id].p_pipes.append(snd_pipe)
            self.all_pipes.extend([fst_pipe, snd_pipe])

    """Starting the processes and enabling database access"""
    def start_data_access(self, processes: list, shared_memory: dict):
        self.connect_processes(processes)
        lock = Lock()
        started = []
        for i, proc in enumerate(processes):
            p = Process(target=proc.access_data,
                        args=(self.no_processes, shared_memory, lock),
                        name="Process {}".format(i),
                        daemon=True
                        )
            started.append(p)
            p.start()

        for proc in started:
            proc.join()

        for pip in self.all_pipes:
            pip.close()

        print("\nAll processes finished the database access.")


"""Initialization of shared database"""
def initialize_database(processes: list, shared_memory: dict):
    for proc in processes:
        shared_memory[proc.p_id] = [proc.loc_clock, 0]


"""Script main logic execution start"""
def start_exchange(no_processes: int):

    database_controller = Database(no_processes)
    manager = Manager()
    shared_memory = manager.dict()

    working_processes = []
    for i in range(no_processes):
        working_processes.append(WorkingProcess(i, no_processes))

    initialize_database(working_processes, shared_memory)

    database_controller.start_data_access(working_processes, shared_memory)


"""Script entry point"""
if __name__ == '__main__':
    no_processes = int(sys.argv[1])
    # start_exchange(no_processes)
    for i in range(20):
        start_exchange(no_processes)