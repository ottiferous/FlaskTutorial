#Introduction

## Flaskr + DUO = 2FA your login

## How to use
Assuming you already have Flaskr setup just run ``` python flaskr.py ``` in the main directory of this repository.
Open a browser session to the URL specified by Flask. Make sure that you can reach the cloud servers for Duo Security to allow authentication.

##About
This is being used as a proof of concept for setting up 2FA on a basic web login using Python.

##Configuration files:

This application relies on two configuration files that follow the standard .ini format.

For example:
```
; My App configuration

[app]
skey = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
This will be read through ConfigParser() into a dictionary. The values can be accessed as

    config.get('app','skey')

Which will return the value stored next to the `skey` value that is used to sign the login cookies.

Duo will use another .ini file as follows
```
; Duo integration config

[duo]

ikey = ikey
skey = skey
akey = akey
host = host
```
