#!/usr/bin/env python
# coding=sjis
# ktip2carrier.py
# Copyright (c) 2009 Kanda.Motohiro@gmail.com
import re
# http://pypi.python.org/pypi/IPy/0.62 からもってくる。
from IPy import IP

if __debug__:
    def dbgprint(*args):
        """ 実行中のファイル名、行番号、関数名と、 args を表示する。
        Cookbook より。"""
        import logging
        import traceback
        import os
        items = list(traceback.extract_stack()[-2][:3])
        items[0] = os.path.basename(items[0])
        logging.info(str(items) + str(args))
else:
    def dbgprint(*args): pass

class Ip2carrier(object):

    """
ke-tai.org で公開されている、日本の携帯電話キャリアのＩＰアドレス一覧表
をもとに、指定されたＩＰｖ４アドレスが属するキャリアと、ＣＩＤＲ、更新日付
を返す。キャリア名は、英小文字で表す。

>>> i2c = Ip2carrier()
>>>
>>> i2c.lookup('192.168.1.123')
(None, None, None)
>>> i2c.lookup('210.153.84.20')
('docomo', '210.153.84.0/24', '2008/06/20')
>>> i2c.lookup('124.146.175.200')
('docomo', '124.146.175.0/24', '2008/06/20')
>>> i2c.lookup('210.230.128.225')
('au', '210.230.128.224/28', '2009/03/10')
>>> i2c.lookup('219.108.157.30')
('au', '219.108.157.0/25', '2009/03/10')
>>> i2c.lookup('123.108.236.254')
('softbank', '123.108.236.0/24', '2008/02/29')
>>> i2c.lookup('211.8.159.150')
('softbank', '211.8.159.128/25', '2008/02/29')
>>> i2c.lookup('61.198.142.77')
('willcom', '61.198.142.0/24', '2009/03/19')
>>> i2c.lookup('61.204.4.200')
('willcom', '61.204.4.0/24', '2009/03/19')
>>> i2c.lookup('117.55.1.250')
('emobile', '117.55.1.224/27', '2008/02/26')
>>> i2c.lookup('1.2.3.4')
(None, None, None)
>>> i2c.lookup('Hello World')
(None, None, None)
>>> i2c.lookup('9999')
(None, None, None)
>>> i2c.lookup('')
(None, None, None)
"""
# ２００９年３月時点の、キャリアＩＰアドレス表
    addressList200903 = """
# Mobile IP Address Blocking
# last update 2009/03/23
# ----------------------

Order Deny,Allow
Deny from all


# ----------------------
# Carrier
# ----------------------

# docomo (http://www.nttdocomo.co.jp/service/imode/make/content/ip/)
# 2008/06/20
Allow from 210.153.84.0/24 210.136.161.0/24 210.153.86.0/24 124.146.174.0/24 124.146.175.0/24

# au (http://www.au.kddi.com/ezfactory/tec/spec/ezsava_ip.html)
# 2009/03/10
Allow from 210.230.128.224/28 121.111.227.160/27 61.117.1.0/28 219.108.158.0/27 219.125.146.0/28 61.117.2.32/29 61.117.2.40/29 219.108.158.40/29 219.125.148.0/25 222.5.63.0/25 222.5.63.128/25 222.5.62.128/25 59.135.38.128/25 219.108.157.0/25 219.125.145.0/25 121.111.231.0/25 121.111.227.0/25 118.152.214.192/26 118.159.131.0/25 118.159.133.0/25

# SoftBank (http://creation.mb.softbank.jp/web/web_ip.html)
# 2008/02/29
Allow from 123.108.236.0/24 123.108.237.0/27 202.179.204.0/24 202.253.96.224/27 210.146.7.192/26 210.146.60.192/26 210.151.9.128/26 210.169.130.112/28 210.175.1.128/25 210.228.189.0/24 211.8.159.128/25

# Willcom (http://www.willcom-inc.com/ja/service/contents_service/club_air_edge/for_phone/ip/)
# 2009/03/19
Allow from 61.198.142.0/24 219.108.14.0/24 61.198.161.0/24 61.198.249.0/24 61.198.250.0/24 61.198.253.0/24 61.198.254.0/24 219.108.4.0/24 61.198.255.0/24 219.108.5.0/24 61.204.3.0/25 219.108.6.0/24 61.204.4.0/24 221.119.0.0/24 61.204.6.0/25 221.119.1.0/24 125.28.4.0/24 221.119.2.0/24 125.28.5.0/24 221.119.3.0/24 125.28.6.0/24 221.119.4.0/24 125.28.7.0/24 221.119.5.0/24 125.28.8.0/24 221.119.6.0/24 211.18.235.0/24 221.119.7.0/24 211.18.238.0/24 221.119.8.0/24 211.18.239.0/24 221.119.9.0/24 125.28.11.0/24 125.28.13.0/24 125.28.12.0/24 125.28.14.0/24 125.28.2.0/24 125.28.3.0/24 211.18.232.0/24 211.18.233.0/24 211.18.236.0/24 211.18.237.0/24 125.28.0.0/24 125.28.1.0/24 61.204.0.0/24 210.168.246.0/24 210.168.247.0/24 219.108.7.0/24 61.204.2.0/24 61.204.5.0/24 61.198.129.0/24 61.198.140.0/24 61.198.141.0/24 125.28.15.0/24 61.198.165.0/24 61.198.166.0/24 61.198.168.0/24 61.198.169.0/24 61.198.170.0/24 61.198.248.0/24 125.28.16.0/24 125.28.17.0/24 211.18.234.0/24 219.108.8.0/24 219.108.9.0/24 219.108.10.0/24 61.198.138.100/32 61.198.138.101/32 61.198.138.102/32 61.198.139.160/28 61.198.139.128/27 61.198.138.103/32 61.198.139.0/29 219.108.15.0/24 61.198.130.0/24 61.198.163.0/24 61.204.6.128/25 61.204.7.0/25 61.204.92.0/24 61.204.93.0/24 61.204.94.0/24 61.204.95.0/24 61.198.128.0/24 61.198.131.0/24 61.198.143.0/24 61.198.172.0/24 61.198.173.0/24 61.198.252.0/24 61.204.3.128/25 211.126.192.128/25 219.108.11.0/24 219.108.12.0/24 219.108.13.0/24 61.198.132.0/24 61.198.133.0/24 61.198.134.0/24 61.198.135.0/24 61.198.136.0/24 61.198.137.0/24 61.198.160.0/24 61.198.162.0/24 61.198.164.0/24 61.198.171.0/24 61.198.174.0/24 61.198.175.0/24 61.198.251.0/24 210.169.92.0/24 210.169.93.0/24 210.169.94.0/24 210.169.95.0/24 210.169.96.0/24 210.169.97.0/24 210.169.98.0/24 210.169.99.0/24

# emobile (http://developer.emnet.ne.jp/ipaddress.html)
# 2008/02/26
Allow from 117.55.1.224/27

# ----------------------

"""
    def __init__(self, addressList = None):
        """ 最新のアドレスリストが得られなければ、ローカルに
もっているものを使う。 """
        if not addressList:
            self.addressList = self.addressList200903
        else:
            self.addressList = addressList

    def lookup(self, ip):
        """addressList を１行ずつ読んで、ip がそのアドレスに含まれるか見る。
        あれば、キャリア名と、アドレス、更新日付を返す。"""
        try:
            for (carrier, cidr, update) in str2cidrs(self.addressList):
                # ここで、IPy を使う。 netmask も見て、アドレス判定。
                # 自分で、ビット演算するなら、 IPy パッケージは不要です。
                if ip in cidr:
                    return (carrier, cidr.strNormal(), update)

        except ValueError, e:
