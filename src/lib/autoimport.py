from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from ..internals.cache.redis import delete_keys, delete_keys_pattern
from ..internals.database.database import get_raw_conn, return_conn, get_cursor
from ..internals.utils.logger import log
from base64 import b64decode,b64encode
import config

def log_import_id(key_id, import_id):
    conn = get_raw_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO saved_session_key_import_ids (key_id, import_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (int(key_id), import_id))
    conn.commit()
    return_conn(conn)

def kill_key(key_id):
    # mark as dead (should happen when a key is detected as unusable due to expiration/invalidation)
    conn = get_raw_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE saved_session_keys SET dead = TRUE WHERE id = %s", (int(key_id),))
    conn.commit()
    return_conn(conn)

def decrypt_all_good_keys(privatekey):
    key_der = b64decode(privatekey.strip())
    key_prv = RSA.importKey(key_der)
    cipher = PKCS1_OAEP.new(key_prv)

    conn = get_raw_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_session_keys WHERE dead = FALSE")
    encrypted_keys = cursor.fetchall()
    decrypted_keys = []
    for key in encrypted_keys:
        key_to_decrypt = key
        key_to_decrypt['encrypted_key'] = cipher.decrypt(b64decode(key_to_decrypt['encrypted_key'])).decode('utf-8')
        decrypted_keys.append(key_to_decrypt)

    return decrypted_keys

def encrypt_and_save_session_for_auto_import(service, key, contributor_id = None, discord_channel_ids = None):
    key_der = b64decode(config.pubkey.strip())
    key_pub = RSA.importKey(key_der)
    cipher = PKCS1_OAEP.new(key_pub)
    encrypted_bin_key = cipher.encrypt(key.encode())
    encrypted_key = b64encode(encrypted_bin_key).decode('utf-8')

    conn = get_raw_conn()
    cursor = conn.cursor()
    model = {
        'service': service,
        'discord_channel_ids': discord_channel_ids,
        'encrypted_key': encrypted_key,
        'contributor_id': int(contributor_id) if contributor_id else None
    }
    query = "INSERT INTO saved_session_keys ({fields}) VALUES ({values}) ON CONFLICT DO NOTHING".format(
        fields = ','.join(model.keys()),
        values = ','.join(['%s'] * len(model.values()))
    )
    cursor.execute(query, list(model.values()))
    conn.commit()
    return_conn(conn)
    if contributor_id:
        delete_keys_pattern(['saved_keys:' + contributor_id])
