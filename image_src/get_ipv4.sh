#!/bin/bash
#FRITZBOX_ADDRESS=fritz.box	# In Env File

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
XMLFILE=ipv4.xml
ABS_PATH=@$DIR/$XMLFILE

curl -s "http://$FRITZBOX_ADDRESS:49000/igdupnp/control/WANIPConn1" -H "Content-Type: text/xml; charset="utf-8"" -H "SoapAction:urn:schemas-upnp-org:service:WANIPConnection:1#GetExternalIPAddress" \
-d "$ABS_PATH" | grep -Eo "\<[[:digit:]]{1,3}(\.[[:digit:]]{1,3}){3}\>"
