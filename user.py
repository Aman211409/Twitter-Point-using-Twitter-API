from database import CursorFromConnectionFromPool
import oauth2
from twiiter_utils import consumer
import json


class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.screen_name)

    # saving to database from python

    def save_to_db(self):  # self is the currently bound object
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users (screen_name, oauth_token, oauth_token_secret) values (%s, %s, %s)',
                           (self.screen_name, self.oauth_token, self.oauth_token_secret))

    # loading from database

    @classmethod
    def load_from_db(cls, screen_name):  # cls is the currently bound class, therefore cls is user
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from users where screen_name = %s', (screen_name,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(user_data[1], user_data[2], user_data[3], user_data[0])

    def twitter_request(self, uri, verb):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # make twitter api calls
        response, content = authorized_client.request(uri, verb)
        if response.status != 200:
            print("An error occurred when searching!")

        return json.loads(content.decode('utf-8'))
