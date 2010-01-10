#!coding: utf-8

from google.appengine.ext.webapp import template
import os
import re
import helper
import emoji

ua_docomo   = re.compile(r'^DoCoMo')
ua_ezweb     = re.compile(r'^KDDI|^UP.Browser')
ua_softbank = re.compile(r'^J-PHONE|^Vodafone|^SoftBank')

class BaseController:
  def __init__(self, handler):
    self.handler = handler

  def before_filter(self):
    pass

  def after_filter(self):
    pass

  def render(self, path, values):
    """ make html """
    values['helper'] = helper
    html = template.render(path, values)

    """ set content type & encode html"""
    if (self.is_docomo()):
      content_type = 'application/xhtml+xml; charset=UTF-8'
    elif (self.is_ezweb()):
      content_type = 'text/html; charset=Shift-JIS'
      html = unicode(html, 'utf-8').encode('ms932')
    else:
      content_type = 'text/html; charset=UTF-8'

    """ emoji """
    html = emoji.encode(html, self)

    """ output """
    self.handler.response.headers['Content-Type'] = content_type
    self.handler.response.out.write(html)

  def header(self, name):
    if self.handler.request.headers.has_key(name):
      return self.handler.request.headers[name]
    return None

  def ua(self):
    return self.header('user-agent')

  def mobile_id(self):
    if (self.is_docomo()):
      return self.header('x-dcmguid')
    elif(self.is_ezweb()):
      return self.header('x-up-subno')
    elif (self.is_softbank()):
      return self.header('x-jphone-uid')
    return ''

  def is_docomo(self):
    return ua_docomo.match(self.ua())

  def is_softbank(self):
    return ua_softbank.match(self.ua())

  def is_ezweb(self):
    return ua_ezweb.match(self.ua())


def replace_guid(handler, str):
  if handler.is_docomo():
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
