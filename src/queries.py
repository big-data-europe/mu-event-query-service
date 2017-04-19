from helpers import log, query
from time import sleep
from itertools import groupby, ifilter
import json


def prefix():
    """
    Returns a list with all the needed prefixes to query the database
    """
    string = "PREFIX dockevent: <http://ontology.aksw.org/dockevent/>\n"
    string += "PREFIX dockcontainer: <http://ontology.aksw.org/dockcontainer/>\n"
    string += "PREFIX dockcontainer_network: <http://ontology.aksw.org/dockcontainer/network/>\n"
    string += "PREFIX dockevent_type: <http://ontology.aksw.org/dockevent/types/>\n"
    string += "PREFIX dockevent_action: <http://ontology.aksw.org/dockevent/actions/>\n\n"
    return string


def get_triple_value(data, predicate):
    value = filter(lambda item: predicate in item['p']['value'], data)
    return value[0]['o']['value']


def list_container_events(date_from):
    """
    Queries the database for all new events (after current timestamp) and returns
    a JSON object with the data.
    """
    my_query = prefix()
    my_query += "select distinct ?cname ?p ?o\n"
    my_query += "where {\n"
    my_query += "?dockevent a dockevent_type:event .\n"
    my_query += "?dockevent dockevent:type dockevent_type:container .\n"
    my_query += "?dockevent dockevent:action dockevent_action:start .\n"
    my_query += "?dockevent dockevent:container ?curl .\n"
    my_query += "?dockevent dockevent:time ?time .\n"
    my_query += "?curl dockcontainer:name ?cname .\n"
    my_query += "?curl dockcontainer:network ?cnetwork .\n"
    my_query += "?cnetwork ?p ?o .\n"
    my_query += "FILTER (?time > \"%s\"^^<http://www.w3.org/2001/XMLSchema#int>)\n" % int(round(date_from))
    my_query += "} order by ?cname \n"

    result = query(my_query)

    custom_result = []

    for key, items in groupby(result['results']['bindings'], lambda x: x['cname']['value']):
        list_items = list(items)
        custom_dict = {
            'name': key.replace("/",""),
            'data': {
                'ipAddress': get_triple_value(list_items, 'network/ipAddress'),
                'interface_id': get_triple_value(list_items, 'network/id'),
                'network_name': get_triple_value(list_items, 'network/name')
            }
        }
        custom_result.append(custom_dict)

    return json.dumps(custom_result)
