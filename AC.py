from steplogs import specific_logger, steplogger
from collections import namedtuple
from AP import APclass
import math
class ACclass:
    def __init__(self, steplogger):
        self.steplogger = steplogger
        self._preferred_channel = ["11", "6", "1"]
        self.all_ap = []
        self._channels_available = {"1": [], "2": [], "3": [], "4": [], "5": [], "6":[],
                                    "7":[], "8":[], "9":[], "10":[], "11":[]}
        self.logger = specific_logger("AC")

    def new_ap(self, ap):
        self.all_ap.append(ap)
        self.update_channel_availability(ap)

    def update_channel_availability(self, ap):
        original = int(ap.channel)
        if self._channels_available[f"{ap.channel}"] == []:
            self._channels_available[f"{ap.channel}"].append(ap)
            return
        for x in self._channels_available[f"{ap.channel}"]:
            if self.do_aps_overlap(x, ap):
                self.resolve_channel_conflict(ap)
        if ap.channel == original:
            self._channels_available[f"{ap.channel}"].append(ap)

    def do_aps_overlap(self, ap1, ap2) -> bool:
        distance = math.sqrt((int(ap1.x) - int(ap2.x)) ** 2 + (int(ap1.y) - int(ap2.y)) ** 2)
        return distance < (int(ap1._coverage_radius) + int(ap2._coverage_radius))

    def resolve_channel_conflict(self, ap):
        for channel in self._preferred_channel:
            if channel != ap.channel and all(not self.do_aps_overlap(ap, other_ap) for other_ap in self._channels_available[channel]):
                ap.channel = channel
                self._channels_available[channel].append(ap)
                self.steplogger.add_new_log(f"AC REQUIRES {ap._apname} TO CHANGE CHANNEL TO {channel}")
                self.logger.add_new_log(f"AC REQUIRES {ap._apname} TO CHANGE CHANNEL TO {channel}")
                return
        for channel, ap_list in self._channels_available.items():
            if channel != ap.channel and all(not self.do_aps_overlap(ap, other_ap) for other_ap in ap_list):
                ap.channel = channel
                self._channels_available[channel].append(ap)  # Update the channel list
                self.steplogger.add_new_log(f"AC REQUIRES {ap._apname} TO CHANGE CHANNEL TO {channel}")
                self.logger.add_new_log(f"AC REQUIRES {ap._apname} TO CHANGE CHANNEL TO {channel}")
                return

    def evaluate_best_ap(self, client):
        compatible_ap_score = {}
        highest_score_ap =[]
        high_score = 0
        client_wifi_standard = client._standard[4]
        if self.all_ap is []:
            return
        for point in self.all_ap:
            calculated_rssi = point.calculate_rssi(client)
            if calculated_rssi is not None and calculated_rssi >= client.minimal_rssi and (point.minimal_rssi is None or calculated_rssi >= point.minimal_rssi):
                compatible_ap_score[point] = 1
        # Prefer APs with higher or more compatible WiFi standards. For this one,
        # they prefer in such order, device with WIFI 6 always prefer AP with WIFI 6 or higher.
        # In tie, device prefer APs with more supported roaming standard.
        # For example if two AP both support WIFI6, but the one AP support close number of roaming standard with the device, the device would choose that one.
        # More detailed example is that client one support 802.11r and 802.11v, one AP support all three standards and the other AP support only 802.11r and 802.11v, the client will prefer the one support only 802.11r and 802.11v.
        #......
        # If there is a tie, prefer AP with more power.
        for point, score in compatible_ap_score.item():
            if point._standard[4] >= client_wifi_standard:
                compatible_ap_score[point] = score + 1
        for point, score in compatible_ap_score.items():
            if score > high_score:
                high_score = score
                highest_score_ap = []
                highest_score_ap.append(point)
            elif score == high_score:
                highest_score_ap.append(point)
        # If tie then comapare roaming standard
        if high_score == 1:
            pass #did not find ap with same or higher wifi standard
        if len(highest_score_ap) > 1:
            pass





    def disconnecting_client(self, client):
        #if out of range
        pass


    def __call__(self):
        return self.logger.generate("ac")



# ap1 = APclass("AP1", 10, 10, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap2 = APclass("AP2", 15, 15, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap3 = APclass("AP3", 200, 60, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap4 = APclass("AP4", 15, 15, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap5 = APclass("AP4", 210, 90, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
#
# ac = ACclass()
# ac.new_ap(ap1)
# ac.new_ap(ap2)
# ac.new_ap(ap3)
# ac.new_ap(ap4)
# ac.new_ap(ap5)
#
# print(ap1.channel)
# print(ap2.channel)
# print(ap3.channel)
# print(ap4.channel)
# print(ap5.channel)
