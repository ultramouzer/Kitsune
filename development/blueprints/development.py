from flask import Blueprint, request

from development.internals import dev_random
from development.lib import randoms
from development.lib.service_key import get_service_keys, kill_service_keys
from src.lib.autoimport import encrypt_and_save_session_for_auto_import

development = Blueprint('development', __name__)

@development.route('/development/service-keys', methods=['POST'])
def generate_service_keys():
    account_id: str = request.form.get('account_id')

    service_keys = [randoms.service_key(account_id) for key in range(dev_random.randint(15, 35))]

    for service_key in service_keys:
        encrypt_and_save_session_for_auto_import(
            service= service_key['service'],
            key= service_key['key'],
            contributor_id= service_key['contributor_id']
        )
        print(f"Saved {service_keys.index(service_key) + 1} keys out of {len(service_keys)}.")

    targets_amount = dev_random.randint(1, len(service_keys) - 1)
    marked_keys = get_service_keys(targets_amount)
    print(marked_keys)
    print(f"{len(marked_keys)} keys are marked for kill.")
    kill_service_keys(marked_keys)
    return '', 200
