class Clientclass:
    def __init__(self, x, y, standard, speed, supports_11k, supports_11v, supports_11r, minimal_rssi):
        self.x = x
        self.y = y
        self.standard = standard
        self.speed = speed
        self.supports11k = supports_11k
        self.supports11v = supports_11v
        self.supports11r = supports_11r
        self.minimal_rssi = minimal_rssi

    def move(self, x_cor, y_cor):
        self.x = x_cor
        self.y = y_cor