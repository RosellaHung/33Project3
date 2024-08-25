import math
class APclass:
    def __init__(self, x, y, channel, powerlevel, frequency, standard, supports_11k, supports_11v,
                supports_11r, coverage_radius, device_limit, minimal_rssi=None):
        self.x = x
        self.y = y
        self.channel = channel
        self.powerlevel = powerlevel
        self.frequency = frequency
        self.standard = standard
        self.supports_11k = supports_11k
        self.supports_11v = supports_11v
        self.supports_11r = supports_11r
        self.coverage_radius = coverage_radius
        self.device_limit = device_limit
        self.minimal_rssi = minimal_rssi
        self.connected_clients = []

    def connect(self):
        pass

    def disconnect(self):
        pass

    def roam(self):
        pass