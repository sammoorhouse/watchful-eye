#!/usr/bin/env python

import graphyte
import os
import urllib2
import requests

from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import check_output, Popen, PIPE, CalledProcessError
from xml.etree import ElementTree

telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
telemetry_target_port = int(os.getenv('TELEMETRY_TARGET_PORT', '2003'))
telemetry_prefix = os.getenv('TELEMETRY_PREFIX', 'io.turntabl')

graphyte.init(host=telemetry_target_host, port=telemetry_target_port, prefix=telemetry_prefix)

def publish_wifi_signal_quality():
    try:
        shell_cmd = 'iwconfig {} | grep Link'.format('wlan0')

        proc = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = proc.communicate()
        msg = output.decode('utf-8').strip()

        # like:
        # Link Quality=41/70  Signal level=-69 dBm  

        quality_str = msg.split('Link Quality=')[1].split('/70')[0].strip() #hurl
        quality = int(quality_str)
        
        graphyte.send('wifi.signal_quality', quality)

    except CalledProcessError:
        print("couldn't get signal quality")
        pass

def publish_ping():
    graphyte.send('ping', 1)

def get_ssid():
    try:
        SSID = str(check_output(["iwgetid", "-r"]).strip(), "utf-8")
        return SSID
    except CalledProcessError:
        print("couldn't get SSID")
        pass

def get_default_gateway():
    try:
        shell_cmd = 'ip route | grep default'

        proc = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = proc.communicate()
        msg = output.decode('utf-8').strip()

        # like:
        # default via 192.168.8.1 dev wlan0  metric 600 

        gateway = msg.split('default via ')[1].split(' dev')[0].strip() #hurl
        return gateway

    except CalledProcessError:
        print("couldn't get signal quality")
        pass

def publish_router_statistics():
    gw = get_default_gateway()

    
    resp = requests.get('http://{}/api/monitoring/traffic-statistics').format(gw))
    tree = ElementTree.fromstring(resp.content)

    # like
    # <?xml version="1.0" encoding="UTF-8"?>
    # <response>
    #     <CurrentConnectTime>567</CurrentConnectTime>
    #     <CurrentUpload>8347382</CurrentUpload>
    #     <CurrentDownload>268664986</CurrentDownload>
    #     <CurrentDownloadRate>882061</CurrentDownloadRate>
    #     <CurrentUploadRate>10994</CurrentUploadRate>
    #     <TotalUpload>1118079367</TotalUpload>
    #     <TotalDownload>2190438818</TotalDownload>
    #     <TotalConnectTime>45107</TotalConnectTime>
    #     <showtraffic>1</showtraffic>
    # </response>

    current_upload_bytes = tree.find('CurrentUpload').text
    current_upload_rate = tree.find('CurrentUploadRate').text

    current_download_bytes = tree.find('CurrentDownload').text
    current_download_rate = tree.find('CurrentDownloadRate').text

    graphyte.send('4g.current_upload_bytes', current_upload_bytes)
    graphyte.send('4g.current_upload_rate', current_upload_rate)

    graphyte.send('4g.current_download_bytes', current_download_bytes)
    graphyte.send('4g.current_download_rate', current_download_rate)


def main():

    #graphyte.send('4g.tagged.upload', upload / 1024 / 1024, tags={'SSID': SSID})
    #graphyte.send('4g.tagged.download', download / 1024 / 1024, tags={'SSID': SSID})
     
    SSID = get_ssid()

    sched = BlockingScheduler()
    sched.add_job(publish_wifi_signal_quality, 'interval', minutes=1)
    sched.add_job(publish_router_statistics, 'interval', seconds=10)
    sched.add_job(publish_ping, 'interval', seconds=10)

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()