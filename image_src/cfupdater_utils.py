from cfupdater import LOCATION, IPV6_WRONG_PREFIXES

import os
import re
from requests import get


def getIPv4():
    try:
        ip = os.popen('{}/get_ipv4.sh'.format(LOCATION)).read().replace("\n", "")
        if ip == "":
            printToLog("Couldn't get external IPv4 via UPnP. Starting Ipifiy API...")
            ip = get('https://api.ipify.org').text
            if ip == "":
                printToLog("Couldn't call Ipifiy API")
                return None
            else: return ip
        else:
            #printToLog("Discovered IPv4: {}".format(ip))
            return ip
    except Exception as e:
        printToLog("Critical error while retrieving external IPv4: {}".format(e))


def getIPv6():
    try:
        ipFull = os.popen("ip -o -f inet6 address show scope global primary -deprecated -mngtmpaddr").read()
        ip = re.search(
            "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",
            ipFull
        )
        if ip == None:
            printToLog("Couldn't get external IPv6 via cmdline. Starting Ipifiy API...")
            ip = get('https://api6.ipify.org').text
            if ip == "":
                printToLog("Couldn't call Ipifiy API")
                return None
            else: return ip
        else: 
            #printToLog("Discovered IPv6: {}".format(ip.group()))
            return ip.group()
    except Exception as e:
        printToLog("Critical error while retrieving external IPv6: {}".format(e))


def printToLog(string):

    from datetime import datetime

    print("{} -- {}".format(datetime.now(), string))
    log = open("{}/logs/cfupdater.log".format(LOCATION), "a")
    log.write("\n{} -- {}".format(datetime.now(), string))
    log.close()