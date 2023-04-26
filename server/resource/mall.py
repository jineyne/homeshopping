import json
from datetime import datetime, timedelta

from flask import make_response, jsonify
from flask_restful import Resource

from models import ShoppingMall, init_db, db
from common.utils import CleanList
from server import cache

class ShoppingMallView(Resource):


    def get(self):
        init_db()

        cache_name = "cache-shopping-malls"

        rv = cache.get(cache_name)
        if rv is None:
            items = CleanList(db.session.query(ShoppingMall).all())
            cache.set(cache_name, items, timeout=24*60*60)
        else:
            items = rv

        json_data = json.dumps(items, ensure_ascii=False, indent=4)
        res = make_response(json_data)
        res.headers["Content-Type"] = "application/json;charset=utf-8"
        res.status_code = 200

        return res