## hrsync

`hrsync` (heart-rate synchronizer) is a standalone web app for downloading heart-rate
information from Fitbit.  Fitbit hasn't made it easy yet for users to download
their own heart-rate data, but they will provide this data to registered applications
through their Web API.  This repository provides a web server which functions
as a Fitbit Application for downloading heart-rate data.

Notable features:

* OAuth 2.0 authentication to the Fitbit API.

* Daily and summary heart-rate data is downloaded and stored in a SQLite database.

### Installation

```
make create-ve
make setup
```

&#169; 2018, Jon Sorenson
