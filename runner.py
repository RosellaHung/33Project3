from collections import namedtuple
from AP import APclass
# AP_dict = {"APNAME": "",
# #             "x": 0,
# #             "y": 0,
# #             "channel": 0,
# #             "powerlevel": 0,
# #             "frequency": "",
# #             "standard": "",
# #             "supports_11k": False,
# #             "supports_11v": False,
# #             "supports_11r": False,
# #             "coverage_radius": 0,
# #             "device_limit": 0,
# #             "minimal_rssi": None}
# # Client_nt = namedtuple("Client",
# #                        ["CLIENTNAME", "x", "y", "standard", "speed", "supports_11k",
# #                         "supports_11v", "supports_11r", "minimal_rssi"])
# # Move_nt = namedtuple("Move", ["CLIENT", "x", "y"])

def run(file: str):
    with open(file, "r") as file:
        content = file.readlines()
        for line in content:
            # line_lst = line.strip().split()
            # print(line_lst)
            # if line_lst == []:
            #     pass
            # elif not line_lst[0] in ("AP", "CLIENT", "MOVE"):
            #     raise ValueError(f"Invalid line format: {line.strip()}")
            process_lines(line)

def process_lines(line):
    line_lst = line.strip().split()
    if line_lst == []:
        pass
    elif not line_lst[0] in ("AP", "CLIENT", "MOVE"):
        raise ValueError(f"Invalid line format: {line.strip()}")



if __name__ == "__main__":
    run("Sampleinput.txt")