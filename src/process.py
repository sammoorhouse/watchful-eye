#!/usr/bin/env python

import subprocess


def main():
    print("hello, world!")

    SSID = None
    try:
        SSID = subprocess.check_output(["iwgetid", "-r"]).strip()
    except subprocess.CalledProcessError:
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    print("SSID: " + SSID)

if __name__ == "__main__":
    main()