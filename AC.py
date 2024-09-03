from steplogs import specific_logger
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

    def update_channel_availability(self, ap):
        original = int(ap.channel)
        if self._channels_available[f"{ap.channel}"] == []:
            self.logger.add_new_log(f"AC ASSIGNED {ap._apname} TO CHANNEL {ap.channel}")
            self._channels_available[f"{ap.channel}"].append(ap)
            return
        for x in self._channels_available[f"{ap.channel}"]:
            if self.do_aps_overlap(x, ap):
                result = self.resolve_channel_conflict(ap)
                if not result:
                    self.logger.add_new_log(f"NO CHANNEL AVAILABLE FOR {ap._apname} TO ASSIGN")
                    self.all_ap.remove(ap)
                return
        if int(ap.channel) == original:
            self._channels_available[f"{ap.channel}"].append(ap)
            self.logger.add_new_log(f"AC ASSIGNED {ap._apname} TO CHANNEL {ap.channel}")

    def do_aps_overlap(self, ap1, ap2) -> bool:
        distance = math.sqrt((int(ap1.x) - int(ap2.x)) ** 2 + (int(ap1.y) - int(ap2.y)) ** 2)
        return distance < (int(ap1._coverage_radius) + int(ap2._coverage_radius))

    def resolve_channel_conflict(self, ap):
        for channel in self._preferred_channel:
            if channel != ap.channel and all(not self.do_aps_overlap(ap, other_ap) for other_ap in self._channels_available[channel]):
                ap.channel = channel
                self._channels_available[channel].append(ap)
                self.logger.add_new_log(f"AC REQUIRES {ap._apname} TO CHANGE CHANNEL TO {channel}")
                return
        for channel, ap_list in self._channels_available.items():
            if channel != ap.channel and all(not self.do_aps_overlap(ap, other_ap) for other_ap in ap_list):
                ap.channel = channel
                self._channels_available[channel].append(ap)  # Update the channel list
                self.logger.add_new_log(f"AC REQUIRES {ap._apname} TO CHANGE CHANNEL TO {channel}")
                return

    def evaluate_best_ap(self, client):
        compatible_ap_scores = dict()
        client_wifi_standard = client._standard[4]
        client_support_standard = (client._supports11k, client._supports11v, client._supports11r)
        if self.all_ap is []:
            return "Out Of Range"
        for point in self.all_ap:
            calculated_rssi = point.calculate_rssi(client)
            if calculated_rssi is not None and abs(calculated_rssi) >= client._minimal_rssi and (point._minimal_rssi is None or abs(calculated_rssi) >= float(point._minimal_rssi)):
                compatible_ap_scores[point] = 1
        if not compatible_ap_scores:
            return "Out Of Range"
        for point in compatible_ap_scores.keys():
            if int(point._standard[4:]) > int(client_wifi_standard):
                compatible_ap_scores[point] += 2
            elif int(point._standard[4:]) == int(client_wifi_standard):
                compatible_ap_scores[point] += 1
        highest_score_ap, is_tie = self.find_if_tie(compatible_ap_scores)
        if is_tie is True:
            for ap in highest_score_ap:
                if (ap._supports_11k, ap._supports_11v, ap._supports_11r) == (client_support_standard):
                    compatible_ap_scores[ap] += 1
        highest_score_ap, is_tie = self.find_if_tie(compatible_ap_scores)
        if is_tie is True:
            power = [(0, None)]
            for point in compatible_ap_scores.keys():
                if point._powerlevel > power[0][0]:
                    power = [(point._powerlevel, point)]
                elif point._powerlevel == power:
                    power.append((point._powerlevel, point))
            for power_lev, point in power:
                compatible_ap_scores[point] += 1
        for ap in compatible_ap_scores:
            if len(ap.connecting_clients) >= ap._device_limit:
                del compatible_ap_scores[ap]
        if not compatible_ap_scores:
            return
        for ap in compatible_ap_scores:
            if '6' in ap._frequency:
                compatible_ap_scores[ap] += 2
            elif '5' in ap._frequency and not '6' in ap._frequency:
                compatible_ap_scores[ap] += 1
        for ap in compatible_ap_scores:
            if ap.channel == '11':
                compatible_ap_scores[ap] += 3
            elif ap.channel == '6':
                compatible_ap_scores[ap] += 2
            elif ap.channel == '1':
                compatible_ap_scores[ap] += 1
        for ap in compatible_ap_scores:
            if ap._supports_11r == "true":
                compatible_ap_scores[ap] += 1
        most_compatible_ap, is_tie = self.find_if_tie(compatible_ap_scores)
        least_loaded_ap = None
        if is_tie:
            tracker = 1.0
            for ap in most_compatible_ap:
                load = len(ap.connecting_clients) / ap._device_limit
                if load < tracker:
                    tracker = load
                    least_loaded_ap = ap
        else:
            least_loaded_ap = most_compatible_ap[0]
        return least_loaded_ap

    def find_if_tie(self, ap_dict):
        most_compatible_ap = []
        high_score = 0
        for point, score in ap_dict.items():
            if score > high_score:
                high_score = score
                most_compatible_ap = []
                most_compatible_ap.append(point)
            elif score == high_score:
                most_compatible_ap.append(point)
        return most_compatible_ap, len(most_compatible_ap) > 1

    def __str__(self):
        string_form = (f"\nAP in channel:\n"
                       f"1 : {self._channels_available["1"]}\n"
                       f"2 : {self._channels_available["2"]}\n"
                       f"3 : {self._channels_available["3"]}\n"
                       f"4 : {self._channels_available["4"]}\n"
                       f"5 : {self._channels_available["5"]}\n"
                       f"6 : {self._channels_available["6"]}\n"
                       f"7 : {self._channels_available["7"]}\n"
                       f"8 : {self._channels_available["8"]}\n"
                       f"9 : {self._channels_available["9"]}\n"
                       f"10 : {self._channels_available["10"]}\n"
                       f"11 : {self._channels_available["11"]}\n")

    def __call__(self):
        return self.logger.generate("ac")