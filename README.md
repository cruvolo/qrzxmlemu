# QRZ.com XML interface emulator

This is wrapper code to emulate the http://www.qrz.com/ XML database lookup
feature using a html scraping interface.

## About this emulator

This program uses the [qrmbot](http://github.com/molo1134/qrmbot/) qrz scraping
script.  The script uses your login credentials to authenticate to qrz.com and
scrape HTML output, which requires a regular (free) account, but no XML
subscription.

This emulator works by using a local http server, and intercepting calls to
`xmldata.qrz.com` by modifying the `/etc/hosts` file.

## Tested compatible software

* fldigi 4.1.03 (linux)

## Installation and configuration

As tested on Debian.

### Prerequisites

* `apache2`
* `perl`
* `perl-base`
* `perl-modules`
* `libswitch-perl`
* `liburi-perl`
* `libdate-manip-perl`

### Checkout of git repositories

1. `mkdir -p $HOME/src; cd $HOME/src`
2. `git clone https://github.com/molo1134/qrmbot.git`
3. `git clone https://github.com/cruvolo/qrzxmlemu.git`

### Add credentials to `.qrzlogin` file

4. `cd qrzxmlemu`
5. `echo '$login_callsign="<YOURCALL>";' > .qrzlogin`
6. `echo '$login_password="<YOURPASS>";' >> .qrzlogin`
7. `chmod 600 .qrzlogin`
8. `chown www-data.www-data .qrzlogin`

### Configure apache webserver

Copy the example configuration to `/etc/apache2/sites-available/`, then edit
it there (use an appropriate choice in naming this configuration file):

9. `sudo cp apachesiteconfig.example.conf /etc/apache2/sites-available/002-qrzxml.conf`
10. `sudo vi /etc/apache2/sites-available/002-qrzxml.conf`

On lines 12, 13 and 31 change the path for the `qrzxmlemu` git checkout
directory to match your checkout path.

11. `cd /etc/apache2/sites-enabled/; sudo ln -s ../sites-available/002-qrzxml.conf`
12. Reload the apache configuration: `sudo /etc/init.d/apache2 reload`

### Edit your hosts file to intercept requests to `xmldata.qrz.com`:

13. `sudo bash -c '( echo "127.0.0.1       xmldata.qrz.com" >> /etc/hosts )'`

### Verify output:

```
$ curl 'http://xmldata.qrz.com/xml/current/?s=21529326d6f39f02df51826ec8989b73;callsign=AA7BQ'
<?xml version="1.0" ?>
<QRZDatabase version="1.33">
  <Callsign>
    <call>AA7BQ</call>
    <aliases>AA7BQ/QRP,AA7BQ/R,AA7BQ/M,N6UFT,AA7BQ/DL1,AA7BQ/HR6</aliases>
    <dxcc>291</dxcc>
```

## License

All original code is 2-clause BSD licensed.  See [LICENSE](LICENSE) file.

## Interface specification

This was tested with the v1.33 interface, which is documented here:

https://www.qrz.com/XML/current_spec.html

