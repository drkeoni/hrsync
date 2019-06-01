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

Download all heart-rate data starting from 02/14/2017:
```
fetch_hr_data.py --period max --start_date 2017-02-14 > 2017-02-14_2019_06_01.json
```

&#169; 2018, Jon Sorenson
