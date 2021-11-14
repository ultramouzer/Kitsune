from development.internals import dev_random
from development.types import Extended_Random

from .generators import random_dm, random_user
from .types import Random_Dataset


def generate_dataset(random: Extended_Random = dev_random):
    """
    Creates a random dataset of import items.
    """
    users_amount = random.randint(0, 30)
    users = [random_user(random=random) for index in range(users_amount)] if users_amount else []

    # some of the users will have a DM with the account
    dms_amount = random.randint(0, 30)
    dms = [random_dm(random=random) for index in range(dms_amount)] if dms_amount else []
    dm_users = random.sample(users, random.randint(0, len(users) - 1))
    dms.extend([random_dm(user['id'], random) for user in dm_users] if dm_users else [])

    dataset = Random_Dataset(
        dms=dms,
        users=users,
    )

    return dataset
