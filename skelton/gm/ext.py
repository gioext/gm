#!coding: utf-8

from google.appengine.api import memcache
from google.appengine.ext.webapp import template
import os, re, md5, logging
import emoji

csrf_secret = "aoiueo"
ua_docomo   = re.compile(r'^DoCoMo')
ua_ezweb    = re.compile(r'^KDDI|^UP.Browser')
ua_softbank = re.compile(r'^J-PHONE|^Vodafone|^SoftBank')

""" Mobile Base Controller """
class BaseController:
  def __init__(self, handler):
    self.handler = handler
    self.user_agent = handler.request.headers['user-agent']
    self.is_docomo = ua_docomo.match(self.user_agent)
    self.is_softbank = ua_softbank.match(self.user_agent)
    self.is_ezweb = ua_ezweb.match(self.user_agent)
    self.request = handler.request
    self.response = self.handler.response

  def before_filter(self):
    if self.request.method == "GET":
      pass
    elif self.request.method == "POST":
      if self.is_ezweb:
        self.request.charset = "ms932"

  def after_filter(self):
    if self.request.method == "GET":
      pass
    elif self.request.method == "POST":
      pass

  def render(self, path, values):
    """ make html """
    html = template.render(path, values)

    """ set content type & encode html"""
    if self.is_docomo:
      content_type = 'application/xhtml+xml; charset=UTF-8'
    elif self.is_ezweb:
      content_type = 'text/html; charset=Shift-JIS'
      html = unicode(html, 'utf-8').encode('ms932')
    else:
      content_type = 'text/html; charset=UTF-8'

    """ emoji """
    html = emoji.encode(html, self)

    """ output """
    self.response.headers['Content-Type'] = content_type
    self.response.out.write(html)

  def halt_redirect(self, url):
    guid = ''
    if self.is_docomo:
      s = '&'
      if url.find('?') == -1:
        s = '?'
      guid = s + 'guid=ON'

    self.handler.redirect(url + guid)
    raise RedirectException

  def attr_key(self, key):
    return "attr:" + key

  def attr_read(self, key):
    return memcache.get(self.attr_key(key))

  def attr_write(self, key, value):
    return memcache.set(self.attr_key(key), value)

  def csrf_token(self):
    return md5.new(csrf_secret + self.mobile_id()).hexdigest();

  def check_csrf(self, token):
    if token != self.csrf_token():
      raise "invalid csrf"

  def header(self, name):
    if self.request.headers.has_key(name):
      return self.request.headers[name]
    return None

  def mobile_id(self):
    if self.is_docomo:
      return self.header('x-dcmguid')
    elif self.is_ezweb:
      return self.header('x-up-subno')
    elif self.is_softbank:
      return self.header('x-jphone-uid')
    return ''


def replace_guid(handler, str):
  if handler.is_docomo:
    regex = r'(action|href)="/(.+?)"'
    return re.sub(regex, guidurl, str)
  return str

def guidurl(g):
  tag = g.group(1)
  url = g.group(2)
  if url.find('?') == -1:
    s = '?'
  else:
    s = '&'
  return '%s="/%s%s%s"' % (tag, url, s, 'guid=ON')
