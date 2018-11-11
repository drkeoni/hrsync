## hrsync

This code base started out as a standalone web app that I had 
believed was necessary to be able use the Fitbit API.
Luckily I found the python-fitbit package and realized
I could register a non-public callback URL for authentication,
and that allowed me to get away from designing a web app.
The code base is now a collection of scripts and ipython notebooks.

### Installation

```
make create-ve
make setup
```

### Usage

Source the environment and login:
```
. etc/setup_local.bash
fitbit_login.py
```


&#169; 2018, Jon Sorenson
