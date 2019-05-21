#!/usr/bin/env python

import time
import subprocess
import process


def main():

    while True:
        # Run one process loop
        process.main()

        # Sleep to avoid 100% CPU usage
        time.sleep(5)

# handle reset somewhere
#    subprocess.call(["resin-wifi-connect", "--clear=true"])


if __name__ == "__main__":
    main()