#!/usr/bin/python3

from datetime import datetime

def validate_date_time(date, time):

    date_time = date + " " + time
    try:
        full_date = datetime.strptime(date_time, '%d.%m.%Y %H:%M')
    except ValueError:
        raise ValueError("Incorrect datetime format, date argument must be DD.MM.YYYY and time argument HH:MM")

    if len(date_time) != 16:
        raise ValueError("Incorrect datetime format, date argument must be DD.MM.YYYY and time argument HH:MM")
    
    now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M")
    if full_date < datetime.strptime(now, '%d.%m.%Y %H:%M'):
        raise ValueError("Not supported date, probably you try to find connection from the past")

