from AP import APclass
from AC import ACclass
from Client import Clientclass
all_ap = dict()
all_client = dict()
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
        all_ap[line_lst[1]] = Ap
    elif line_lst[0] == "CLIENT":
        Client = Clientclass(ac, *line_lst[1:])
        all_client[line_lst[1]]= Client
    elif line_lst[0] == "MOVE":
        all_moves.append(line_lst[1:])


def simulate(file: str):
    if not type(file) is str:
        raise TypeError(f"File name must be str but given {type(file)}: {file}")
    with open(file, "r") as file:
        for line in file:
            process_lines(line)
        for client_name, client_obj in all_client.items():
            client_obj.connect_to_ap()
        for action in all_moves:
            client_obj = all_client[action[0]]
            client_obj.move(action[1], action[2])
    print(ac.logger)
    for x,y in all_ap.items():
        print(y)





if __name__ == "__main__":
    simulate("Sampleinput.txt")
    # with open("AP1_log.bin", "rb") as binary_file:
    #     loaded_list = pickle.load(binary_file)
    # for x in loaded_list:
    #     print(x)





