#!/usr/bin/env python3
import sys
import os
import argparse
import logging
import json
import datetime as dt

from fitbit import Fitbit
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests_oauthlib.oauth2_session import TokenUpdated

LOG_FORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(LOG_FORMAT))
log.addHandler(ch)

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
AUTH_FILE = os.path.join(ROOT, '.fitbit_auth.json')
DATE_FORMAT = '%Y-%m-%d'

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--period', default='1d',
                        help='Period of time for heart-rate data.  '
                             'Examples: 1d, 1w, 30d, 6m'
                       )
    parser.add_argument('--start_date', default=None,
                        help='If specified use this date as the start date '
                             'for querying the API (until now).  Format yyyy-mm-dd'
                       )
    args = parser.parse_args()
    return args


def get_fitbit_credentials():
    try:
        client_id = os.environ['FITBIT_APP_ID']
        client_secret = os.environ['FITBIT_APP_SECRET']
        auth_data = json.load(open(AUTH_FILE,'r'))
    except KeyError:
        log.error('Fitbit credentials not found in the environment.')
        return None, None, None
    return client_id, client_secret, auth_data


def run(args):
    client_id, client_secret, auth_data = get_fitbit_credentials()
    if client_id is None:
        return 1

    fitbit_api = Fitbit(client_id=client_id, client_secret=client_secret,
            access_token=auth_data['access_token'], refresh_token=auth_data['refresh_token'],
            expires_at=auth_data['expires_at'])

    try:
        if args.start_date:
            try:
                start_date = dt.datetime.strptime(args.start_date, DATE_FORMAT)
            except ValueError:
                log.error("'{}' does not look like a date in format {}".format(args.start_date, DATE_FORMAT))
                return 1
            end_date = dt.datetime.now()
            hr_data = fitbit_api.time_series('heart', base_date=start_date, end_date=end_date)
        else:
            hr_data = fitbit_api.time_series('heart', period=args.period)
    except TokenExpiredError as e:
        log.exception(e)
        log.error('You need to reauthenticate with fitbit oauth')
        return 1
    except TokenUpdated as e:
        log.exception(e)
        log.error('You need to reauthenticate with fitbit oauth')
        return 1

    print(json.dumps(hr_data, indent=4))

    return 0


if __name__ == '__main__':
    args = parse_args()
    sys.exit(run(args))
