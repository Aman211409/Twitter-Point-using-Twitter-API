from user import User
from database import Database
from twiiter_utils import get_request_token, get_oauth_token, get_access_token


Database.initialise(user='postgres', host='localhost', password='211409', database='learning')

user_email = input("Enter your email address: ")
user = User.load_from_db(user_email)

if not user:

    # get the request token parsing the query string returned
    request_token = get_request_token()
    oauth_verifier = get_oauth_token(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    first = input("Input your first name: ")
    last = input("Input your last name: ")

    user = User(user_email, first, last, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

# create an authorized token Token object and use that to perform twitter API calls
tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')

for tweet in tweets['statuses']:
    print(tweet['text'])

# this was a horrible code, not now
