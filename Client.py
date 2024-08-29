from steplogs import specific_logger
from AC import ACclass
class Clientclass:
    def __init__(self, steplogger, ac, client_name, x, y, standard, frequency, supports_11k, supports_11v, supports_11r, minimal_rssi):
        self.steplogger = steplogger
        self.ac = ac
        self._client_name = client_name
        self.x = x
        self.y = y
        self._standard = standard
        self._frequency = frequency
        self._supports11k = supports_11k
        self._supports11v = supports_11v
        self._supports11r = supports_11r
        self._minimal_rssi = minimal_rssi
        self.logger = specific_logger(client_name)
        self.connected_ap = None

    def move(self, x_cor, y_cor):
        self.x = x_cor
        self.y = y_cor

    def connect_to_ap(self):
        best_ap = self.ac.evaluate_best_ap(self)
        for ap in best_ap:
            result = ap.connect(self)
            if result[0]:
                self.steplogger.add_new_log(f"CLIENT CONNECT TO {ap._apname} WITH SIGNAL STRENGTH {result[1]}")
                self.logger.add_new_log(f"CLIENT CONNECT TO {ap._apname} WITH SIGNAL STRENGTH {result[1]}")

    def disconnect(self):
        pass


    def roam(self):
        pass

    def __call__(self):
        return self.logger.generate(self._apname)