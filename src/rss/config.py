
class Config:
    pass


class DevConfig(Config):
    ALERT_TIME = 4
    MSG_TIME = 5
    FEED_FILE_NAME = "test"


class ProdConfig(Config):
    ALERT_TIME = 60
    MSG_TIME = 30
    FEED_FILE_NAME = "sasmex"

