import json
from datetime import datetime, timedelta

from flask import make_response, jsonify
from flask_restful import Resource

from models import Item, init_db, db
from common.utils import CleanItem
from server import cache

class ItemView(Resource):


    def get(self, ft="all", date="", time="", asc="asc"):
        init_db()

        cache_name = "cache-%s-%s-%s-%s"%(ft, date, time, asc)

        rv = cache.get(cache_name)
        if rv is None:
            items = []

            try:
                min_day = datetime(year=2017, month=11, day=20)
                max_day = datetime(year=2017, month=11, day=30)

                dt = datetime.strptime(date, "%Y%m%d")

                if not (min_day <= dt <= max_day):
                    return {"error_mesage": "out of days"}, 409
            except:
                return {"error_mesage": "out of days"}, 409

            offset = len(time)-2
            hour = int(time[:offset]) if time[:offset] else 0
            minute = int(time[offset:]) if time[offset:] else 0

            time_start = datetime(year=dt.year, month=dt.month, day=dt.day,
                                  hour=hour, minute=minute)
            time_start -= timedelta(minutes=1)
        
            if asc == "asc":
                time_end = time_start + timedelta(hours=4)
            else:
                time_end = time_start
                time_start = time_start - timedelta(hours=4)

            get_items = db.session.query(Item).filter(
                Item.start_time.between(time_start, time_end)
            ).all()

            for item in get_items:
                cleaned_item = CleanItem(item)
                items.append(cleaned_item)

            if ft != "all":
                tkns = ft.split(":")
                type = None
                while len(tkns) != 0:
                    if tkns[0] == "ct":
                        type="ct"
                        tkns.pop(0)

                    elif tkns[0] == "m":
                        type="m"
                        tkns.pop(0)

                    if type == "ct":
                        _items = list(filter(
                            lambda x:
                                "name" in x["category"] and
                                x["category"]["name"] == tkns[0],
                            items
                        ))
                        items = _items
                        tkns.pop(0)


                    elif type == "m":
                        _items = list(filter(
                            lambda x:
                                "name" in x["mall"] and
                                x["mall"]["name"] == tkns[0],
                            items
                        ))
                        items = _items
                        tkns.pop(0)

            if len(items) == 0:
                return {"error_message": "unable to find item"}, 204
                
            list_ = []
            for item in items:
                exist_items = list(filter(
                    lambda x:
                        item["mall"]["name"] == x["mall"]["name"] and
                        item["start_time"] == x["start_time"] and
                        item["end_time"] == x["end_time"],
                    list_
                ))
                if len(exist_items) == 0:
                    list_.append(item)
                elif len(exist_items) == 1:
                    if not "sub_item" in exist_items[0]:
                        exist_items[0]["sub_item"] = []
                    exist_items[0]["sub_item"].append(item)
                else:
                    print(len(exist_items))
                    raise KeyError("something wrong")
            items = list_

            items = sorted(items, key=lambda x: x["start_time"])
            cache.set(cache_name, items, timeout=24*60*60)
        else:
            items = rv


        json_data = json.dumps(items, ensure_ascii=False, indent=4)
        res = make_response(json_data)
        res.headers["Content-Type"] = "application/json;charset=utf-8"
        res.status_code = 200

        return res