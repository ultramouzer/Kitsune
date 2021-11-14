import sys
from pathlib import Path
from datetime import datetime
from typing import List
from setproctitle import setthreadtitle

from src.internals.utils.logger import log
from src.internals.cache.redis import delete_keys

from development.internals import dev_random, service_name
from development.lib.randoms.dataset import generate_dataset
from development.types import Extended_Random
from development.types.models import DM, Comment, Post, User, File

from .comments import import_comments
from .dms import import_dms
from .posts import import_posts
from .users import import_users
from .download_file import download_file

sys.setrecursionlimit(100000)


def run_paysite_import(import_id: str, key: str, contributor_id: str, random: Extended_Random = dev_random):
    """Runs the importer."""
    setthreadtitle(f'Kitsune Import|{import_id}')
    dataset = generate_dataset(random)
    dms: List[DM] = []
    users: List[User] = []
    posts: List[Post] = []
    comments: List[Comment] = []

    if dataset['dms']:
        for dm in dataset['dms']:
            dm_model = DM(
                import_id=import_id,
                contributor_id=contributor_id,
                id=dm['id'],
                user=dm['user'],
                service=service_name,
                file={},
                published=dm['published'],
                content=dm['content']
            )
            dms.append(dm_model)

    if dataset['users']:
        for user in dataset['users']:
            user_model = User(
                id=user['id'],
                name=user['name'],
                service=service_name
            )
            users.append(user_model)

            if user['posts']:
                for post in user['posts']:
                    files: List[File] = []
                    file_item: File = None
                    atttachments: List[File] = []

                    if post['files']:
                        for file in post['files']:

                            # file_model = download_file(
                            #     file_path=file['path'],
                            #     service=service_name,
                            #     user=user['id'],
                            #     post=post['id'],
                            #     file_name=file['name']
                            # )

                            # files.append(file_model)
                            files.append(file)

                    if files:
                        file_item = files[0]
                    else:
                        file_item = {}

                    if len(files) > 1:
                        atttachments.extend(files[1:])

                    post_model = Post(
                        id=post['id'],
                        user=post['user'],
                        service=service_name,
                        file=file_item,
                        attachments=[],
                        published=post['published'],
                        edited=post['edited'],
                        shared_file=False,
                        added=datetime.now(),
                        title=post['title'],
                        content=post['content'],
                        embed={},
                    )
                    posts.append(post_model)

                    if post['comments']:
                        for comment in post['comments']:
                            comment_model = Comment(
                                id=comment['id'],
                                post_id=post['id'],
                                commenter=comment['commenter_id'],
                                content=comment['content'],
                                service=service_name,
                                published=comment['published'],
                                parent_id=comment['parent_id']
                            )
                            comments.append(comment_model)

    log(import_id, f'{len(dms)} DMs are going to be \"imported\"')
    import_dms(import_id, dms)
    log(import_id, f'{len(users)} artists are going to be \"imported\"')
    import_users(import_id, users)
    log(import_id, f'{len(posts)} posts are going to be \"imported\"')
    import_posts(import_id, posts)
    log(import_id, f'{len(comments)} comments are going to be \"imported\"')
    import_comments(import_id, comments)

    log(import_id, f"Finished the import \"{import_id}\" of service \"{service_name}\".")
    delete_keys([f'imports:{import_id}'])
