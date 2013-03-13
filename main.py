import webapp2
from views import MainPage, Stall, Newfood 
	

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/#review', Stall),
							   ('/#newfood', Newfood)
							   ],
                              debug=True)
