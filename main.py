import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import db
from google.appengine.api import users

class Food(db.Model):
  day = db.IntegerProperty()
  name = db.StringProperty()
  picture = db.BlobProperty()
  price = db.FloatProperty()
  rating = db.IntegerProperty()
  
class Review(db.Model):
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  rating = db.IntegerProperty()


def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name=self.request.get('guestbook_name')
        reviews_query = Review.all().ancestor(
            guestbook_key(guestbook_name)).order('-date')
        reviews = reviews_query.run(limit=10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'reviews': reviews,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'review' to ensure each review is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name')
    review = Review(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      review.author = users.get_current_user().nickname()
    review.content = self.request.get('content')
    review.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook)],
                              debug=True)
