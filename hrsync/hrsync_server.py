__doc__ = """ """
import os
import sys
import logging

from flask import Flask, render_template

APP_ROOT = os.path.abspath(os.path.join('..',os.path.dirname(__name__)))
CONFIG_PATH = os.path.join(APP_ROOT,'etc','config','config.py')
DEFAULT_PORT = 80

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
            help='Port to start the hrsync server on')
    parser.add_argument('--debug', action='store_true', default=False,
            help='Launch server in debug mode')
    args = parser.parse_args()
    return args

def create_server():
    app = Flask(__name__)
    app.config.from_pyfile(


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error_500.html', msg=str(error)), 500


@app.before_first_request
def setup_logging():
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    log_handler = logging.StreamHandler(stream=sys.stderr)
    log_handler.setFormatter(logging.Formatter(log_format))
    log_handler.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)


app = create_server()

if __name__ == '__main__':
    args = parse_args()
    app.run(host=app.config['FLASK_HOST'], port=args.port, debug=args.debug)
