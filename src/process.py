#!/usr/bin/env python

import subprocess
import graphyte
import os

def main():
    telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
    telemetry_target_port = os.getenv('TELEMETRY_TARGET_PORT', '2003')

    print(telemetry_target_host)
    print(telemetry_target_port)

    SSID = None
    try:
        SSID = str(subprocess.check_output(["iwgetid", "-r"]).strip(), "utf-8")
    except subprocess.CalledProcessError:
        print("couldn't get SSID")
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    graphyte.init(host=telemetry_target_host, prefix='io.turntabl')
    message = 42
    print('sending message ' + str(message))
    try:
        graphyte.send('foo.bar', message, tags={'SSID': SSID})
    except:
        print('send failed')
        pass

if __name__ == "__main__":
    main()