class Config:
    pass


class DevConfig(Config):
    ALERT_TIME = 4
    MSG_TIME = 5
    FEED_FILE_NAME = "test"
    IP = "localhost"
    PORT = 12345
    CHECK_LAST_ALERT = False


class DevConfigSupporting(DevConfig):
    CHECK_LAST_ALERT = True


class ProdConfig(Config):
    ALERT_TIME = 60
    MSG_TIME = 30
    FEED_FILE_NAME = "sasmex"
    # TODO: update this value
    IP = "localhost"
    PORT = 12345
    CHECK_LAST_ALERT = False


class ProdConfigSupporting(ProdConfig):
    IP = "localhost"
    CHECK_LAST_ALERT = True


configurations = {
    "dev": DevConfig(),
    "dev-support": DevConfigSupporting(),
    "prod": ProdConfig(),
    "prod-support": ProdConfigSupporting(),
}
