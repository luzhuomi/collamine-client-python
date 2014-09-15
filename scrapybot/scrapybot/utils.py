
from string import replace
import datetime


def normalized9GagDate(s):
    s = s.replace("From",'')
    if s[-3:] == "ago":
        tokens = s.split(" ")
        if len(tokens) > 2:
            if (tokens[1] == "day") or (tokens[1] == "days"):
                # days
                s = str(datetime.date.today() - datetime.timedelta(days=int(tokens[0])))
            else:
                # hours
                s = str((datetime.datetime.today() - datetime.timedelta(hours=int(tokens[0]))).date())
    todaystr = str(datetime.date.today())
    yesterdaystr = str(datetime.date.today()-datetime.timedelta(days=1))
    return replace(replace(s.upper(), 'TODAY', todaystr), 'YESTERDAY', yesterdaystr)

def normalizeFriendlyDate(s):
    todaystr = str(datetime.date.today())
    yesterdaystr = str(datetime.date.today()-datetime.timedelta(days=1))
    return replace(replace(s.upper(), 'TODAY', todaystr), 'YESTERDAY', yesterdaystr)

