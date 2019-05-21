#!/usr/bin/env python

import subprocess
import graphyte
import os

def main():
    telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
    telemetry_target_port = os.getenv('TELEMETRY_TARGET_PORT', '2003')
    telemetry_prefix = os.getenv('TELEMETRY_PREFIX')

    print('prefix: ' + telemetry_prefix)

    SSID = None
    try:
        SSID = str(subprocess.check_output(["iwgetid", "-r"]).strip(), "utf-8")
    except subprocess.CalledProcessError:
        print("couldn't get SSID")
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    quality, signal_strength = None
    try:
        shell_cmd = 'iwconfig {} | grep Link'.format('wlan0')

        proc = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = proc.communicate()
        msg = output.decode('utf-8').strip()

        # like:
        # Link Quality=41/70  Signal level=-69 dBm  

        quality = msg.split('Signal level=')[1].split('dBm')[0].strip() #hurl
        signal_strength = msg.split('Link Quality=')[1].split('Signal level')[0].strip()
        

    graphyte.init(host=telemetry_target_host, port=telemetry_target_port, prefix=telemetry_prefix)
    graphyte.send('wifi.signal_quality', quality)
    graphyte.send('wifi.signal_strength', signal_strength)
    #graphyte.send('foo.blam', 43, tags={'SSID': SSID})

if __name__ == "__main__":
    main()