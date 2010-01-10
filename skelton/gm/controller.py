#!coding: utf-8

from google.appengine.ext.webapp import template
import os
import re
import helper

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
    values['helper'] = helper
    body = template.render(path, values)
    self.handler.response.out.write(body)

  #
  # for mobile
  #

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
