#!coding: utf-8

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from binascii import a2b_hex
import re
import os

ua_docomo   = re.compile(r'^DoCoMo')
ua_kddi     = re.compile(r'^KDDI|^UP.Browser')
ua_softbank = re.compile(r'^J-PHONE|^Vodafone|^SoftBank')

class BaseHandler(webapp.RequestHandler):
  def ua(self):
    return self.request.headers['user-agent']

  def is_docomo(self):
    return ua_docomo.match(self.ua())

  def is_softbank(self):
    return ua_softbank.match(self.ua())

  def is_kddi(self):
    return ua_kddi.match(self.ua())

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
   30:('F8BD', 'F68E', '1B2450540F'),   # 30:地下鉄
   31:('F8BE', 'F689', '1B24473F0F'),   # 31:新幹線
   32:('F8BF', 'F68A', '1B24473B0F'),   # 32:車（セダン）
   33:('F8C0', 'F68A', '1B24473B0F'),   # 33:車（RV）
   34:('F8C1', 'F688', '1B2445790F'),   # 34:バス
   35:('F8C2', 'F68D', '1B2446220F'),   # 35:船
   36:('F8C3', 'F68C', '1B24473D0F'),   # 36:飛行機
   37:('F8C4', 'F684', '1B2447560F'),   # 37:家
   38:('F8C5', 'F686', '1B2447580F'),   # 38:ビル
   39:('F8C6', 'F6F4', '1B2445730F'),   # 39:郵便局
   40:('F8C7', 'F758', '1B2445750F'),   # 40:病院
   41:('F8C8', 'F683', '1B24456D0F'),   # 41:銀行
   42:('F8C9', 'F67B', '1B2445740F'),   # 42:ATM
   43:('F8CA', 'F686', '1B2445780F'),   # 43:ホテル
   44:('F8CB', 'F67C', '1B2445760F'),   # 44:コンビニ
   45:('F8CC', 'F78E', '1B24475A0F'),   # 45:ガソリンスタンド
   46:('F8CD', 'F67E', '1B24456F0F'),   # 46:駐車場
   47:('F8CE', 'F642', '1B24456E0F'),   # 47:信号
   48:('F8CF', 'F67D', '1B2445590F'),   # 48:トイレ
   49:('F8D0', 'F685', '1B2447630F'),   # 49:レストラン
   50:('F8D1', 'F7B4', '1B2447650F'),   # 50:喫茶店
   51:('F8D2', 'F69B', '1B2447640F'),   # 51:バー
   52:('F8D3', 'F69C', '1B2447670F'),   # 52:ビール
   53:('F8D4', 'F6AF', '1B2445400F'),   # 53:ファーストフード
   54:('F8D5', 'F6E6', '1B24455E0F'),   # 54:ブティック
   55:('F8D6', 'F6EF', '1B24454E0F'),   # 55:美容院
   56:('F8D7', 'F6DC', '1B24475C0F'),   # 56:カラオケ
   57:('F8D8', 'F6F0', '1B24475D0F'),   # 57:映画
   58:('F8D9', 'F771', '1B2446560F'),   # 58:右斜め上
   59:('F8DA', 'F645', '1B2445440F'),   # 59:遊園地
   60:('F8DB', 'F6DE', '1B24475E0F'),   # 60:音楽
   61:('F8DC', 'F7B9', '1B2446250F'),   # 61:アート
   62:('F8DD', 'F66C', '1B2447240F'),   # 62:演劇
   63:('F8DE', 'F7BB', '1B2447570F'),   # 63:イベント
   64:('F8DF', 'F676', '1B2445450F'),   # 64:チケット
   65:('F8E0', 'F655', '1B24453D0F'),   # 65:喫煙
   66:('F8E1', 'F656', '1B2446280F'),   # 66:禁煙
   67:('F8E2', 'F6EE', '1B2447280F'),   # 67:カメラ
   68:('F8E3', 'F674', '1B24453E0F'),   # 68:カバン
   69:('F8E4', 'F782', '1B2445680F'),   # 69:本
   70:('F8E5', 'F7BC', '1B2445300F'),   # 70:リボン
   71:('F8E6', 'F6A8', '1B2445320F'),   # 71:プレゼント
   72:('F8E7', 'F7BD', '1B2447660F'),   # 72:バースデー
   73:('F8E8', 'F7B3', '1B2447290F'),   # 73:電話
   74:('F8E9', 'F7A5', '1B24472A0F'),   # 74:携帯電話
   75:('F8EA', 'F78B', '1B2445680F'),   # 75:メモ
   76:('F8EB', 'F6DB', '1B24454A0F'),   # 76:TV
   77:('F8EC', 'F69F', '1B24454B0F'),   # 77:ゲーム
   78:('F8ED', 'F6E5', '1B2445460F'),   # 78:CD
   79:('F8EE', 'F7B2', '1B24462C0F'),   # 79:ハート
   80:('F8EF', 'F7BE', '1B24462E0F'),   # 80:スペード
   81:('F8F0', 'F7BF', '1B24462D0F'),   # 81:ダイヤ
   82:('F8F1', 'F7C0', '1B24462F0F'),   # 82:クラブ
   83:('F8F2', 'F7C1', '1B2445250F'),   # 83:目
   84:('F8F3', 'F7C2', '1B2445610F'),   # 84:耳
   85:('F8F4', 'F6CC', '1B24472D0F'),   # 85:グー
   86:('F8F5', 'F7C3', '1B2447310F'),   # 86:チョキ
   87:('F8F6', 'F7C4', '1B2447320F'),   # 87:パー
   88:('F8F7', 'F769', '1B2446580F'),   # 88:右斜め下
   89:('F8F8', 'F768', '1B2446570F'),   # 89:左斜め上
   90:('F8F9', 'F6C7', '1B2446210F'),   # 90:足
   91:('F8FA', 'F6F3', '1B2447270F'),   # 91:くつ
   92:('F8FB', 'F6D7', '1B2446310F'),   # 92:眼鏡
   93:('F8FC', 'F657', '1B24462A0F'),   # 93:車椅子
   94:('F940', 'F7C5', '1B24476C0F'),   # 94:新月
   95:('F941', 'F7C6', '1B24476C0F'),   # 95:やや欠け月
   96:('F942', 'F7C7', '1B24476C0F'),   # 96:半月
   97:('F943', 'F65E', '1B24476C0F'),   # 97:三日月
   98:('F944', 'F661', '1B24476C0F'),   # 98:満月
   99:('F945', 'F6BA', '1B2447730F'),   # 99:犬
  100:('F946', 'F6B4', '1B2447700F'),   # 100:猫
  101:('F947', 'F6BB', '1B24473C0F'),   # 101:リゾート
  102:('F948', 'F6A2', '1B2447530F'),   # 102:クリスマス
  103:('F949', 'F772', '1B2446590F'),   # 103:左斜め下
  104:('F972', 'F6F7', '1B2445240F'),   # 104:phoneto
  105:('F973', 'F6FA', '1B2445230F'),   # 105:mailto
  106:('F974', 'F6F9', '1B24472B0F'),   # 106:faxto
  107:('F975', 'F65A', '1B2447690F'),   # 107:iモード
  108:('F976', 'F65A', '1B2447690F'),   # 108:iモード
  109:('F977', 'F7AE', '1B2445230F'),   # 109:メール
  110:('F978', 'F6B0', '1B2447690F'),   # 110:ドコモ提供
  111:('F979', 'F6B1', '1B2447690F'),   # 111:ドコモポイント
  112:('F97A', 'F79A', '1B2446350F'),   # 112:有料
  113:('F97B', 'F795', '1B2446360F'),   # 113:無料
  114:('F97C', 'F6C3', '1B2446490F'),   # 114:ID
  115:('F97D', 'F6F2', '1B24475F0F'),   # 115:パスワード
  116:('F97E', 'F779', '1B2446500F'),   # 116:次頁有
  117:('F980', 'F7C8', '1B2447690F'),   # 117:クリア
  118:('F981', 'F6F1', '1B2445340F'),   # 118:サーチ
  119:('F982', 'F7E5', '1B2446320F'),   # 119:NEW
  120:('F983', 'F78F', '1B24456B0F'),   # 120:位置情報
  121:('F984', 'F795', '1B2446310F'),   # 121:フリーダイヤル
  122:('F985', 'F7B3', '1B2446300F'),   # 122:シャープダイヤル
  123:('F986', 'F748', '1B2447690F'),   # 123:モバQ
  124:('F987', 'F6FB', '1B24463C0F'),   # 124:1
  125:('F988', 'F6FC', '1B24463D0F'),   # 125:2
  126:('F989', 'F740', '1B24463E0F'),   # 126:3
  127:('F98A', 'F741', '1B24463F0F'),   # 127:4
  128:('F98B', 'F742', '1B2446400F'),   # 128:5
  129:('F98C', 'F743', '1B2446410F'),   # 129:6
  130:('F98D', 'F744', '1B2446420F'),   # 130:7
  131:('F98E', 'F745', '1B2446430F'),   # 131:8
  132:('F98F', 'F746', '1B2446440F'),   # 132:9
  133:('F990', 'F7C9', '1B2446450F'),   # 133:0
  134:('F9B0', 'F7CA', '1B24466D0F'),   # 135:決定
  135:('F991', 'F6C3', '1B2447420F'),   # 135:黒ハート
  136:('F992', 'F7CC', '1B2447420F'),   # 136:揺れるハート
  137:('F993', 'F64F', '1B2447430F'),   # 137:失恋
  138:('F994', 'F650', '1B2447420F'),   # 138:ハート達
  139:('F995', 'F649', '1B2447770F'),   # 139:わーい
  140:('F996', 'F64A', '1B2447790F'),   # 140:ちっ
  141:('F997', 'F64B', '1B2447780F'),   # 141:がく〜
  142:('F998', 'F64C', '1B2445270F'),   # 142:もうやだ〜
  143:('F999', 'F7CB', '1B2445270F'),   # 143:ふらふら
  144:('F99A', 'F3EE', '1B2446560F'),   # 144:グッド
  145:('F99B', 'F7EE', '1B24475E0F'),   # 145:るんるん
  146:('F99C', 'F695', '1B2445430F'),   # 146:いい気分（温泉）
  147:('F99D', 'F6B0', '1B2446240F'),   # 147:かわいい
  148:('F99E', 'F6C4', '1B2447230F'),   # 148:キスマーク
  149:('F99F', 'F37E', '1B244F4E0F'),   # 149:ぴかぴか（新しい）
  150:('F9A0', 'F64E', '1B24452F0F'),   # 150:ひらめき
  151:('F9A1', 'F64A', '1B2446260F'),   # 151:むかっ（怒り）
  152:('F9A2', 'F6CC', '1B24472D0F'),   # 152:パンチ
  153:('F9A3', 'F652', '1B24453C0F'),   # 153:爆弾
  154:('F9A4', 'F65E', '1B24475E0F'),   # 154:ムード
  155:('F9A5', 'F75C', '1B2446580F'),   # 155:バッド
  156:('F9A6', 'F64D', '1B24455C0F'),   # 156:眠い（睡眠）
  157:('F9A7', 'F65A', '1B2447410F'),   # 157:exclamation
  158:('F9A8', 'F65B', '1B2447400F'),   # 158:exclamation&question
  159:('F9A9', 'F3F1', '1B2447410F'),   # 159:exclamation×2
  160:('F9AA', 'F7CD', '1B2446260F'),   # 160:どんっ（衝撃）
  161:('F9AB', 'F7CE', '1B2446390F'),   # 161:あせあせ（飛び散る汗）
  162:('F9AC', 'F6BF', '1B2445280F'),   # 162:たらーっ（汗）
  163:('F9AD', 'F6CD', '1B2445350F'),   # 163:ダッシュ（走り出す様）
  164:('F9AE', 'F74D', '1B2447690F'),   # 164:ー（長音記号1）
  165:('F9AF', 'F74E', '1B2447690F'),   # 165:ー（長音記号2）
  166:('F950', 'F697', '1B2445330F'),   # 166:カチンコ
  167:('F951', 'F6A0', '1B24454F0F'),   # 167:袋
  168:('F952', 'F679', '1B2445680F'),   # 168:ペン
  169:('F955', 'F6D4', '1B2447210F'),   # 169:人影
  170:('F956', 'F657', '1B24453F0F'),   # 170:椅子
  171:('F957', 'F640', '1B2445660F'),   # 171:夜
  172:('F95B', 'F778', '1B2446510F'),   # 172:soon
  173:('F95C', 'F6E8', '1B24465A0F'),   # 173:on
  174:('F95D', 'F779', '1B2446500F'),   # 174:end
  175:('F95E', 'F7B1', '1B24474D0F')    # 175:時計
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
