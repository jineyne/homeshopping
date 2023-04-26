import json
from datetime import datetime, timedelta

from flask import make_response, jsonify
from flask_restful import Resource

from models import Category, init_db, db
from common.utils import CleanList
from server import cache

class CategoryView(Resource):


    def get(self):
        init_db()

        cache_name = "cache-category"

        rv = cache.get(cache_name)
        if rv is None:
            items = CleanList(db.session.query(Category).all())
            cache.set(cache_name, items, timeout=24*60*60)
        else:
            items = rv

        json_data = json.dumps(items, ensure_ascii=False, indent=4)
        res = make_response(json_data)
        res.headers["Content-Type"] = "application/json;charset=utf-8"
        res.status_code = 200

        return res