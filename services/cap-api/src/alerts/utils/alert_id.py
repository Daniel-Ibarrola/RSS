from datetime import datetime


def alert_id(date: datetime) -> str:
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    hour = f"{date.hour:02d}"
    minute = f"{date.minute:02d}"
    second = f"{date.second:02d}"
    return str(date.year) + month + day + hour + minute + second