# IPv4 アドレスでないものを渡されると、こういう例外になるので、無視。
# >>> i2c.lookup('Hello World')
# ValueError: invalid literal for long() with base 10: 'Hello World'
            pass
        return (None, None, None)

def str2cidrs(addressList):
    """指定された .htaccess 形式の文字列から、キャリア名とＣＩＤＲ、更新日付
    の組を、１つづつ返す。ジェネレータ。
    ke-tai.org で、ファイルのフォーマットを変えたら、同期してなおすこと。"""
    for line in addressList.split("¥n"):
        # Allow from の前にあらわれるコメント内の文字列を、キャリア名とする。
        # docomo (http://www.nttdocomo.co.jp/service/imode/make/content/ip/)
        m = re.match('^#¥s+(¥w+)¥s+¥(http://', line)
        if m:
            carrier = m.group(1).lower() # 小文字にする。
            update = None
            continue
        # 日付。
        # 2008/06/20
        m = re.match('^#¥s+([¥d/]+)', line)
        if m:
            update = m.group(1)
            continue

        if not line.startswith("Allow from"):
            continue
        line = line.replace("Allow from", "")
        # 空白で区切ったひとつづつが、ＩＰアドレスのＣＩＤＲ表記。
        for ip in line.split():
            yield (carrier, IP(ip), update)
            
