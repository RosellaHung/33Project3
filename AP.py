import math
from steplogs import specific_logger
class APclass:
    def __init__(self, ac, APNAME, x, y, channel, powerlevel, frequency, standard, supports_11k, supports_11v,
                supports_11r, coverage_radius, device_limit, minimal_rssi=None):
        self.ac = ac
        self._apname = APNAME
        self.x = int(x)
        self.y = int(y)
        self.channel = channel
        self._powerlevel = int(powerlevel)
        if len(frequency) > 1:
            self._frequency = frequency.split('/')
        elif len(frequency) == 1:
            self._frequency = [frequency]
        self._standard = standard
        self._supports_11k = supports_11k
        self._supports_11v = supports_11v
        self._supports_11r = supports_11r
        self._coverage_radius = int(coverage_radius)
        self._device_limit = int(device_limit)
        self._minimal_rssi = minimal_rssi
        self.connecting_clients = []
        self.logger = specific_logger(self._apname)

    def calculate_rssi(self, client):
        result = None
        for cghz in client._frequency:
            for ghz in self._frequency:
                if ghz == cghz:
                    result = float(ghz) * 1000
        distance = math.sqrt((self.x - int(client.x)) ** 2 + (self.y - int(client.y)) ** 2)
        if distance > self._coverage_radius:
            return None
        return self._powerlevel - 20 * math.log10(distance) - 20 * math.log10(result) - 32.44

    def check_availablity(self):
        return len(self.connecting_clients)  < self._device_limit

    def connect(self, client):
        rssi = abs(self.calculate_rssi(client))
        if self.check_availablity() and not rssi is None and (self._minimal_rssi is None or rssi > float(self._minimal_rssi)):
            self.connecting_clients.append(client)
            client.connected_ap = self
            self.logger.add_new_log(f"{client._client_name} CONNECT LOCATION {client.x} {client.y} {client._standard} {"/".join(client._frequency)} {client._supports11k} {client._supports11v} {client._supports11r}") # Yet to change
            self.ac.logger.add_new_log(f"{client._client_name} CONNECT LOCATION {client.x} {client.y} {client._standard} {"/".join(client._frequency)} {client._supports11k} {client._supports11v} {client._supports11r}")  # Yet to change
            return True, rssi
        return False, rssi

    def disconnect(self, client): # when client is out of range
        self.connecting_clients = [c for c in self.connecting_clients if not client]
        self.logger.add_new_log(f"{client._client_name} DISCONNECT AT LOCATION {client.x} {client.y}")
        self.ac.logger.add_new_log(f"{client._client_name} DISCONNECT AT LOCATION {client.x} {client.y}")

    def roam(self):
        pass


    def __call__(self):
        return self.logger.generate(self._apname)