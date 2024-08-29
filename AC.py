from steplogs import specific_logger
from AP import APclass
import math
class ACclass:
    def __init__(self):
        self._preferred_channel = ["11", "6", "1"]
        self.all_ap = []
        self._channels_available = {"1": [], "2": [], "3": [], "4": [], "5": [], "6":[],
                                    "7":[], "8":[], "9":[], "10":[], "11":[]}
        self.logger = specific_logger("AC")

    def new_ap(self, ap):
        self.all_ap.append(ap)
        self.update_channel_availability(ap)
        self.logger.add_new_log(f"AP {ap._apname} ADDED ON CHANNEL {ap.channel}")

    def update_channel_availability(self, ap):
        if self._channels_available[f"{ap.channel}"] == []:
            self._channels_available[f"{ap.channel}"].append(ap)
            return
        for x in self._channels_available[f"{ap.channel}"]:
            if self.do_aps_overlap(x, ap):
                self.resolve_channel_conflict(ap)
                return

    def do_aps_overlap(self, ap1, ap2):
        distance = math.sqrt((ap1.x - ap2.x) ** 2 + (ap1.y - ap2.y) ** 2)
        return distance < (ap1._coverage_radius + ap2._coverage_radius)

    def resolve_channel_conflict(self, ap):
        for channel in self._preferred_channel:
            if channel != ap.channel and all(not self.do_aps_overlap(ap, other_ap) for other_ap in
                                             self._channels_available[channel]):
                ap.channel = channel
                self._channels_available[channel].append(ap)
                self.logger.add_new_log(f"AC REQUIRES {ap._apname} TO CHANGE CHANNEL TO {channel}")
                return

                # If no preferred channels are available, find the next available non-overlapping channel
            for channel, ap_list in self._channels_available.items():
                if channel != ap.channel and all(
                        not self.do_aps_overlap(ap, other_ap) for other_ap in ap_list):
                    ap.channel = channel
                    self._channels_available[channel].append(ap)  # Update the channel list
                    self.logger.add_new_log(
                        f"AP {ap._apname} ASSIGNED TO CHANNEL {channel} DUE TO OVERLAP")
                    return

    def connecting_client(self, client):
        if self.all_ap is []:
            return
        #calculat the rssi of all ap and find the highest rssi and pair it to the ap



    def roam_or_not(self):
        pass

    def __call__(self):
        return self.logger.generate("ac")



# ap1 = APclass("AP1", 10, 10, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap2 = APclass("AP2", 15, 15, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap3 = APclass("AP3", 12, 12, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap4 = APclass("AP4", 15, 15, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
# ap5 = APclass("AP4", 100, 90, 6, 20, 2.4/5, "WiFi6", "true", "true", "true", 50, 10, 75)
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
