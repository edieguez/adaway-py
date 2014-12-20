AdAway-py
====

About
----
**AdAway-py** is a [python 3](https://www.python.org) script to **block publicity** using the system host file.
It works only in linux (for now)

How it works?
----
In GNU/Linux distros exist a file in /etc/hosts
(a.k.a. [host file](http://en.wikipedia.org/wiki/Hosts_(file))
that contains domain names associated to an IP.
This is a method to resolve hostnames without using a DNS server.
Adaway-py download files that contains the hostnames of publicity servers and
associate them with an non-existant IP

What advantages does it have?
----
* Can block publicity domains or any other
* You don't need to load ads, so **the navigation speed increases**
* **It doesn't require additional software**
* It **works in all the system**, not only in the web browser

Download
----
You can clone this repository using git
```sh
git clone https://github.com/edieguez/adaway-py.git
```
or
[download](https://github.com/edieguez/adaway-py/archive/master.zip)
it as a zip file

How to use it?
----
Just enter in the script directory and type
```sh
sudo ./main.py
```
![AdAway-py 1](https://cloud.githubusercontent.com/assets/8973425/5060497/06d66564-6d1f-11e4-9823-d06b036eb42f.png)
![AdAway-py 2](https://cloud.githubusercontent.com/assets/8973425/5060496/06d4f94a-6d1f-11e4-928f-38e2a870bfdd.png)

Configuration
----
The configuration file is generated in the first run and it is like this

```json
{
    "blacklist": [
        "http://adaway.org/hosts.txt",
        "http://hosts-file.net/ad_servers.asp",
        "http://winhelp2002.mvps.org/hosts.txt",
        "http://someonewhocares.org/hosts/hosts"
    ],
    "custom_hosts": {
        "localhost": "127.0.0.1",
        "ip6-localnet": "fe00::0",
        "ip6-localhost ip6-loopback": "::1",
        "ip6-allrouters": "ff02::2",
        "ip6-allnodes": "ff02::1",
        "ip6-mcastprefix": "ff00::0"
    },
    "whitelist": [
        "adf.ly",
        "localhost"
    ]
}
```

It contains only three sections
### blacklist
Contains all the source files to block ad domains

### custom_host
A dictionary that allows you to personalize your own hosts

### whitelist
A list of domains that the script won't block even if they are in one of the blacklist files
