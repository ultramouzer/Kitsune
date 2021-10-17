from datetime import datetime
from flask import request, current_app, session
import hashlib
import random
import dateutil.parser
import hashlib
import os

def get_value(d, key, default = None):
    try:
        return d[key]
    except Exception:
        return default

def sort_dict_list_by(l, key, reverse = False):
    return sorted(l, key=lambda v: v[key], reverse=reverse)

def restrict_value(value, allowed, default = None):
    if value not in allowed:
        return default
    return value

def take(num, l):
    if len(l) <= num:
        return l
    return l[:num]

def offset(num, l):
    if len(l) <= num:
        return []
    return l[num:]

def limit_int(i, limit):
    if i > limit:
        return limit
    return i

def parse_int(string, default = 0):
    try:
        return int(string)
    except Exception:
        return default

def get_import_id(data):
    salt = str(random.randrange(0, 1000))
    return take(16, hashlib.sha256((data + salt).encode('utf-8')).hexdigest())

def parse_date(string, default = None):
    try:
        return dateutil.parser.parse(string)
    except:
        if default is None:
            return datetime(1970, 1, 1)
        return default

def get_hash_of_file(filename):
    with open(filename, 'rb') as f:
        file_hash_raw = hashlib.sha256()
        for chunk in iter(lambda: f.read(8192), b''):
            file_hash_raw.update(chunk)
        return file_hash_raw.hexdigest()