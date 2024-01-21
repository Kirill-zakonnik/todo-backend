from flask import Flask, request
from resourсes import EntryManager, Entry

app = Flask(__name__)



@app.route("/api/entries/")
def get_entries():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    entries = [entry.json() for entry in entry_manager.entries]
    return entries


@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    json_data = request.get_json()
    entry_manager = EntryManager(FOLDER)
    for entry_data in json_data:
        entry = Entry.from_json(entry_data)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


FOLDER = '/tmp/'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)