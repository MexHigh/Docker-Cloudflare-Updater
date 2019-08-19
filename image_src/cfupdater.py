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
HOSTS_TO_IGNORE = environ['HOSTS_TO_IGNORE'].replace(' ', '').split(",")
WITH_IPV6 = bool(environ['WITH_IPV6'])
CF_EMAIL = environ['CF_EMAIL']
CF_TOKEN = environ['CF_TOKEN']



def updateARecords(extip):

    utils.printToLog("Starting A record updates with IP address: {}".format(extip))

    from CloudFlare import CloudFlare, exceptions as cf_exceptions

    try:
        cf = CloudFlare(email=CF_EMAIL, token=CF_TOKEN)
        cf_zones = cf.zones.get()

        updateZones = []

        for cf_zone in cf_zones:
            if cf_zone['name'] in ZONES_TO_UPDATE:
                updateZones.append(cf_zone)

        if len(updateZones) == 0: utils.printToLog("Zones to update not found in Cloudflare")

        updatedZones = []

        for zone in updateZones:
            dns_records = cf.zones.dns_records.get(zone['id'])
            for dns_record in dns_records:
                if dns_record['type'] == "A":
                    #print("{}\n\n".format(dns_record))
                    if dns_record['name'] not in HOSTS_TO_IGNORE:
                        dns_record['content'] = extip
                        cf.zones.dns_records.put(zone['id'], dns_record['id'], data=dns_record)
                        updatedZones.append(dns_record['name'])

        utils.printToLog("A record updates successfull")

    except cf_exceptions.CloudFlareAPIError as e:
        utils.printToLog("CloudFlareAPIError in updateARecords(): {}".format(e))


def updateAAAARecords(extip):

    utils.printToLog("Starting AAAA record updates with IP address: {}".format(extip))

    from CloudFlare import CloudFlare, exceptions as cf_exceptions

    try:
        cf = CloudFlare(email=CF_EMAIL, token=CF_TOKEN)
        cf_zones = cf.zones.get()

        updateZones = []

        for cf_zone in cf_zones:
            if cf_zone['name'] in ZONES_TO_UPDATE:
                updateZones.append(cf_zone)

        if len(updateZones) == 0: utils.printToLog("Zones to update not found in Cloudflare")

        updatedZones = []

        for zone in updateZones:
            dns_records = cf.zones.dns_records.get(zone['id'])
            for dns_record in dns_records:
                if dns_record['type'] == "AAAA":
                    #print("{}\n\n".format(dns_record))
                    if dns_record['name'] not in HOSTS_TO_IGNORE:
                        dns_record['content'] = extip
                        cf.zones.dns_records.put(zone['id'], dns_record['id'], data=dns_record)
                        updatedZones.append(dns_record['name'])

        utils.printToLog("AAAA record updates successfull")

    except cf_exceptions.CloudFlareAPIError as e:
        utils.printToLog("CloudFlareAPIError in updateAAAARecords(): {}".format(e))


def main():

    utils.printToLog("Updater started")

    updateARecords(utils.getIPv4())
    thread_ipv4 = threads.IPv4Scanner(1)
    thread_ipv4.start()

    if WITH_IPV6:
        updateAAAARecords(utils.getIPv6())
        thread_ipv6 = threads.IPv6Scanner(2)
        thread_ipv6.start()


if __name__ == '__main__':
    main()
