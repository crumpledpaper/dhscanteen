import cgi
import datetime
import urllib
import webapp2
import jinja2
import os


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))

from models import Food, Review
from google.appengine.ext import db
from google.appengine.api import users

def stall_key(stall_name=None):
  """Constructs a Datastore key for a stall entity with stall_name."""
  return db.Key.from_path('Stall', stall_name or 'default_stall')

def food_key(food_name=None):
  return db.Key.from_path('NewFood', food_name or 'default_food')
  
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))
  
class MainPage(BaseHandler):
    def get(self):
        stall_name=self.request.get('stall_name')
        food_query = Food.all().ancestor(
            stall_key(stall_name)).order('-name')
        food = food_query.run()

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        self.render_template('index.html',{
            'food': food,
            'url': url,
            'url_linktext': url_linktext,
        })


class Stall(BaseHandler):
  def post(self):
    # We set the same parent key on the 'review' to ensure each review is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    food_name = self.request.get('stall_name')
    review = Review(parent=stall_key(stall_name),
					content = self.request.get('content'))

    if users.get_current_user():
      author = users.get_current_user().nickname()
    
    review.put()
    self.redirect('/?' + urllib.urlencode({'stall_name': stall_name}))

class Newfood(BaseHandler):
  def post(self):
    food_name = self.request.get('food_name')
	food = Food(parent=food_key(food_name),
				food.price = self.request.get('price'),
				food.picture = )

	food.put()
	self.redirect('/?' + urllib.urlencode({'food_name': food_name}))
