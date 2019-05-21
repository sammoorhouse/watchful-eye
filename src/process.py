#!/usr/bin/env python

import subprocess
import graphyte
import os

def main():
    telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
    telemetry_target_port = os.getenv('TELEMETRY_TARGET_PORT', '2013')

    telemetry_target = telemetry_target_host + ':' + telemetry_target_port

    print(telemetry_target)

    SSID = None
    try:
        SSID = str(subprocess.check_output(["iwgetid", "-r"]).strip(), "utf-8")
    except subprocess.CalledProcessError:
        print("couldn't get SSID")
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    graphyte.init(telemetry_target, prefix='io.turntabl')
    graphyte.send('foo.bar', 42, tags={'SSID': SSID})

if __name__ == "__main__":
    main()