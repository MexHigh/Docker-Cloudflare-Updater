'''
Created on Jun 19, 2019

@author: Leon Schmidt
'''


import cfupdater_utils as utils
import cfupdater_thread as threads

from os import path, environ



# ENVVARS
LOCATION = path.dirname(path.abspath(__file__))
ZONES_TO_UPDATE = environ['ZONES_TO_UPDATE'].replace(' ', '').split(",")
HOSTS_TO_UPDATE = environ['HOSTS_TO_UPDATE'].replace(' ', '').split(",")
HOSTS_TO_IGNORE = environ['HOSTS_TO_IGNORE'].replace(' ', '').split(",")
WITH_IPV6 = bool(environ['WITH_IPV6'])
IPV6_WRONG_PREFIXES = ["fc", "fd", "fe"]
CF_EMAIL = environ['CF_EMAIL']
CF_TOKEN = environ['CF_TOKEN']



def updateRecords(recType, extip):

    utils.printToLog("Starting {} record updates with IP address: {}".format(recType, extip))

    from CloudFlare import CloudFlare, exceptions as cf_exceptions

    try:
        cf = CloudFlare(email=CF_EMAIL, token=CF_TOKEN)
        cf_zones = cf.zones.get()

        updateZones = []

        for cf_zone in cf_zones:
            if cf_zone['name'] in ZONES_TO_UPDATE:
                updateZones.append(cf_zone)

        if len(updateZones) == 0:
            utils.printToLog("Zones to update not found in Cloudflare")
            return

        updatedZones = []

        for zone in updateZones:
            dns_records = cf.zones.dns_records.get(zone['id'])
            for dns_record in dns_records:
                if dns_record['type'] == recType:
                    #print("{}\n\n".format(dns_record))
                    if dns_record['name'] in HOSTS_TO_UPDATE:
                        dns_record['content'] = extip
                        cf.zones.dns_records.put(zone['id'], dns_record['id'], data=dns_record)
                        #print("Updated " + dns_record['name'])
                        updatedZones.append(dns_record['name'])

        utils.printToLog("{} record updates successfull".format(recType))

    except cf_exceptions.CloudFlareAPIError as e:
        utils.printToLog("CloudFlareAPIError in updateARecords(): {}".format(e))


def main():

    utils.printToLog("Updater started")

    updateRecords("A", utils.getIPv4())
    thread_ipv4 = threads.IPv4Scanner(1)
    thread_ipv4.start()

    if WITH_IPV6:
        updateRecords("AAAA", utils.getIPv6())
        thread_ipv6 = threads.IPv6Scanner(2)
        thread_ipv6.start()


if __name__ == '__main__':
    main()