# ------------ Google App Engine Web application code --------------------
# 以下、ウエブアプリケーション依存のコード
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch

# ケータイキャリア・クローラIPアドレス
ke_tai_orgUrl = ¥
"""http://ke-tai.org/index.php?%A5%B1%A1%BC%A5%BF%A5%A4%A5%AD%A5%E3%A5%EA%A5%A2%A1%A6%A5%AF%A5%ED%A1%BC%A5%E9IP%A5%A2%A5%C9%A5%EC%A5%B9"""

class KtAddressListDb(db.Model):
    """ htaccess 形式のＩＰアドレスリストを Data Store ファイルに覚える。 """
    # このレコードの更新日
    dbUpdateTime = db.DateTimeProperty(auto_now=True)
    # ke-tai.org のファイルの更新日
    sourceUpdateTime = db.StringProperty()
    # .htaccess ファイル
    content = db.BlobProperty()

    def __repr__(self):
        return self.content

# end class KtAddressListDb

def refreshAddressListDb(self):
    """ 最新版をとってきて、ファイルに入れる。成功したら True を返す。 """
    try:
        result = urlfetch.fetch(ke_tai_orgUrl)
    except urlfetch.Error, e:
        msg = "%s urlfetch error %s" % (ke_tai_orgUrl, e)
        dbgprint(msg)
        self.response.out.write(msg)
        return False
    if result.status_code != 200:
        msg = "%s urlfetch error %s" % (ke_tai_orgUrl, result.status_code)
        dbgprint(msg)
        self.response.out.write(msg)
        return False

    # 既知の形式か。
    start = result.content.find("# Mobile IP Address Blocking")
    end = result.content.find("# MVNO")
    if end == -1:
        end = result.content.find("# Search Engine")
    if start == -1 or end == -1 or end <= start:
        msg = "unknown ip address list format. %d %d %s" % (start, end, result.content[:32])
        dbgprint(msg)
        self.response.out.write(msg)
        self.response.out.write(result.content)
        return False
            
    buf = result.content[start:end]
    if buf.find("Allow") == -1:
        msg = "unknown ip address list format. %s" % buf[:32]
        dbgprint(msg)
        self.response.out.write(msg)
        self.response.out.write(buf)
        return False

    # アドレスリスト自身の更新時刻が、一番最初の方に、書いてある。
    # last update 2009/03/23
    m = re.search('#¥s+last¥s+update¥s*([¥d/]+)', result.content[start:end])
    if m:
        sourceUpdateTime = m.group(1)
    else:
        sourceUpdateTime = None

    # 同じレコードがあったら、消して、
    for rec in KtAddressListDb.all():
        db.delete(rec)

    # 新しいレコードを１つ作って格納。
    rec = KtAddressListDb(content = buf, sourceUpdateTime = sourceUpdateTime)
    rec.put()
    return True
    
