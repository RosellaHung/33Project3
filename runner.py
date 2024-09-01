from AP import APclass
from AC import ACclass
from Client import Clientclass
from steplogs import steplogger
all_ap = dict()
all_client = dict()
all_moves = []
tracker = steplogger()
ac = ACclass(tracker)

def process_lines(line):
    line_lst = line.strip().split()
    if line_lst == []:
        pass
    elif not line_lst[0] in ("AP", "CLIENT", "MOVE"):
        raise ValueError(f"Invalid line format: {line.strip()}")
    elif line_lst[0] == "AP":
        Ap = APclass(tracker, ac, *line_lst[1:])
        ac.new_ap(Ap)
        all_ap[line_lst[1]] = Ap
    elif line_lst[0] == "CLIENT":
        Client = Clientclass(tracker, ac, *line_lst[1:])
        all_client[line_lst[1]] = Client
    elif line_lst[0] == "MOVE":
        all_moves.append(line_lst[1:])


def simulate(file: str):
    if not type(file) is str:
        raise TypeError(f"File name must be str but given {type(file)}: {file}")
    with open(file, "r") as file:
        for line in file:
            process_lines(line)
        for action in all_moves:
            client = all_client[action[1]]
            client.move(action[2], action[3])


    for x in tracker.step_lst:
        print(x) #Right before program ends





if __name__ == "__main__":
    run("Sampleinput.txt")
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





