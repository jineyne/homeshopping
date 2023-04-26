import datetime
import json

from models import Item, ShoppingMall, Category
from models import db

def CleanItem(item):
    res = {}
    for key, value in item.__dict__.items():
        if key == "mall":
            m = db.session.query(ShoppingMall)\
                    .filter(ShoppingMall.id == value).one_or_none()
            res[key] = CleanObject(m)
            continue
        elif key == "category":
            c = db.session.query(Category)\
                    .filter(Category.id == value).one_or_none()
            res[key] = CleanObject(c)
            continue
        elif key == "start_time":
            res["date"] = value.strftime("%Y%m%d")
            res["start_time"] = value.strftime("%H:%M")
        elif key == "end_time":
            res[key] = value.strftime("%H:%M")
        elif isinstance(value, str) or isinstance(value, int):
            res[key] = value

    return res

def CleanList(items):
    res = []
    for item in items:
        res.append(CleanObject(item))
    return res

def CleanObject(obj):
    if obj is None:
        return {}

    res = {}
    for key, value in obj.__dict__.items():
        if isinstance(value, datetime.time):
            res[key] = value.strftime("%H:%M")
        elif isinstance(value, datetime.date):
            res[key] = value.strftime("%Y%m%d")
        elif isinstance(value, str) or isinstance(value, int):
            res[key] = value
        else:
            pass
    return res