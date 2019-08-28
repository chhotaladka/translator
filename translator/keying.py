from django.utils.encoding import smart_str
import hashlib

def _smart_key(key):
    return hashlib.md5(smart_str('_'.join([c for c in key if ord(c) > 32 and ord(c) != 127])).encode('utf-8')).hexdigest()

def make_key(key, key_prefix, version):
    "Truncate all keys to 250 or less and remove control characters"
    return ':'.join([key_prefix, str(version), _smart_key(key)])[:250]