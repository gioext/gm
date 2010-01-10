import logging
import sys
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.__dispatch("get")

  def post(self):
    self.__dispatch("post")

  def head(self):
    self.__bad_method()

  def put(self):
    self.__bad_method()

  def delete(self):
    self.__bad_method()

  def __bad_method(self):
    self.response.out.write("This application does not support (head|put|delete) methods.")

  def __error(self):
    self.error(500)
    self.response.out.write('500 Internal Server Error')

  def __dispatch(self, method):
    route = self.__route(self.request.path)
    controller = "%sController" % (route['module'].capitalize())
    try:
      exec("from app.controllers.%s import %s" % (route['module'], controller))
      clazz = eval(controller)
      c = clazz(self)
      action = getattr(c, "%s_%s" % (method, route['action']), None)
      c.before_filter()
      action()
      c.after_filter()
      html = os.path.join(os.path.dirname(__file__), 'app/templates', route['module'], route['action'] + '.html')
      values = c.__dict__
      c.render(html, values)
    except Exception, e:
      logging.error(e)
      self.__error()

  def __route(self, url):
    """ fixme """
    split_url = url.split('/')
    split_url.pop(0)
    module = action = ''
    try:
      module = split_url.pop(0)
      action = split_url.pop(0)
    except:
      pass
    module = module or 'top'
    action = action or 'index'
    logging.info("Run module:%s action:%s" % (module, action))
    return { 'module': module, 'action': action } 

app = webapp.WSGIApplication([(r'.*', MainHandler)], debug=True)

def main():
  dirname = os.path.dirname(__file__)
  sys.path.append(dirname)
  run_wsgi_app(app)

if __name__ == '__main__':
  main()
