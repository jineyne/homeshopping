import urllib
import unittest

from flask import Flask
from flask_testing import TestCase

from server import build_app, db
from resource.init import setup_db_with_data

class ServerTest(TestCase):

    SQLALCHEMY_DATABASE_URL= "sqlite://"
    TESTING = True

    def create_app(self):
        return build_app(conf=self)

    def setUp(self):
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_server_is_up(self):
        res = self.client.get("/item/all/20171125/1300/asc")
        assert res.status_code == 204, "status_code is %d"%res.status_code

    def test_after_end_time(self):
        res = self.client.get("/item/all/20171131/0100/asc")
        assert res.status_code == 409, "status_code is %d"%res.status_code

    def test_before_start_time(self):
        pass

class ItemTest(TestCase):

    SQLALCHEMY_DATABASE_URL= "sqlite://"
    TESTING = True

    def create_app(self):
        return build_app(conf=self)

    def setUp(self):
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_item(self):
        setup_db_with_data()

        res = self.client.get("/item/all/20171125/0000/asc")
        assert res.status_code == 200, "status_code is %d"%res.status_code

        res = self.client.get("/cate")
        assert res.status_code == 200, "status_code is %d"%res.status_code

        res = self.client.get("/mall")
        assert res.status_code == 200, "status_code is %d"%res.status_code



if __name__ == '__main__':
    unittest.main()