import datetime


def get_current_date():
    d = datetime.datetime.now()
    return d.strftime("%a, %d %b %Y %I:%M:%S %Z")