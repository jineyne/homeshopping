from datetime import datetime

from flask_restful import Resource
from tqdm import tqdm
from sklearn.externals import joblib

from models import Category, ShoppingMall, Item, init_db, db

def parse_data(data):
    mall_name = {
        "cjmall": "cj오쇼핑",
        "gsshop": "gs홈쇼핑",
        "lottemall": "롯데홈쇼핑",
        "hmall": "현대홈쇼핑",
    }

    mall = db.session.query(ShoppingMall)\
        .filter(ShoppingMall.name == data["genre2"]).one_or_none()
    if(mall is None):
        mall = ShoppingMall(data["genre2"], mall_name[data["genre2"]])
        db.session.add(mall)
        db.session.commit()
    
    cate = db.session.query(Category)\
        .filter(Category.name == data["cate1"]).scalar()
    if(cate is None):
        cate = Category(data["cate1"])
        db.session.add(cate)
        db.session.commit()

    item = Item(
        id=data["id"], name=data["name"], date=str(data["date"]), mall=mall,
        start_time=str(data["start_time"]), end_time=str(data["end_time"]),
        category=cate, url=data["url"], img=data["img"], 
        price=data["price"], org_price=data["org_price"])
    db.session.add(item)
    db.session.commit()

def setup_db_with_data():
    datas = joblib.load("timeline_goods_dump.dat")
    if len(datas) is not 0:
        for data in tqdm(datas):
            parse_data(data)

class InitView(Resource):


    def get(self):
        init_db()

        setup_db_with_data()

        return "success!", 200
