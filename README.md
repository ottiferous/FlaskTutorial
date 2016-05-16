#Introduction

## Flaskr + DUO = 2FA your login

## How to use
Assuming you already have Flaskr setup just run ``` python flaskr.py ``` in the main directory of this repository.
The application can be reached locally by navigating to the URL specified once Flask has been started.


##Configuration files:

This application relies on two configuration files that follow the standard .ini format.

For example:
```
    ; My App configuration

    [app]
    skey = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
This will be read through ConfigParser() into a dictionary. The values can be access as

    `config.get('app','skey')`

Which will return the value stored next to the skey value that is used to sign the login cookies.