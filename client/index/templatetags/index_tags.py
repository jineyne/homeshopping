from datetime import datetime, timedelta

from django import template

register = template.Library()

@register.simple_tag
def parse_time(time):
    offset = time.split(":")
    hour = int(offset[0]) if offset[0] else 0
    minute = int(offset[1]) if offset[1] else 0

    return hour, minute

@register.simple_tag
def get_year(time):
    dt = datetime.strptime(time, "%Y%m%d").date()
    return dt.year

@register.simple_tag
def get_month(time):
    dt = datetime.strptime(time, "%Y%m%d").date()
    return dt.month

@register.simple_tag
def get_day(time):
    dt = datetime.strptime(time, "%Y%m%d").date()
    return dt.day

@register.simple_tag
def get_weekday(time):
    dt = datetime.strptime(time, "%Y%m%d").date()
    return ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()] + "요일"

@register.simple_tag
def get_hour(time):
    hour = get_org_hour(time)
    if hour > 12:
        hour-=12
        hour="오후 %d"%hour
    else:
        hour="오전 %d"%hour
    return hour

def get_org_hour(time):
    offset = time.split(":")
    hour = int(offset[0]) if offset[0] else 0
    return hour

@register.simple_tag
def get_minute(time):
    offset = time.split(":")
    minute = int(offset[1]) if offset[1] else 0
    return minute

@register.simple_tag
def convert_to_money(num):
    return "{:,}".format(int(num))


@register.simple_tag
def update_variable(value):
    return value

@register.simple_tag
def is_online(date, start_time, end_time):
    now_date = datetime.strptime("20171125", "%Y%m%d")
    now_date += timedelta(hours=13, minutes=0)
    org_date = datetime.strptime(date, "%Y%m%d")
    org_start_time = org_date \
        + timedelta(hours=get_org_hour(start_time), 
                    minutes=get_minute(start_time))
    org_end_time = org_date \
        + timedelta(hours=get_org_hour(end_time), 
                    minutes=get_minute(end_time))
    return org_start_time < now_date < org_end_time