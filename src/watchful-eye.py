#!/usr/bin/env python

import time
import subprocess
import process
import os

def main():

    telemetry_wait_seconds = int(os.getenv('telemetry_wait_seconds', '60'))
    while True:
        process.main()
        time.sleep(telemetry_wait_seconds)

# handle reset somewhere
#    subprocess.call(["resin-wifi-connect", "--clear=true"])


if __name__ == "__main__":
    main()