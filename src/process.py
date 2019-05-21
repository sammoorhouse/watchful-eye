#!/usr/bin/env python

from subprocess import check_output, Popen, PIPE, CalledProcessError
import graphyte
import os

def main():
    telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
    telemetry_target_port = int(os.getenv('TELEMETRY_TARGET_PORT', '2003'))
    telemetry_prefix = os.getenv('TELEMETRY_PREFIX', 'io.turntabl')

    print('prefix: ' + telemetry_prefix)

    SSID = None
    try:
        SSID = str(check_output(["iwgetid", "-r"]).strip(), "utf-8")
    except CalledProcessError:
        print("couldn't get SSID")
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    quality = None
    try:
        shell_cmd = 'iwconfig {} | grep Link'.format('wlan0')

        proc = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = proc.communicate()
        msg = output.decode('utf-8').strip()

        # like:
        # Link Quality=41/70  Signal level=-69 dBm  

        quality_str = msg.split('Link Quality=')[1].split('/70')[0].strip() #hurl
        quality = int(quality_str)

    except CalledProcessError:
        print("couldn't get SSID")
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    graphyte.init(host=telemetry_target_host, port=telemetry_target_port, prefix=telemetry_prefix)
    graphyte.send('wifi.signal_quality', quality)
    #graphyte.send('foo.blam', 43, tags={'SSID': SSID})

if __name__ == "__main__":
    main()