# Watchful Eye

Monitors some wifi health metrics and boshes them into graphite, ready for visualisation in a grafana you've got hosted somewhere.

I've got it running on a handful of [balena](https://balena.io)-bound raspberry pis.

![Watchful Eye](/img/watchful-eye.png)

## Monitor setup

Create a balena account, create a new application, install the OS on a raspberry pi.

Set the following vars in your app's config:

```TELEMETRY_TARGET_HOST```
```TELEMETRY_TARGET_PORT```
```TELEMETRY_PREFIX```

When you first power the pi up, you'll need to connect via ethernet so its onboard balena OS can grab your (ahem) package.

Watchful-eye is built with the *brilliant* [wifi-connect](https://github.com/balena-io/wifi-connect) so you should then power it up *without* ethernet, log on to the wireless network called "wifi-connect" and then pass in your wifi network's login credentials. The pi will use these from now on!

## Grafana setup

On your ```TELEMETRY_TARGET``` box, run something like the following docker-compose.yml:

```
    root@localhost:~/grafana# cat docker-compose.yml
    version: "3"
    services:
    grafana:
        image: grafana/grafana
        container_name: grafana
        restart: always
        ports:
        - 3000:3000
        networks:
        - grafana-net
        volumes:
        - grafana-volume

    graphite:
        image: graphiteapp/graphite-statsd
        container_name: graphite
        restart: always
        ports:
        - 80:80
        - 2003-2004:2003-2004
        - 2023-2024:2023-2024
        - 8125:8125/udp
        - 8126:8126
        networks:
        - grafana-net

    networks:
    grafana-net:

    volumes:
    grafana-volume:
        external: true
```

You should then be able to log onto grafana at your-host:3000. Add the graphite data source which will be sitting on http://graphite:8080. You should then be able to graph [TELEMETRY_PREFIX].wifi.signal_quality, .4g.upload, .4g.download

## Comments
keep 'em to yourself.

I kid, I kid! sam@globalcode.org.uk