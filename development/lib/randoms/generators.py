from development.internals import dev_random, asset_files, service_name

from development.types import Extended_Random, Service_Key_DB
from .types import Random_DM, Random_Post, Random_File, Random_Comment, Random_User


def random_post(user_id: str = None, random: Extended_Random = dev_random) -> Random_Post:
    id = random.string()
    user = user_id if user_id else random.string()
    published_date = random.date() if random.boolean() else None
    edited_date = random.date(published_date) if published_date and random.boolean() else None
    title = random.lorem_ipsum(1, 1, 1) if random.boolean() else ''
    content = random.lorem_ipsum() if random.boolean() else ''
    files_amount = random.randint(0, 4)
    files = [random_file(random) for index in range(files_amount)] if files_amount else []
    comments_amount = random.randint(0, 30) if random.boolean() else 0
    comments = [random_comment(user, random) for index in range(comments_amount)] if comments_amount else []

    post = Random_Post(
        id=id,
        user=user,
        published=published_date,
        edited=edited_date,
        title=title,
        content=content,
        files=files,
        comments=comments
    )

    return post


def random_user(user_id: str = None, random: Extended_Random = dev_random) -> Random_User:
    post_amount = random.randint(1, 200)
    posts = [random_post(user_id, random) for index in range(post_amount)]
    user = Random_User(
        id=user_id if user_id else random.string(),
        name=random.varchar(3, 50) if random.boolean else random.text(3, 50),
        posts=posts
    )

    return user


def random_dm(user_id: str = None, random: Extended_Random = dev_random) -> Random_DM:
    dm = Random_DM(
        id=random.string(),
        user=user_id if user_id else random.string(),
        published=random.date(),
        content=random.lorem_ipsum()
    )

    return dm


def random_file(random: Extended_Random = dev_random) -> Random_File:
    file_path = random.choice(asset_files)
    file = Random_File(
        path=str(file_path),
        name=file_path.name
    )

    return file


def random_comment(user_id: str = None, random: Extended_Random = dev_random) -> Random_Comment:
    comment = Random_Comment(
        id=random.string(),
        commenter_id=user_id if user_id else random.string(),
        content=random.lorem_ipsum(),
        parent_id=random.string(),
        published=random.date()
    )
    return comment


def service_key(account_id: str):
    key_item = Service_Key_DB(
        service=service_name,
        key=dev_random.text(),
        contributor_id=account_id,
    )
    return key_item
