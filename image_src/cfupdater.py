'''
Created on Jun 19, 2019

@author: Leon Schmidt
'''


from threading import Thread
from os import path
from os import environ


# ENVVARS
LOCATION = path.dirname(path.abspath(__file__))
ZONES_TO_UPDATE = environ['ZONES_TO_UPDATE']
HOSTS_TO_IGNORE = environ['HOSTS_TO_IGNORE']
CF_EMAIL = environ['CF_EMAIL']
CF_TOKEN = environ['CF_TOKEN']



class IPScanner(Thread):

    def __init__(self, threadID):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = "IPScanner"
        self.counter = 1    # Default


    def run(self):  # Deamon, welcher checkt, wann sich die IP ändert

        printToLog("IPScanner Thread gestartet")
        from time import sleep

        ip = getIP()

        while True:

            oldip = ip
            sleep(60)
            ip = getIP()

            if ip != oldip:
                printToLog("Ungleiche IPs erkannt (Alt: {}, Neu: {}). Update wird gestartet".format(oldip, ip))
                updateARecords(ip)


def getIP():

    try:
        import os
        from requests import get

        ip = os.popen('{}/get_ipv4.sh'.format(LOCATION)).read().replace("\n", "")
        if ip == "":
            printToLog("Konnte externe IP nicht via UPnP anfragen. Starte Ipifiy API...")
            ip = get('https://api.ipify.org').text
            if ip == "":
                printToLog("Konnte Ipifiy API nicht ansprechen")
                return None
            else: return ip
        else:
            #printToLog("Discovered IPv4: {}".format(ip))
            return ip
    except Exception as e:
        printToLog("Kritischer Fehler beim Abfragen der externen IP: {}".format(e))
    except:
        printToLog("Kritischer Fehler beim Abfragen der externen IP. Fehlertyp konnte nicht festgestellt werden.")



def printToLog(string):

    from datetime import datetime

    print("{} -- {}".format(datetime.now(), string))
    log = open("{}/logs/cfupdater.log".format(LOCATION), "a")
    log.write("\n{} -- {}".format(datetime.now(), string))
    log.close()


def updateARecords(extip):

    printToLog("Starte A Record Updates mit IP Adresse: {}".format(extip))

    from CloudFlare import CloudFlare, exceptions as cf_exceptions

    try:
        cf = CloudFlare(email=CF_EMAIL, token=CF_TOKEN)
        cf_zones = cf.zones.get()

        updateZones = []

        for cf_zone in cf_zones:
            if cf_zone['name'] in ZONES_TO_UPDATE:
                updateZones.append(cf_zone)

        if len(updateZones) == 0: printToLog("Zonen, welche geupdated werden sollen, wurden nicht gefunden")

        for zone in updateZones:
            dns_records = cf.zones.dns_records.get(zone['id'])
            for dns_record in dns_records:
                if dns_record['type'] == "A":
                    #print("{}\n\n".format(dns_record))
                    if dns_record['name'] not in HOSTS_TO_IGNORE:
                        dns_record['content'] = extip
                        result = cf.zones.dns_records.put(zone['id'], dns_record['id'], data=dns_record)
                        #print(result)

        printToLog("A Record Updates erfolgreich ausgeführt")

    except cf_exceptions.CloudFlareAPIError as e:
        printToLog("CloudFlareAPIError in updateARecords(): {}".format(e))


def main():

    printToLog("Programm gestartet")

    # Initial Update
    updateARecords(getIP())

    thread = IPScanner(1)
    thread.start()


if __name__ == '__main__':
    main()
