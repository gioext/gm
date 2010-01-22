#!coding: utf-8

from google.appengine.api import memcache
from google.appengine.ext.webapp import template
import os
import re
import md5
import logging
import emoji

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

  def before_filter(self):
    self.ipblock()
    self.authorization()
    self.regist()
    if self.request.method == "POST":
      self.check_csrf()
      if self.is_ezweb:
        self.request.charset = "ms932"

  def after_filter(self):
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
    raise RedirectException('redirect to %s' % (url))

  def attr_key(self, key):
    return "attr:" + key

  def attr_read(self, key):
    return memcache.get(self.attr_key(key))

  def attr_write(self, key, value):
    return memcache.set(self.attr_key(key), value)

  def csrf_token(self):
    return md5.new(csrf_secret + self.owner_id()).hexdigest();

  def check_csrf(self):
    token = self.request.get('csrf')
    if token != self.csrf_token():
      raise CsrfException("invalid csrf")

  def header(self, name):
    if self.request.headers.has_key(name):
      return self.request.headers[name]
    return None

  def param(self, key):
    return self.request.get(key)

  def emoji_param(self, key):
    v = self.param(key)
    return emoji.decode(self, v)

  """
  DoCoMoの場合リンクとフォームのURLにguid=ONをつける
  """
  def replace_guid(self, str):
    if self.is_docomo:
      def repl_guidurl(g):
        tag = g.group(1)
        url = g.group(2)
        if url.find('?') == -1:
          s = '?'
        else:
          s = '&'
        return '%s="/%s%s%s"' % (tag, url, s, 'guid=ON')
      return re.sub(r'(action|href)="/(.*?)"', repl_guidurl, str)
    return str

  """
  IP制限
  """
  def ipblock(self):
    pass

  """
  アプリに登録済みかチェックする
  未登録の場合は/registへredirect
  """
  def regist(self):
    pass

  """
  正当なリクエストかSignatureをチェックする
  不正の場合は/top/brへredirect
  """
  def authorization(self):
    if (self.module == 'top' and self.action == 'invalid'):
      return
    #self.redirect('/top/invalid')

  """
  Open social owner id
  """
  def owner_id(self):
    return 1234

  def my_person(self):
    return { 'name': u'Giox', 'avaurl': 'http://img.mixi.jp/img/basic/common/noimage_member76.gif' }

  def my_friend(self):
    return []

