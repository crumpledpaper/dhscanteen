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
  reference = db.ReferenceProperty(Food)


def stall_key(stall_name=None):
  """Constructs a Datastore key for a stall entity with stall_name."""
  return db.Key.from_path('Stall', stall_name or 'default_stall')


class MainPage(webapp2.RequestHandler):
    def get(self):
        stall_name=self.request.get('stall_name')
        reviews_query = Review.all().ancestor(
            stall_key(stall_name)).order('-date')
        reviews = reviews_query.run(limit=10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
        template_values = {
            'reviews': reviews,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


class Stall(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'review' to ensure each review is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    stall_name = self.request.get('stall_name')
    review = Review(parent=stall_key(stall_name))

    if users.get_current_user():
      review.author = users.get_current_user().nickname()
    review.content = self.request.get('content')
    review.put()
    self.redirect('/?' + urllib.urlencode({'stall_name': stall_name}))
  
	

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/review', Stall)],
                              debug=True)