def readAddressListDb():
    """ ファイルから、アドレスリストを読んで、文字列として返す。 """
    recs = KtAddressListDb.all().fetch(1)
    if not recs:
        return (None, None)
    return (recs[0].content, recs[0].sourceUpdateTime)

def withinADay():
    """ アドレスリストの更新時刻と、現在を比べて、１日以内なら、 True を返す。 """
    import datetime

    recs = KtAddressListDb.all().fetch(1)
    if not recs:
        return False
    dbTime = recs[0].dbUpdateTime
    now = datetime.datetime.now()
    #dbgprint(now, dbTime)

    if now <= dbTime + datetime.timedelta(days=1):
        return True
    return False

# テンプレート？　めんどうだから、いいや。
def WelcomePage(self):
    head = u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset='UTF-8'" >
<meta name="keywords" content="携帯ＩＰ判定,Python サンプルソースコード,ＩＰ制限,キャリア判定,振り分け">
<meta name="description" content="指定されたＩＰアドレスが、どの携帯電話キャリアのものか判定します。Python ソースもついています。">
<title>携帯ＩＰ判定。Python ソースつき</title>
</head>
<body>
<h1>携帯ＩＰ判定。Python ソースつき</h1>
This site provides IP address to Japanese Mobile Phone Carrier translation.<br>
<p>
このサイトは、指定されたＩＰアドレスが、どの日本の携帯電話のキャリア
のものか判定します。<br>
ウエブサービスとしてお使いになれますし、 Python のソースコードも公開しています。
<br>私の３つめの
<a href="http://appengine.google.com/">Google App Engine</a>
アプリケーションです。</p>
<pre>
Usage:
http://ip2jpmobilecarrier.appspot.com/?ip=210.153.84.1
docomo

http://ip2jpmobilecarrier.appspot.com/?ip=123.108.236.1&amp;output=xml
&lt;ip2carrier&gt;
&lt;ip&gt;123.108.236.1&lt;/ip&gt;
&lt;carrier&gt;softbank&lt;/carrier&gt;
&lt;cidr&gt;123.108.236.0/24&lt;/cidr&gt;
&lt;update&gt;2008/02/29&lt;/update&gt;
&lt;/ip2carrier&gt;

http://ip2jpmobilecarrier.appspot.com/?ip=192.168.0.1
unknown
</pre>
<br>
もとにする、キャリアがウエブアクセスに使うＩＰアドレスの一覧は、
<a href="http://ke-tai.org">ke-tai.org</a>さんが、
<a href="http://ke-tai.org/index.php?%A5%B1%A1%BC%A5%BF%A5%A4%A5%AD%A5%E3%A5%EA%A5%A2%A1%A6%A5%AF%A5%ED%A1%BC%A5%E9IP%A5%A2%A5%C9%A5%EC%A5%B9">
ケータイキャリア・クローラIPアドレス</a>のページで公開されているものを
使わせていただいています。<br>
出力はＸＭＬ，ただのテキストのいずれかです。<br>
キャリア名は、英小文字で、以下のいずれかです。docomo au softbank willcom emobile <br>
携帯電話以外のＩＰアドレスは、unknown と返します。<br>
<br>
Python で書かれた<a href="ktip2carrier.html">ソースコード</a>を、
<a href="http://www.opensource.org/licenses/bsd-license.php">
ＢＳＤライセンス</a>で公開していますので、
ご自分のアプリケーションに組み込むことができます。<br>
ウエブアプリケーション依存の部分は、不要なら除いてください。<br>
ソースの拡張子を、 py から html にしただけのものを置きます。シフトＪＩＳで、ＤＯＳ改行です。<br>
ようするに、.htaccess 形式のファイルを、改行と空白で分割して、
IPy パッケージでＩＰアドレスの包含を判断するだけです。ご自分で書かれても
たいしたことはないでしょう。<br>
<hr>
"""
    
    self.response.out.write(head)
    (buf, sourceUpdateTime) = readAddressListDb()
    # ＩＰアドレスリストを２次配布するのはやめましょう。
    #self.response.out.write('<pre>' + buf + '</pre>')
    self.response.out.write(u"現在のＩＰアドレスリストの更新時刻 %s<br>" % sourceUpdateTime)
    tail = u"""
