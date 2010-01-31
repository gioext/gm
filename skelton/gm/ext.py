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
class AuthException(Exception):
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
    self._owner_id = handler.request.get('opensocial_owner_id')
    self._app_id = handler.request.get('opensocial_app_id')

  def before_filter(self):
    Filter.authorization(self)
    Filter.regist(self)
    Filter.request_charset(self)

  def render(self, path, values):
    html = template.render(path, values)
    html = Filter.output(self, html)
    html = Filter.encode_emoji(self, html)
    html = Filter.replace_url(self, html)
    self.response.out.write(html)

#TODO
  def redirect(self, url):
    self.handler.redirect(url)
    raise RedirectException('redirect to %s' % (url))


#TODO
class OpenSocial(object):
  def __init__(self, id):
    self.id = id
    if not self.id:
      raise Exception("Error opensocial_owner_id")

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
  """
  @classmethod
  def authorization(cls, handler):
    if handler.module == 'top' and handler.action == 'invalid':
      return
    if not handler.request.headers.has_key('authorization'):
      raise AuthException("No authorization signature.")
    logging.info("Authorization Signature: " + handler.request.headers['authorization'])

#TODO:cache
  """
  アプリに登録済みかチェックする
  未登録の場合は/registへredirect
  """
  @classmethod
  def regist(cls, handler):
    return
    user = app.models.User.get_by_owner_id(handler._owner_id)
    if handler.module != 'regist' and not user:
      handler.redirect('/regist')

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
      return '%s="?guid=ON&url=%s"' % (tag, urllib.quote(url))
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
  def encode_emoji(cls, handler, html):
    return emoji.encode(handler, html)

  """
  絵文字逆変換
  """
  @classmethod
  def decode_emoji(cls, handler, html):
    return emoji.decode(handler, html)
