#!/usr/bin/env python

from subprocess import check_output, Popen, PIPE, CalledProcessError
import graphyte
import os
import speedtest
from apscheduler.schedulers.blocking import BlockingScheduler

telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
telemetry_target_port = int(os.getenv('TELEMETRY_TARGET_PORT', '2003'))
telemetry_prefix = os.getenv('TELEMETRY_PREFIX', 'io.turntabl')

graphyte.init(host=telemetry_target_host, port=telemetry_target_port, prefix=telemetry_prefix)

def publish_speeds():
    s = speedtest.Speedtest()
    upload = s.upload()
    download = s.download()

    graphyte.send('4g.upload', upload / 1024 / 1024)
    graphyte.send('4g.download', download / 1024 / 1024)

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


def main():

    #graphyte.send('4g.tagged.upload', upload / 1024 / 1024, tags={'SSID': SSID})
    #graphyte.send('4g.tagged.download', download / 1024 / 1024, tags={'SSID': SSID})
     
    SSID = get_ssid()


    sched = BlockingScheduler()
    sched.add_job(publish_speeds, 'interval', minutes=5)
    sched.add_job(publish_wifi_signal_quality, 'interval', minutes=0.5)
    sched.add_job(publish_ping, 'interval', minutes=0.1)

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()