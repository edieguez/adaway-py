
**AdAway-py** is a [python 3](https://www.python.org) script to **block ads** using the system host file. It works in Linux

## How it works?

In GNU/Linux distros exist a file in /etc/hosts (a.k.a. [host file](http://en.wikipedia.org/wiki/Hosts_(file)) that contains domain names associated to an IP. This applies to Windows too, but the file is in a different location. This is a method to resolve hostnames without using
Adaway-py download files that contains the hostnames of publicity servers and associate them with an non-existant IP

## What advantages does it have?

* Can block publicity domains or any other
* You don't need to load ads, so **the navigation speed increases**
* **It doesn't require additional software**
* It **works in all the system**, not only in the web browser

## Download

* Clone this repository using git

``` shell
git clone https://github.com/edieguez/adaway-py.git
```

* [Download](https://github.com/edieguez/adaway-py/archive/master.zip) it as a zip file
* Download a [compressed version](https://github.com/edieguez/adaway-py/blob/master/adaway.py?raw=true) ***this is the recommended way if you only want to use the script***

## How to use it?

Just enter in the script directory and type

```sh
sudo ./__main__.py
```

you can execute it from the outside folder with

```sh
sudo python adaway-py
```

or if you use the compressed file

```sh
sudo ./adaway.py
```

You can use some flags to do specific actions

``` shell
usage: adaway.py [-h] [-o HOSTS_FILE] [-a | -d | -w host [host ...] | -b host [host ...]]

A python3 script to block ads using the hosts file

options:
  -h, --help          show this help message and exit
  -o HOSTS_FILE       output file
  -a                  apply blocking
  -d                  deactivate blocking
  -w host [host ...]  whitelist one or multiple hosts
  -b host [host ...]  blacklist one or multiple hosts
```

![AdAway-py 1](https://cloud.githubusercontent.com/assets/8973425/5060497/06d66564-6d1f-11e4-9823-d06b036eb42f.png)
![AdAway-py 2](https://cloud.githubusercontent.com/assets/8973425/5060496/06d4f94a-6d1f-11e4-928f-38e2a870bfdd.png)

## Configuration

The configuration file is generated in the first run and it looks like this

```json
{
  "blacklist": [
    "www.nsa.gov",
    "somenastydomain.com"
  ],
  "custom_hosts": {
    "mydomain.com": "127.0.0.1",
    "itanimulli.com": "50.63.202.25"
  },
  "host_files": [
    "http://adaway.org/hosts.txt",
    "http://hosts-file.net/ad_servers.asp",
    "http://winhelp2002.mvps.org/hosts.txt",
    "http://someonewhocares.org/hosts/hosts"
  ],
  "whitelist": [
    "adf.ly",
    "www.linkbucks.com"
  ]
}
```

It contains only four sections

### blacklist

A list of domains that the script will block. It allows you to include hosts that are
not in the hosts files

### custom_host

A dictionary that allows you to personalize your own hosts

### host_files

Contains all the source files to block ad domains

### whitelist

A list of domains that the script won't block even if they are in one of the host files