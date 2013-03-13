from google.appengine.ext import db

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