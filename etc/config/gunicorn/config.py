# gunicorn config file

pidfile = '/tmp/gunicorn_hrsync.pid'
workers = 4
bind = '0.0.0.0:8421'
accesslog = '/opt/log/hrsync/gunicorn-access.log'
errorlog = '/opt/log/hrsync/gunicorn-error.log'
loglevel = 'info'
timeout = 1800
graceful_timeout = 1800
keepalive = 600
