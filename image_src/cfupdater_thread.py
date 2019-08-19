import cfupdater as main
import cfupdater_utils as utils

from threading import Thread
from time import sleep



class IPv4Scanner(Thread):

    def __init__(self, threadID):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = "IPv4Scanner"
        self.counter = 1    # Default


    def run(self):  # Thread, which checks, when the external IP changes

        utils.printToLog("IPv4Scanner thread started")

        ip = utils.getIPv4()

        while True:

            oldip = ip
            sleep(60)
            ip = utils.getIPv4()

            if ip != oldip:
                utils.printToLog("IPv4 change detected (Old: {}, New: {}). Starting update...".format(oldip, ip))
                main.updateARecords(ip)


class IPv6Scanner(Thread):

    def __init__(self, threadID):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = "IPv6Scanner"
        self.counter = 1    # Default


    def run(self):  # Thread, which checks, when the external IP changes

        utils.printToLog("IPv6Scanner thread started")

        ip = utils.getIPv6()

        while True:

            oldip = ip
            sleep(60)
            ip = utils.getIPv6()

            if ip != oldip:
                utils.printToLog("IPv6 change detected (Old: {}, New: {}). Starting update...".format(oldip, ip))
                main.updateAAAARecords(ip)