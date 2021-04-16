import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode
from os import makedirs
from os.path import join
import uuid

pubkey = """
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAidwu1XAMIyt9nI2UCj1u
Mc234/eWHTZiQCAP6StTnlKoSWbHZOzn50kQQ6it0G75nAZ8PuNISLGfA2amLou1
uKzkj75qooykdr1YNqXMUlp1mEsGnWTeWq63IazqAO97VHDrD7p6jxy//io/vz24
jTqwdrT0uKv4d4IyFPEewxuncS5chHz8V8taIaVeBAgwW2H57y1RaRb3LDdfRDng
gqkAqUUiaYoGmoB67drGwRs4/HkuQnDtmf4QJaNGmKC20+2IuCMD2wJpTZzxpu3N
6e8eoXActqy5npZHdem/43GRd/YEEP0yWdNNEVRUfCocjsykFRpMOY+lXFTIkmzD
mSBXB8zi0ZXQHIlUcB1VhZW1US9xVYfxFkldr4uTC/lF2ZaJraW4wtWN4gcB5DL/
3LX47nir22zJN1jIyGI+hy6/+q82XkWH6S7B61eLB+uOsa/PWh6ugJ9z0vvd3lMW
LF6xnRfem8C9UCh2gMOvHodeprugX9Bkd6gL8q5ziw/Y9rD094wvFk+2lvqDRG4h
xrRvGgHmOizG3QqKEnoctSTvgFf/PnCqd0UDAQmwRcB63SmtyjHEnPsBwM3x3Mvh
CPqjGSTYD4QAR8DIDQZA/4KPbNQdKxzswCWZU1RwhVqhUNzHtJAyb/Puhh/PnchX
mExh8S9vH2MIe9/z5Ms+PZkCAwEAAQ==
"""

base_dir = '/tmp/session_keys/'

def encrypt_and_log_session(import_id, service, key):
    try:
        makedirs(base_dir, exist_ok = True)
        data = {
            'import_id': import_id,
            'service': service,
            'key': key
        }
        to_encrypt = json.dumps(data)

        key_der = b64decode(pubkey.strip())
        key_pub = RSA.importKey(key_der)
        cipher = Cipher_PKCS1_v1_5.new(key_pub)
        cipher_text = cipher.encrypt(to_encrypt.encode())

        filename = f'{service}-{import_id}'
        to_write = b64encode(cipher_text).decode('utf-8')

        with open(join(base_dir, filename), 'w') as f:
            f.write(to_write)
    except Exception as e:
        print(f'Error encrypting session data. Continuing with import: {e}')
