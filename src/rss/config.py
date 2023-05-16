import os


class Config:
    pass


base_path = os.path.dirname(__file__)


class DevConfig(Config):
    ALERT_TIME = int(os.environ.get("ALERT_TIME", 5))
    MSG_TIME = int(os.environ.get("MSG_TIME", 5))
    ALERT_FILE_NAME = "test_alert"
    UPDATE_FILE_NAME = "test_update"
    NON_ALERT_FILE_NAME = "test_event"
    IP = os.environ.get("IP", "localhost")
    PORT = int(os.environ.get("PORT", 12345))
    SAVE_PATH = os.path.abspath(os.path.join(base_path, "..", "..", "feeds/"))
    CHECK_LAST_ALERT = False


class DevConfigSupporting(DevConfig):
    CHECK_LAST_ALERT = True


class ProdConfig(Config):
    ALERT_TIME = 60
    MSG_TIME = 60
    ALERT_FILE_NAME = "sasmex"
    UPDATE_FILE_NAME = "sasmex"
    NON_ALERT_FILE_NAME = "sasmex_evento"
    IP = "172.30.17.182"
    PORT = 13084
    SAVE_PATH = "/var/www/rss/"
    CHECK_LAST_ALERT = False


class ProdConfigSupporting(ProdConfig):
    IP = "172.30.17.182"
    CHECK_LAST_ALERT = True


configurations = {
    "dev": DevConfig(),
    "dev-support": DevConfigSupporting(),
    "prod": ProdConfig(),
    "prod-support": ProdConfigSupporting(),
}
