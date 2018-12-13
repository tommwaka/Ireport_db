import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app
from ...db_config import _init_db
from ...db_config import destroy_tables


class AuthTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.user = {
                "firstname" : "mwakidusa",
                "lastname" : "tommwasaka",
                "email" : "tom@gmail.com",
                "username" : "hosanssasadqw",
                "password" : "dhfjfjjs"
            }
        self.redflag = {
              "type" : "redflag",
              "location" : "45E, 24N",
              "status" : "draft", 
              "images" : "image", 
              "videos" : "video",
              "comment" : "whats happening.."
            }
        with self.app.app_context():
            self.db = _init_db()

    def create_user(self, path='/v2/auth/signup', data={}):
        if not data:
            data = self.user
        result = self.client.post(path, data=json.dumps(data),
                                  content_type='application/json')
        return result

    def create_incident(self, path='/v2/redflags', data={}):
        user = self.create_user()
        token = user.json['Auth-token']
        headers = {"Authorization": "Bearer {}".format(token)}
        if not data:
            data = self.redflag
        result = self.client.post(path, data=json.dumps(data), headers=headers,
                                                content_type='application/json')
        return result

    def get_flags(self, path='/v2/redflags'):
        user = self.create_user()
        token = user.json['Auth-token']
        headers = {"Authorization": "Bearer {}".format(token)}
        result = self.client.get(path, headers=headers, content_type='application/json')        
        return result

    def test_post_incident(self):
        new_flag = self.create_incident()
        self.assertEqual(new_flag.status_code, 201)

    def test_get_incidents(self):
        incidents = self.get_flags()
        self.assertEqual(incidents.status_code, 200)


    def tearDown(self):

        with self.app.app_context():
            destroy_tables()
            self.db.close()


if __name__ == "__main__":
    unittest.main()