from pony.orm import Database, PrimaryKey, Required, \
    db_session, ObjectNotFound
from os import getenv

db = Database()
db.bind(provider='sqlite', filename=f'{"/app/config/" if getenv("IS_DOCKER", False) else "./"}/database.sqlite',
        create_db=True)


class Support(db.Entity):
    id = PrimaryKey(int)
    Action = Required(str, 255)


class CompletedTorrents(db.Entity):
    hash = PrimaryKey(str)


db.generate_mapping(create_tables=True)


def read_support(chat_id):
    with db_session:
        try:
            return Support[chat_id].Action
        except ObjectNotFound:
            return ""


def write_support(status, chat_id):
    with db_session:
        try:
            Support[chat_id].Action = status
        except ObjectNotFound:
            Support(Action=status, id=chat_id)


def write_completed_torrents(torrent_hash):
    with db_session:
        CompletedTorrents(hash=torrent_hash)


def read_completed_torrents(torrent_hash):
    with db_session:
        return CompletedTorrents.get(hash=torrent_hash)
