#!coding: utf-8

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import re
import os
import emoji

ua_docomo   = re.compile(r'^DoCoMo')
ua_kddi     = re.compile(r'^KDDI|^UP.Browser')
ua_softbank = re.compile(r'^J-PHONE|^Vodafone|^SoftBank')

class BaseHandler(webapp.RequestHandler):
  def header(self, name):
    if self.request.headers.has_key(name):
      return self.request.headers[name]
    return None

  def ua(self):
    return self.header('user-agent')

  def is_docomo(self):
    return ua_docomo.match(self.ua())

  def is_softbank(self):
    return ua_softbank.match(self.ua())

  def is_kddi(self):
    return ua_kddi.match(self.ua())

  def enable_cookie(self):
    pass

  def mobile_id(self):
    if (self.is_docomo()):
      return self.header('x-dcmguid')
    elif(self.is_kddi()):
      return self.header('x-up-subno')
    elif (self.is_softbank()):
      return self.header('x-jphone-uid')
    return ''

  def encode_emoji(self, str):
    pattern = "\$([0-9]+)\$"
    if (self.is_docomo()):
      return re.sub(pattern, emoji.repl_docomo, str)
    elif (self.is_kddi()):
      return re.sub(pattern, emoji.repl_kddi, str)
    elif (self.is_softbank()):
      return re.sub(pattern, emoji.repl_softbank, str)
    return re.sub(pattern, '', str)

  def set_mobile_content_type(self):
    content_type = 'text/html; charset=Shift-JIS'
    if (self.is_docomo()):
      content_type = 'application/xhtml+xml; charset=Shift-JIS'
    self.response.headers['Content-Type'] = content_type

  def render(self, tpl, values):
    self.set_mobile_content_type()
    path = os.path.join(os.path.dirname(__file__), "../views/", tpl)
    body = unicode(template.render(path, values), 'utf-8').encode('ms932')
    self.response.out.write(self.encode_emoji(body))

