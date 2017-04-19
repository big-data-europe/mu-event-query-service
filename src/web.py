import os
import queries
import json
from time import time

timenow = time()

@app.route('/containers')
def main():
    containers = queries.list_container_events(timenow)
    queries.write_json_into_file(containers)
    return json.dumps(containers)
