import json

from flask import request, Blueprint

import logging
logger = logging.getLogger(__name__)


bp = Blueprint("main", __name__, static_folder="static", static_url_path="/static/views")


@bp.route('/', methods=['GET'])
def index():
    return bp.send_static_file('index.html')


@bp.route('/fetchentries', methods=['GET'])
def fetchentries():
    if request.method == 'GET':
        try:
            with open('entries.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            with open('entries.json', 'w') as f:
                f.write('{"entries": []}')
                return {}
    return None


@bp.route('/addentry', methods=['POST'])
def addentry():
    if request.method == 'POST':
        params = request.get_json()
        with open('entries.json', 'r') as f:
            data = json.load(f)
        data['entries'].append({
            'url': params['url'],
            'chatId': params['chatId'],
            'name': params['name'],
        })
        with open('entries.json', 'w') as f:
            json.dump(data, f, indent=4)
        return data
