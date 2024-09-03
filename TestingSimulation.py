import unittest
from AC import ACclass
from AP import APclass
from Client import Clientclass
class TestSimulationProgram(unittest.TestCase):
    def setUp(self):
        self.ac = ACclass()
        self.ap1 = APclass(self.ac, "AP1", "0", "20", "11", "20", "2.4/5", "WiFi7", "true", "true",
                      "true", "15", "10")
        self.ap2 = APclass(self.ac, "AP2", "25", "41", "2", "30", "6", "WiFi6", "false", "true",
                      "true", "15", "20", "80")
        self.ap3 = APclass(self.ac, "AP3", "200", "60", "6", "21", "2.4/5", "WiFi6", "true", "true",
                      "true", "52", "32", "75")
        self.ap4 = APclass(self.ac, "AP4", "110", "10", "6", "27", "2.4/5", "WiFi6", "true", "true",
                      "true", "90", "10")
        self.ac.new_ap(self.ap1)
        self.ac.new_ap(self.ap2)
        self.ac.new_ap(self.ap3)
        self.ac.new_ap(self.ap4)


    def test_assign_channel_wo_conflicts(self):
        self.assertEqual(self.ap1.channel, "11")
        self.assertEqual(self.ap2.channel, "2")
        self.assertEqual(self.ap3.channel, "6")
        # self.assertEqual(self.ap4.channel, "6")

    def test_assign_channel_with_conflicts(self):
        ac_test = ACclass()
        ap1 = APclass(ac_test, "AP1", "0", "20", "11", "20", "2.4/5", "WiFi7", "true", "true",
                      "true", "30", "10")
        ap2 = APclass(ac_test, "AP2", "25", "41", "11", "30", "6", "WiFi6", "false", "true",
                      "true", "20", "20", "80")
        ap3 = APclass(ac_test, "AP3", "200", "60", "11", "19", "2.4/5", "WiFi6", "true", "true",
                      "false", "200", "32", "75")
        ap4 = APclass(ac_test, "AP4", "110", "10", "11", "20", "2.4/5", "WiFi8", "true", "true",
                      "true", "70", "10")
        ap5 = APclass(ac_test, "AP5", "34", "92", "11", "20", "2.4/5", "WiFi8", "true",
                      "true",
                      "true", "200", "10")
        ac_test.new_ap(ap1)
        ac_test.new_ap(ap2)
        ac_test.new_ap(ap3)
        ac_test.new_ap(ap4)
        ac_test.new_ap(ap5)
        self.assertEqual(ap1.channel, "11")
        self.assertEqual(ap2.channel, "6")
        self.assertEqual(ap3.channel, "1")
        self.assertEqual(ap4.channel, "11")
        self.assertEqual(ap5.channel, "2")

    def test_connecting_client_to_ap(self):
        line_lst = ["Client1", "10", "10", "WiFi6", "2.4/5", "true", "true", "true", "73"]
        Client1 = Clientclass(self.ac, *line_lst)
        Client1.connect_to_ap()
        client_logs = Client1.logger.step_lst
        self.assertEqual(Client1.connected_ap._apname, "AP1")
        self.assertEqual("Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH" in client_logs[0], True)

    def test_decide_not_to_roam(self):
        line_lst = ["Client1", "10", "10", "WiFi6", "2.4/5", "true", "true", "true", "73"]
        Client1 = Clientclass(self.ac, *line_lst)
        Client1.connect_to_ap()
        Client1.move(14, 19)
        self.assertEqual(Client1.connected_ap._apname, "AP1")

    def test_decide_to_roam(self):
        line_lst = ["Client1", "10", "10", "WiFi6", "2.4/5", "true", "true", "true", "73"]
        Client1 = Clientclass(self.ac, *line_lst)
        Client1.connect_to_ap()
        Client1.move(150, 72)
        self.assertEqual(Client1.connected_ap._apname, "AP4")








if __name__ == "__main__":
    unittest.main()
