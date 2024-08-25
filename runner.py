from collections import namedtuple
AP_dict = {"APNAME": "",
            "x": 0,
            "y": 0,
            "channel": 0,
            "powerlevel": 0,
            "frequency": "",
            "standard": "",
            "supports_11k": False,
            "supports_11v": False,
            "supports_11r": False,
            "coverage_radius": 0,
            "device_limit": 0,
            "minimal_rssi": None}
Client_nt = namedtuple("Client",
                       ["CLIENTNAME", "x", "y", "standard", "speed", "supports_11k",
                        "supports_11v", "supports_11r", "minimal_rssi"])
Move_nt = namedtuple("Move", ["CLIENT", "x", "y"])

def run(file: str):
    with open(file, "r") as file:
        content = file.readlines()
        for line in content:
            line_lst = line.strip().split()
            if not line_lst[0] in ("AP", "CLIENT", "MOVE") or not line_lst:
                raise ValueError(f"Invalid line format: {line.strip()}")


if __name__ == "__main__":
    run()