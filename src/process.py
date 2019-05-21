#!/usr/bin/env python

import subprocess
import graphyte
import os

def main():
    telemetry_target_host = os.getenv('TELEMETRY_TARGET_HOST')
    telemetry_target_port = os.getenv('TELEMETRY_TARGET_PORT', '2003')
    telemetry_prefix = os.getenv('TELEMETRY_PREFIX')

    SSID = None
    try:
        SSID = str(subprocess.check_output(["iwgetid", "-r"]).strip(), "utf-8")
    except subprocess.CalledProcessError:
        print("couldn't get SSID")
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    graphyte.init(host=telemetry_target_host, port=telemetry_target_port prefix=telemetry_prefix)
    graphyte.send('foo.baz', 42)

if __name__ == "__main__":
    main()