ＩＰアドレスに変更があった場合、以下のボタンを押すと、ke-tai.org から
最新のリストを取得します。<br>
<br>
<form action='%s' method='post'>
<input type='submit' value='Refresh'>
</form>
<hr>
このソースは、私が、２つめの GAE アプリケーション、<br>
<a href="http://kt100mz.appspot.com/">
<img src="main.jpg" alt="山の写真"></a><br>
携帯電話の通話可能圏内から、１００名山を選ぼう。<br><br>
で使うために書いたものです。よろしければ、こちらも、遊んでみてください。<br>
<br>
免責事項など<br>
通信料を除き、ご利用は無料です。<br>
予告なく、サービスを停止、変更することがあります。<br>
このサイトは、Google App Engine の Free Quota つまり、無料のお試しアカウントを使っているので、
高負荷の場合など、動作は保証されません。<br>
このサイトの主な目的は、 Python を使って携帯サイトを作ろうとする開発者に、
<!-- おこがましいですが -->
ＩＰ判定のためのサンプルソースを提供することです。<br>
ＩＰ判定情報は無保証です。正確な情報は、各キャリアより入手ください。<br>
<br>
このサイトの管理者は、Kanda.Motohiro@gmail.com です。<br>
では、 Enjoy!<br>
Last Update 2009.4.3<br>
</body></html>""" % self.request.environ.get("PATH_INFO")
    self.response.out.write(tail)
    return

class MainPage(webapp.RequestHandler):
    def get(self):
        # IP アドレス指定がなければ、メインのページ。
        ip = self.request.get('ip')
        if not ip:
            WelcomePage(self)
            return

        # 問い合わせ。
        output = self.request.get('output')
        if output == 'xml':
            pass
        else:
            output = 'plain'

        (buf, sourceUpdateTime) = readAddressListDb()

        i2c = Ip2carrier(buf)
        (carrier, cidr, update) = i2c.lookup(ip)
        if not carrier:
            carrier = cidr = update = "unknown"

        if output == 'plain':
            self.response.headers['Content-Type'] = "text/plain"
            self.response.out.write(carrier)
            return

        buf = """<?xml version="1.0" encoding="UTF-8" ?>
<ip2carrier>
<ip>%s</ip>
<carrier>%s</carrier>
<cidr>%s</cidr>
<update>%s</update>
</ip2carrier>""" % (ip, carrier, cidr, update)
        self.response.headers['Content-Type'] = "text/xml"
        self.response.out.write(buf)
        
    def post(self):
        # あまり、ひんぱんに問い合わせても迷惑だろうから。
        if withinADay():
            self.response.out.write(u"""<html><body>
            更新は、１日、１回以内にしてください。
            </body></html>""")
            return

        # アドレスリストの更新の要求。
        ok = refreshAddressListDb(self)
        if ok:
            self.redirect(self.request.environ.get("PATH_INFO"))
        # エラーの場合、何か、画面に出していることがあるので、リダイレクトしない。
        return

# end class MainPage

application = webapp.WSGIApplication([
        ('/', MainPage)
        ], debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)

def _test():
    import doctest, ktip2carrier
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    #_test()
    main()

# ＢＳＤライセンスでソース公開します。IPy と同じにします。
"""
Copyright (c) 2009, Kanda Motohiro
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
# eof
