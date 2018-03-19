import os


def get_config():
    address = os.environ.get('SURIROBOT_DB_ADDRESS')
    login = os.environ.get('SURIROBOT_DB_LOGIN')
    passwd = os.environ.get('SURIROBOT_DB_PASSWD')
    name = os.environ.get('SURIROBOT_DB_NAME')

    return dict(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI='mysql://' + login + ':' + passwd + '@' + address + '/' + name,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
