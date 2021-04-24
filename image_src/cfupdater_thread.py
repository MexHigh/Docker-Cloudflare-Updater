import cfupdater as main
import cfupdater_utils as utils

from threading import Thread
from time import sleep


class IPv4Scanner(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.name = "IPv4Scanner"

    def run(self):  # Thread, which checks, when the external IP changes

        utils.printToLog("IPv4Scanner thread started")
        
        ip = None
        oldip = None
        
        while True:

            ip = utils.getIPv4()

            if ip != None and ip != oldip:
                utils.printToLog("IPv4 change detected (Old: {}, New: {})".format(oldip, ip))
                main.updateRecords("A", ip)
                oldip = ip
            
            sleep(60)


class IPv6Scanner(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.name = "IPv6Scanner"

    def run(self):  # Thread, which checks, when the external IP changes

        utils.printToLog("IPv6Scanner thread started")

        ip = None
        oldip = None

        while True:

            ip = utils.getIPv6()

            if ip != None and ip != oldip:
                utils.printToLog("IPv6 change detected (Old: {}, New: {})".format(oldip, ip))
                main.updateRecords("AAAA", ip)
                oldip = ip

            sleep(60)