import os
import argparse
import queries


parser = argparse.ArgumentParser()
parser.add_argument("--debug",
    action="store_true", help="Debug mode (reload modules automatically")
parser.add_argument("--sparql-endpoint",
    type=str, help="SPARQL endpoint (MU_SPARQL_ENDPOINT by default)")


@app.route('/containers')
def main():
    containers = queries.list_container_events()
    return containers
