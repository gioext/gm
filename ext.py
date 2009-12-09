#!coding: utf-8

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from binascii import a2b_hex
import re
import os

class BaseHandler(webapp.RequestHandler):
  def user_agent(self):
    return self.request.headers['user-agent']

  def is_docomo(self):
    return self.user_agent().startswith('DoCoMo')

  def is_softbank(self):
    return self.user_agent().startswith('SoftBank')

  def is_kddi(self):
    return self.user_agent().startswith('KDDI')

  def enable_cookie(self):
    pass

  def encode_emoji(self, str):
    pattern = "\$([0-9]+)\$"
    if (self.is_docomo()):
      return re.sub(pattern, repl_docomo, str)
    elif (self.is_kddi()):
      return re.sub(pattern, repl_kddi, str)
    elif (self.is_softbank()):
      return re.sub(pattern, repl_softbank, str)
    return re.sub(pattern, '', str)

  def render(self, tpl, values):
    path = os.path.join(os.path.dirname(__file__), "../views/", tpl)
    content_type = 'text/html; charset=Shift-JIS'
    if (self.is_docomo()):
      content_type = 'application/xhtml+xml; charset=Shift-JIS'
    self.response.headers['Content-Type'] = content_type

    body = unicode(template.render(path, values), 'utf-8').encode('ms932')
    self.response.out.write(self.encode_emoji(body))

emoji_tbl = {
   0:('F89F', 'F660', '1B24476A0F'),   # 0:晴れ
   1:('F8A0', 'F665', '1B2447690F'),   # 1:曇り
   2:('F8A1', 'F664', '1B24476B0F'),   # 2:雨
   3:('F8A2', 'F65D', '1B2447680F'),   # 3:雪
   4:('F8A3', 'F65F', '1B24455D0F'),   # 4:雷
   5:('F8A4', 'F641', '1B24476B0F'),   # 5:台風
   6:('F8A5', 'F7B5', '1B2447690F'),   # 6:霧
   7:('F8A6', 'F6BF', '1B24476B0F'),   # 7:小雨
   8:('F8A7', 'F667', '1B24465F0F'),   # 8:牡羊座
   9:('F8A8', 'F668', '1B2446600F'),   # 9:牡牛座
  10:('F8A9', 'F669', '1B2446610F'),   # 10:双子座
  11:('F8AA', 'F66A', '1B2446620F'),   # 11:蟹座
  12:('F8AB', 'F66B', '1B2446630F'),   # 12:獅子座
  13:('F8AC', 'F66C', '1B2446640F'),   # 13:乙女座
  14:('F8AD', 'F66D', '1B2446650F'),   # 14:天秤座
  15:('F8AE', 'F66E', '1B2446660F'),   # 15:蠍座
  16:('F8AF', 'F66F', '1B2446670F'),   # 16:射手座
  17:('F8B0', 'F670', '1B2446680F'),   # 17:山羊座
  18:('F8B1', 'F671', '1B2446690F'),   # 18:水瓶座
  19:('F8B2', 'F672', '1B24466A0F'),   # 19:魚座
  20:('F8B3', 'F643', '1B2447260F'),   # 20:スポーツ
  21:('F8B4', 'F693', '1B2447360F'),   # 21:野球
  22:('F8B5', 'F7B6', '1B2447340F'),   # 22:ゴルフ
  23:('F8B6', 'F690', '1B2447350F'),   # 23:テニス
  24:('F8B7', 'F68F', '1B2447380F'),   # 24:サッカー
  25:('F8B8', 'F691', '1B2447330F'),   # 25:スキー
  26:('F8B9', 'F7B7', '1B2445510F'),   # 26:バスケットボール
  27:('F8BA', 'F692', '1B2445520F'),   # 27:モータースポーツ
  28:('F8BB', 'F7B8', '1B24456E0F'),   # 28:ポケットベル
  29:('F8BC', 'F68E', '1B24473E0F'),   # 29:電車
  30:('F8BD', 'F68E', '1B2450540F')    # 30:地下鉄
}

def repl_docomo(a):
  e = emoji_tbl[int(a.group(1))]
  return a2b_hex(e[0])

def repl_kddi(a):
  e = emoji_tbl[int(a.group(1))]
  return a2b_hex(e[1])

def repl_softbank(a):
  e = emoji_tbl[int(a.group(1))]
  return a2b_hex(e[2])
