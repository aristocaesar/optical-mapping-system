from datetime import datetime, timedelta, timezone

def get_wib_now():
    """Returns the current time in WIB (UTC+7) sebagai naive datetime"""
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
