#!coding: utf-8

from google.appengine.api import memcache
from google.appengine.ext.webapp import template
import os, re, md5, logging
import emoji

csrf_secret = "aoiueo"
ua_docomo   = re.compile(r'^DoCoMo')
ua_ezweb    = re.compile(r'^KDDI|^UP.Browser')
ua_softbank = re.compile(r'^J-PHONE|^Vodafone|^SoftBank')

""" redirece exception """
class RedirectException(Exception):
  pass

""" Mobile Base Controller """
class BaseController:
  def __init__(self, handler, module, action):
    self.handler = handler
    self.user_agent = handler.request.headers['user-agent']
    self.is_docomo = ua_docomo.match(self.user_agent)
    self.is_softbank = ua_softbank.match(self.user_agent)
    self.is_ezweb = ua_ezweb.match(self.user_agent)
    self.request = handler.request
    self.response = self.handler.response
    self.module = module
    self.action = action

  def before_filter(self):
    if self.request.method == "GET":
      self.ipblock()
      self.guid()
      self.required_uid()
      self.regist()
    elif self.request.method == "POST":
      self.ipblock()
      self.required_uid()
      self.regist()
      self.check_csrf()
      if self.is_ezweb:
        self.request.charset = "ms932"

  def after_filter(self):
    if self.request.method == "GET":
      pass
    elif self.request.method == "POST":
      pass

  def render(self, path, values):
    html = template.render(path, values)
    if self.is_docomo:
      content_type = 'application/xhtml+xml; charset=UTF-8'
    elif self.is_ezweb:
      content_type = 'text/html; charset=Shift-JIS'
      html = unicode(html, 'utf-8').encode('ms932')
    else:
      content_type = 'text/html; charset=UTF-8'
    html = emoji.encode(self, html)
    html = self.replace_guid(html)
    self.response.headers['Content-Type'] = content_type
    self.response.out.write(html)

  def redirect(self, url):
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

  def check_csrf(self):
    token = self.request.get('csrf')
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

  def param(self, key):
    return self.request.get(key)

  def emoji_param(self, key):
    v = self.param(key)
    return emoji.decode(self, v)

  """ filter """
  def replace_guid(self, str):
    if self.is_docomo:
      regex = r'(action|href)="/(.*?)"'
      return re.sub(regex, repl_guidurl, str)
    return str

  def ipblock(self):
    pass

  def guid(self):
    """ fixme path """
    if self.is_docomo and self.request.get('guid') != 'ON':
      self.redirect(self.request.path)

  def required_uid(self):
    if self.module == 'top':
      return
    if not self.mobile_id():
      self.redirect('/') # fixme

  def regist(self):
    pass
    #if self.request.path.find('/regist') == -1:
    #  if not model.User.all().filter('id =', self.mobile_id()).fetch(1): # fixme:memcached
    #    self.redirect('/regist/index')

  """ opensocial """
  def user_id(self):
    user = model.User.all().filter('id =', self.mobile_id()).fetch(1)
    if user:
      return user[0]
    else:
      return None

  def user_name(self):
    pass

  def avaurl(self):
    return 'http://img.mixi.jp/img/basic/common/noimage_member76.gif'

def repl_guidurl(g):
  tag = g.group(1)
  url = g.group(2)
  if url.find('?') == -1:
    s = '?'
  else:
    s = '&'
  return '%s="/%s%s%s"' % (tag, url, s, 'guid=ON')
