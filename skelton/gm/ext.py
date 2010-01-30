#!coding: utf-8

from google.appengine.api import memcache
from google.appengine.ext.webapp import template
import os
import re
import md5
import logging
import urllib
import emoji
import app.models

csrf_secret = "aoiueo"
ua_docomo   = re.compile(r'^DoCoMo')
ua_ezweb    = re.compile(r'^KDDI|^UP.Browser')
ua_softbank = re.compile(r'^J-PHONE|^Vodafone|^SoftBank')

class RedirectException(Exception):
  pass
class CsrfException(Exception):
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
    #self.my_os = OpenSocial(self.owner_id())

  def before_filter(self):
    #Filter.authorization(self)
    #Filter.regist(self)
    Filter.request_charset(self)

  def after_filter(self):
    pass

  def render(self, path, values):
    html = template.render(path, values)
    html = Filter.output(self, html)
    html = Filter.emoji(self, html)
    #html = Filter.replace_url(self, html)
    self.response.out.write(html)

  def redirect(self, url):
    guid = ''
    if self.is_docomo:
      s = '&'
      if url.find('?') == -1:
        s = '?'
      guid = s + 'guid=ON'

    self.handler.redirect(url + guid)
    raise RedirectException('redirect to %s' % (url))

  def header(self, name):
    if self.request.headers.has_key(name):
      return self.request.headers[name]
    return None

  def param(self, key):
    return self.request.get(key)

  def emoji_param(self, key):
    v = self.param(key)
    return emoji.decode(self, v)

  def app_id(self):
    return self.param('opensocial_app_id')

  def owner_id(self):
    return self.param('opensocial_owner_id')

  def user(self):
    return app.models.User.get_by_owner_id(self.owner_id())


#TODO
class OpenSocial(object):
  def __init__(self, id):
    if not id:
      raise Exception("Error opensocial_owner_id")
    self.id = id

  def get_name(self):
    return 'Giox'

  def get_person(self):
    return { 'name': u'Giox', 'avaurl': 'http://img.mixi.jp/img/basic/common/noimage_member76.gif' }

  def get_avaurl(self):
    return 'http://img.mixi.jp/img/basic/common/noimage_member40.gif'

  def get_friend(self):
    return []


class Filter(object):
#TODO
  """
  正当なリクエストかSignatureをチェックする
  不正の場合は/top/invalidへredirect
  """
  @classmethod
  def authorization(cls, handler):
    if (handler.module == 'top' and handler.action == 'invalid'):
      return
    
#TODO
  """
  アプリに登録済みかチェックする
  未登録の場合は/registへredirect
  """
  @classmethod
  def regist(cls, handler):
    pass

  """
  AUの場合はms932でリクエストされる
  """
  @classmethod
  def request_charset(cls, handler):
    if handler.request.method == "POST" and handler.is_ezweb:
      handler.request.charset = "ms932"

  """
  ?guid=ON&url=http://...の形にreplace
  """
  @classmethod
  def replace_url(cls, handler, str):
    def f(g):
      tag = g.group(1)
      url = handler.request.host_url + '/' +  g.group(2)
      return '%s="/?guid=ON&url=%s"' % (tag, urllib.quote(url))
    return re.sub(r'(action|href)="/(.*?)"', f, str)

  """
  encodingとcontent-typeを設定
  """
  @classmethod
  def output(cls, handler, html):
    if handler.is_docomo:
      content_type = 'application/xhtml+xml; charset=UTF-8'
    elif handler.is_ezweb:
      content_type = 'text/html; charset=Shift-JIS'
      html = unicode(html, 'utf-8').encode('ms932')
    else:
      content_type = 'text/html; charset=UTF-8'
    handler.response.headers['Content-Type'] = content_type
    return html

  """
  絵文字変換
  """
  @classmethod
  def emoji(cls, handler, html):
    return emoji.encode(handler, html)
