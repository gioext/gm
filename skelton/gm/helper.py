#!coding: utf-8

from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def hr(size, arg = '666666'):
  return '<hr style="color:#%s;background:#%s;height:%dpx;border:0px solid #%s;margin:0.3em 0;" size="%d" />' % (arg, arg, size, arg, size)

def space(height):
  return '<div><img src="http://mm.mixi.net/img/dot0.gif" width="1" height="%d" /></div>' % (height)

def header(str):
  return '<div style="background-color:#006600;color:#ffffff;text-align:center">$249$%s$249$</div>' % (str)

register.filter(hr)
register.filter(space)
register.filter(header)
