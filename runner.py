from AP import APclass
from AC import ACclass
from Client import Clientclass
import pickle
# from steplogs import steplogger
all_ap = []
all_client = []
all_moves = []
ac = ACclass()

def process_lines(line):
    line_lst = line.strip().split()
    if line_lst == []:
        pass
    elif not line_lst[0] in ("AP", "CLIENT", "MOVE"):
        raise ValueError(f"Invalid line format: {line.strip()}")
    elif line_lst[0] == "AP":
        Ap = APclass(ac, *line_lst[1:])
        ac.new_ap(Ap)
        all_ap.append(Ap)
    elif line_lst[0] == "CLIENT":
        Client = Clientclass(ac, *line_lst[1:])
        all_client.append(Client)
    elif line_lst[0] == "MOVE":
        all_moves.append(line_lst[1:])


def simulate(file: str):
    if not type(file) is str:
        raise TypeError(f"File name must be str but given {type(file)}: {file}")
    with open(file, "r") as file:
        for line in file:
            process_lines(line)
        for client in all_client:
            client.connect_to_ap()
        for action in all_moves:
            for c in all_client:
                if c == action[0]:
                    client = c
            client.move(action[1], action[2])


    ac() #delete this
    print(ac.logger)
    for ap in all_ap: #delete this
        ap()#delete this
    for client in all_client:#delete this
        client()#delete this

    # with open("AC_log.bin","rb") as file:
    #     x = pickle.load(file)
    #     for _ in x:
    #         print(_)






if __name__ == "__main__":
    simulate("Sampleinput.txt")
    # rssi = -20
    # minimal_rssi = -30
    # check_availablity = False
    # # if check_availablity and (not rssi == None or (minimal_rssi != None and rssi > minimal_rssi)):
    # if check_availablity and not rssi is None and (minimal_rssi is None or rssi > minimal_rssi):
    #     print('yay')
    # all_ap[0]("ap1")
    # with open("AP1_log.bin", "rb") as binary_file:
    #     loaded_list = pickle.load(binary_file)
    # for x in loaded_list:
    #     print(x)





