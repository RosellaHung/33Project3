from steplogs import specific_logger
from AC import ACclass
class Clientclass:
    def __init__(self, ac, client_name, x, y, standard, frequency, supports_11k, supports_11v, supports_11r, minimal_rssi):
        self.ac = ac
        self.client = self
        self._client_name = client_name
        self.x = x
        self.y = y
        self._standard = standard
        if len(frequency) > 1:
            self._frequency = frequency.split('/')
        elif len(frequency) == 1:
            self._frequency = [frequency]
        self._supports11k = supports_11k
        self._supports11v = supports_11v
        self._supports11r = supports_11r
        self._minimal_rssi = float(minimal_rssi)
        self.logger = specific_logger(client_name)
        self.connected_ap = None

    def move(self, x_cor, y_cor):
        self.x = x_cor
        self.y = y_cor
        rssi = self.connected_ap.calculate_rssi(self)
        if not self.connected_ap._minimal_rssi is None and (rssi is None or rssi < float(self.connected_ap._minimal_rssi)):
            self.connected_ap.roam_client(self)
        elif rssi is None or rssi < self._minimal_rssi:
            best_ap_result = self.ac.evaluate_best_ap(self)
            if best_ap_result == "Out Of Range" and self.connected_ap is None:
                self.logger.add_new_log("CLIENT REMAINS UNCONNECTED")
                self.ac.logger.add_new_log(f"{self._client_name} REMAINS UNCONNECTED")
            elif best_ap_result == "Out Of Range" and not self.connected_ap is None:
                self.disconnect()
            else:
                self.roam(best_ap_result)


    def connect_to_ap(self):
        best_ap = self.ac.evaluate_best_ap(self.client)
        if best_ap == "Out Of Range" or best_ap is None:
            self.logger.add_new_log("CLIENT FOUND NO AP TO CONNECT")
            self.ac.logger.add_new_log(f"{self._client_name} FOUND NO AP TO CONNECT")
            return
        result = best_ap.connect(self.client)
        if result[0] is True:
            self.connected_ap = best_ap
            self.logger.add_new_log(f"CLIENT CONNECT TO {best_ap._apname} WITH SIGNAL STRENGTH {result[1]:.2f}")
            self.ac.logger.add_new_log(f"{self._client_name} CONNECT TO {best_ap._apname} WITH SIGNAL STRENGTH {result[1]:.2f}")

    def disconnect(self):
        strength = self.connected_ap.calculate_rssi(self)
        self.connected_ap.disconnect(self)
        self.connected_ap = None
        self.logger.add_new_log(f"CLIENT DISCONNECT FROM {self.connected_ap._apname} WITH SIGNAL STRENGTH {strength:.2f}")
        self.ac.logger.add_new_log(f"{self._client_name} DISCONNECT FROM {self.connected_ap._apname} WITH SIGNAL STRENGTH {strength:.2f}")


    def roam(self, ap):
        if ap is None:
            self.logger.add_new_log("CLIENT ROAM DENIED")
            self.ac.logger.add_new_log(f"{self._client_name} ROAM DENIED")
        else:
            self.logger.add_new_log(f"CLIENT ROAM FROM {self.connected_ap} TO {ap._apname}")
            self.ac.logger.add_new_log(f"{self._client_name} ROAM FROM {self.connected_ap._apname} TO {ap._apname}")
            self.connected_ap = ap

    def __call__(self):
        return self.logger.generate(self._client_name)