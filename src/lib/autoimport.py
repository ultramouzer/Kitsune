from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from ..internals.cache.redis import delete_keys, delete_keys_pattern
from ..internals.database.database import get_raw_conn, return_conn, get_cursor
from ..internals.utils.logger import log
from base64 import b64decode,b64encode
import hashlib
import config
from joblib import Parallel, delayed
from ..internals.cache.redis import get_redis

def log_import_id(key_id, import_id):
    conn = get_raw_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO saved_session_key_import_ids (key_id, import_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (int(key_id), import_id))
    conn.commit()
    return_conn(conn)

def revoke_v1_key(key_id):
    # mark as dead (should happen when a key is detected as unusable due to expiration/invalidation)
    conn = get_raw_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_session_keys WHERE id = %s", (int(key_id),))
    conn.commit()
    return_conn(conn)

def kill_key(key_id):
    # mark as dead (should happen when a key is detected as unusable due to expiration/invalidation)
    conn = get_raw_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE saved_session_keys_with_hashes SET dead = TRUE WHERE id = %s", (int(key_id),))
    conn.commit()
    return_conn(conn)

def decrypt_key(key, rsa_cipher, aes_cipher):
    key_to_decrypt = key
    try:
        key_to_decrypt['decrypted_key'] = rsa_cipher.decrypt(b64decode(key_to_decrypt['encrypted_key'])).decode('utf-8')
    except:
        if aes_cipher:
            try:
                key_to_decrypt['decrypted_key'] = aes_cipher.decrypt(b64decode(key_to_decrypt['encrypted_key'])).decode('utf-8')
            except:
                return None
        else:
            return None
    return (key_to_decrypt)

def decrypt_all_good_keys(privatekey, v1 = False):
    redis = get_redis()

    key_table = 'saved_session_keys' if v1 else 'saved_session_keys_with_hashes'
    key_der = b64decode(privatekey.strip())
    key_prv = RSA.importKey(key_der)
    rsa_cipher = PKCS1_OAEP.new(key_prv)

    aes_cipher = None
    encrypted_aes_key = redis.get('autoimport-aeskey')
    if encrypted_aes_key:
        decrypted_aes_key = rsa_cipher.decrypt(b64decode(encrypted_aes_key))
        aes_cipher = AES.new(decrypted_aes_key)
    
    conn = get_raw_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {key_table} WHERE dead = FALSE")
    encrypted_keys = cursor.fetchall()
    decrypted_keys = []
    decrypting = Parallel(n_jobs=-1)(delayed(decrypt_key)(key, rsa_cipher, aes_cipher) for key in encrypted_keys)
    for key in decrypting:
        if key:
            decrypted_keys.append(key)
    return decrypted_keys

def encrypt_and_save_session_for_auto_import(service, key, contributor_id = None, discord_channel_ids = None):
    redis = get_redis()

    rsa_key_der = b64decode(config.pubkey.strip())
    rsa_key_pub = RSA.importKey(key_der)
    rsa_cipher = PKCS1_OAEP.new(key_pub)

    aes_cipher = None
    encrypted_aes_key = redis.get('autoimport-aeskey') # base64'd encrypted aes key
    if not encrypted_aes_key:
        # create the key, encrypt it with rsa, and save to redis
        new_aes_key = get_random_bytes(16)
        aes_cipher = AES.new(key)
        encrypted_bin_aes_key = rsa_cipher.encrypt(new_aes_key)
        encrypted_aes_key = b64encode(encrypted_bin_aes_key).decode('utf-8')
        redis.set('autoimport-aeskey', encrypted_aes_key)
    else:
        # decrypt the key
        decrypted_aes_key = rsa_cipher.decrypt(b64decode(encrypted_aes_key))
        aes_cipher = AES.new(decrypted_aes_key)

    encrypted_bin_key = aes_cipher.encrypt(key.encode())
    encrypted_key = b64encode(encrypted_bin_key).decode('utf-8')

    conn = get_raw_conn()
    cursor = conn.cursor()
    model = {
        'service': service,
        'discord_channel_ids': discord_channel_ids,
        'encrypted_key': encrypted_key,
        'contributor_id': int(contributor_id) if contributor_id else None,
        'hash': hashlib.sha256((key + config.salt).encode('utf-8')).hexdigest()
    }
    query = "INSERT INTO saved_session_keys_with_hashes ({fields}) VALUES ({values}) ON CONFLICT DO NOTHING".format(
        fields = ','.join(model.keys()),
        values = ','.join(['%s'] * len(model.values()))
    )
    cursor.execute(query, list(model.values()))
    conn.commit()
    return_conn(conn)
    if contributor_id:
        delete_keys_pattern(['saved_keys:' + str(contributor_id)])
