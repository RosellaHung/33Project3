from steplogs import specific_logger
import math
class ACclass:
    def __init__(self, steplogger):
        self.steplogger = steplogger
        self._preferred_channel = [1,6,11]
        self.all_ap = []
        self._channels_available = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
        self.logger = specific_logger("AC")

    def new_ap(self, ap):
        if ap.channel not in self._channels_available:
            self.resolve_channel_conflict(ap)
        self.all_ap.append(ap)
        self._channels_available.discard(ap.channel)
        self.logger.write_new(f"AP {ap.APNAME} ADDED ON CHANNEL {ap.channel}")

    def update_channel_availability(self, ap):
        # Check if the AP's channel overlaps with any other APs on the same channel
        for existing_ap in self.all_ap:
            if existing_ap != ap and existing_ap.channel == ap.channel:
                if self.do_aps_overlap(ap, existing_ap):
                    self.resolve_channel_conflict(ap, existing_ap)
                    return

    def do_aps_overlap(self, ap1, ap2):
        # Calculate the distance between two APs
        distance = math.sqrt((ap1.x - ap2.x) ** 2 + (ap1.y - ap2.y) ** 2)
        # Check if the distance is less than the sum of their coverage radii
        return distance < (ap1.coverage_radius + ap2.coverage_radius)

    def resolve_channel_conflict(self, ap1, ap2):
        # Attempt to reassign channels to avoid overlap
        for channel in self._preferred_channels:
            if channel != ap1.channel and channel != ap2.channel:
                ap2.channel = channel
                self.logger.write_new(
                    f"AP {ap2.APNAME} CHANGED CHANNEL TO {ap2.channel} DUE TO OVERLAP")
                self._channels_available.discard(channel)  # Mark the channel as used
                return

        # If no preferred channels are available, use any other available channel
        for channel in self._channels_available:
            ap2.channel = channel
            self.logger.write_new(
                f"AP {ap2.APNAME} ASSIGNED TO CHANNEL {ap2.channel} DUE TO OVERLAP")
            self._channels_available.discard(channel)
            return


    def connecting_client(self, client):
        if self.all_ap is []:
            return
        #calculat the rssi of all ap and find the highest rssi and pair it to the ap



    def roam_or_not(self):
        pass

    def __call__(self):
        return self.logger.generate(self._apname)




