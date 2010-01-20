#!coding: utf-8

from google.appengine.ext import db

""" key_name: opensocial_owner_id """
class User(db.Model):
  updated_at  = db.DateTimeProperty(auto_now=True)
  created_at  = db.DateTimeProperty(auto_now_add=True)
