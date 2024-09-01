import math
from steplogs import specific_logger, steplogger
class APclass:
    def __init__(self, steplogger, ac, APNAME, x, y, channel, powerlevel, frequency, standard, supports_11k, supports_11v,
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
            client.connected_ap = self
            self.steplogger.add_new_log(f"{client._client_name} CONNECT LOCATION {client.x} {client.y} {client._standard} {client._frequency} {client._supports11k} {client._supports11v} {client._supports11r}")  # Yet to change
            self.logger.add_new_log(f"{client._client_name} CONNECT LOCATION {client.x} {client.y} {client._standard} {client._frequency} {client._supports11k} {client._supports11v} {client._supports11r}") # Yet to change
            return True, rssi
        return False

    def disconnect(self, client): # when client is out of range
        self.connecting_clients = [c for c in self.connecting_clients if not client]
        self.steplogger.add_new_log(f"{client._client_name} DISCONNECT AT LOCATION {client.x} {client.y}")
        self.logger.add_new_log(f"{client._client_name} DISCONNECT AT LOCATION {client.x} {client.y}")

    def roam(self):
        pass


    def __call__(self, filename):
        return self.logger.generate(filename)