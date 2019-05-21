#!/usr/bin/env python

from subprocess import check_output, Popen, PIPE, CalledProcessError
import graphyte
import os
import speedtest

def get_speeds():
    s = speedtest.Speedtest()
    upload = s.upload()
    download = s.download()
    return upload, download

def get_wifi_signal_quality():
    try:
        shell_cmd = 'iwconfig {} | grep Link'.format('wlan0')

        proc = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = proc.communicate()
        msg = output.decode('utf-8').strip()

        # like:
        # Link Quality=41/70  Signal level=-69 dBm  

        quality_str = msg.split('Link Quality=')[1].split('/70')[0].strip() #hurl
        quality = int(quality_str)
        return quality

    except CalledProcessError:
        print("couldn't get SSID")
        pass

def get_ssid():
    try:
        SSID = str(check_output(["iwgetid", "-r"]).strip(), "utf-8")
        return SSID
    except CalledProcessError:
        print("couldn't get SSID")
        pass


def main():
    telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
    telemetry_target_port = int(os.getenv('TELEMETRY_TARGET_PORT', '2003'))
    telemetry_prefix = os.getenv('TELEMETRY_PREFIX', 'io.turntabl')

    print('prefix: ' + telemetry_prefix)

    SSID = get_ssid()
    wifi_signal_quality = get_wifi_signal_quality()
    upload, download = get_speeds()

    graphyte.init(host=telemetry_target_host, port=telemetry_target_port, prefix=telemetry_prefix)
    graphyte.send('wifi.signal_quality', wifi_signal_quality)
    graphyte.send('4g.upload', upload / 1024 / 1024)
    graphyte.send('4g.download', download / 1024 / 1024)

    graphyte.send('4g.tagged.upload', upload, tags={'SSID': SSID})
    graphyte.send('4g.tagged.download', download, tags={'SSID': SSID})

if __name__ == "__main__":
    main()