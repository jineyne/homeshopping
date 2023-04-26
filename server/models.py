from datetime import datetime

from server import db

def init_db():
    db.create_all()

class ShoppingMall(db.Model):
    __tablename__ = "shopping_malls"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    label = db.Column(db.String(50), unique=True)

    def __init__(self, name=None, label=""):
        self.name = name
        self.label = label

    def __repr__(self):
        return "<ShoppingMall %r>" % (self.name)

class Category(db.Model):
    __tablename__ = "categoris"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<Category %r>" % (self.name)


class Item(db.Model):
    __tablename__ = "items"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    mall = db.Column(db.ForeignKey("shopping_malls.id",
                                   onupdate="CASCADE", ondelete="CASCADE"))
    #date = db.Column(db.Date)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    category = db.Column(db.ForeignKey("categoris.id", onupdate="CASCADE",
                                       ondelete="CASCADE"))
    url = db.Column(db.String(255))
    img = db.Column(db.String(255))
    price = db.Column(db.String(255))
    org_price = db.Column(db.String(255))

    def __init__(self, id=None, name=None, mall=None, date=None,
            start_time=None, end_time=None, category=None, url=None,
            img=None, price=None, org_price=None):
        self.id = int(id)
        self.name = name
        self.mall = mall.id
        date_ = datetime.strptime(date, "%Y%m%d")

        offset = len(start_time)-2
        hour = int(start_time[:offset]) if start_time[:offset] else 0
        minute = int(start_time[offset:]) if start_time[offset:] else 0
        self.start_time = datetime(year=date_.year, month=date_.month, 
                                   day=date_.day, hour=hour, minute=minute)

        offset = len(end_time)-2
        hour = int(end_time[:offset]) if end_time[:offset] else 0
        minute = int(end_time[offset:]) if end_time[offset:] else 0
        self.end_time = datetime(year=date_.year, month=date_.month, 
                                 day=date_.day, hour=hour, minute=minute)

        self.category = category.id
        self.url = url
        self.img = img
        self.price = price
        self.org_price = org_price

    def __repr__(self):
        return "<Item %r>" % (self.name)
    