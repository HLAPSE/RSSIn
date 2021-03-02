import datetime

def formatDatetime(time):
    d = datetime.datetime(*(time[0:6]))
    return d.isoformat(' ')