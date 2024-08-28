import math
from steplogs import specific_logger
class APclass:
    def __init__(self, steplogger, APNAME, x, y, channel, powerlevel, frequency, standard, supports_11k, supports_11v,
                supports_11r, coverage_radius, device_limit, minimal_rssi=None):
        self.steplogger = steplogger
        self._apname = APNAME
        self.x = x
        self.y = y
        self.channel = channel
        self._powerlevel = powerlevel
        self._frequency = frequency
        self._standard = standard
        self._supports_11k = supports_11k
        self._supports_11v = supports_11v
        self._supports_11r = supports_11r
        self._coverage_radius = coverage_radius
        self._device_limit = device_limit
        self._minimal_rssi = minimal_rssi
        self.connecting_clients = []
        self.logger = specific_logger(self._apname)

    def calculate_rssi(self, client):
        distance = math.sqrt((self.x - client.x) ** 2 + (self.y - client.y) ** 2)
        if distance > self._coverage_radius:
            return None
        return self._powerlevel - 20 * math.log10(distance) - 20 * math.log10(self._frequency) - 32.44

    def check_availablity(self):
        return len(self.connecting_clients)  < self._device_limit

    def connect(self, client):
        rssi = self.calculate_rssi(client)
        if self.check_availablity() and not rssi is None and (self._minimal_rssi is None or rssi > self._minimal_rssi):
            self.connecting_clients.append(client)
            self.steplogger.step_lst.append(f"CLIENT CONNECT TO {self._apname} WITH SIGNAL STRENGTH 62")
        else:
            self.steplogger.step_lst.append(f"{client.client_name} TRIED {self._apname} BUT WAS DENIED")

    def disconnect(self): # when client is out of range
        pass

    def roam(self):
        pass