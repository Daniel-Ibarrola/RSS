import os


class Config:
    pass


class DevConfig(Config):
    ALERT_TIME = int(os.environ.get("ALERT_TIME", 5))
    MSG_TIME = int(os.environ.get("MSG_TIME", 5))
    ALERT_FILE_NAME = "test_alert"
    NON_ALERT_FILE_NAME = "test_sismo"
    IP = os.environ.get("IP", "localhost")
    PORT = int(os.environ.get("PORT", 12345))
    CHECK_LAST_ALERT = False


class DevConfigSupporting(DevConfig):
    CHECK_LAST_ALERT = True


class ProdConfig(Config):
    ALERT_TIME = 60
    MSG_TIME = 60
    ALERT_FILE_NAME = "alerta"
    NON_ALERT_FILE_NAME = "sismo"
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
