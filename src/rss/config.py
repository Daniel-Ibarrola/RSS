
class Config:
    pass


class DevConfig(Config):
    ALERT_TIME = 4
    MSG_TIME = 5
    FEED_FILE_NAME = "test"
    IP = "localhost"
    PORT = 12345


class ProdConfig(Config):
    ALERT_TIME = 60
    MSG_TIME = 30
    FEED_FILE_NAME = "sasmex"
    # TODO: update this value
    IP = "localhost"
    PORT = 12345
