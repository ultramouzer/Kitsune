import redis
import dateutil
import datetime
import copy
import ujson
import redis
from os import getenv
import config
import rb
import redis_map

cluster: rb.Cluster = None

class KitsuneRouter(rb.BaseRouter):
    def get_host_for_key(self, key):
        top_level_prefix_of_key = key.split(':')[0]
        if (redis_map.keyspaces.get(top_level_prefix_of_key) is not None):
            return redis_map.keyspaces[top_level_prefix_of_key]
        else:
            raise rb.UnroutableCommand()

def init():
    global cluster
    cluster = rb.Cluster(hosts=redis_map.nodes, host_defaults=redis_map.node_options, router_cls=KitsuneRouter, pool_options={"encoding": "utf-8", "decode_responses": True})
    return cluster

def get_redis():
    return cluster.get_routing_client()

def scan_keys(pattern):
    return cluster.get_local_client_for_key(pattern).scan_iter(match=pattern, count=5000)

def delete_keys(keys):
    conn = get_redis()
    for key in keys:
        conn.delete(key)

def delete_keys_pattern(patterns):
    redis = get_redis()
    for pattern in patterns:
        for key in scan_keys(pattern):
            redis.delete(key)

def serialize_dict(data):
    to_serialize = {
        'dates': [],
        'data': {}
    }

    for key, value in data.items():
        if type(value) is datetime.datetime:
            to_serialize['dates'].append(key)
            to_serialize['data'][key] = value.isoformat()
        else:
            to_serialize['data'][key] = value

    return ujson.dumps(to_serialize)

def deserialize_dict(data):
    data = ujson.loads(data)
    to_return = {}
    for key, value in data['data'].items():
        if key in data['dates']:
            to_return[key] = dateutil.parser.parse(value)
        else:
            to_return[key] = value
    return to_return

def serialize_dict_list(data):
    data = copy.deepcopy(data)
    return ujson.dumps(list(map(lambda elem: serialize_dict(elem), data)))

def deserialize_dict_list(data):
    data = ujson.loads(data)
    to_return = list(map(lambda elem: deserialize_dict(elem), data))
    return to_return