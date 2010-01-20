# coding: utf-8
from vendor.IPy import IP

docomo_cidr_list = [
  "210.153.84.0/24",
  "210.136.161.0/24",
  "210.153.86.0/24",
  "124.146.174.0/24",
  "124.146.175.0/24",
  "202.229.176.0/24",
  "202.229.177.0/24",
  "202.229.178.0/24",
]

ezweb_cidr_list = [
  "210.230.128.224/28",
  "121.111.227.160/27",
  "61.117.1.0/28",
  "219.108.158.0/27",
  "219.125.146.0/28",
  "61.117.2.32/29",
  "61.117.2.40/29",
  "219.108.158.40/29",
  "219.125.148.0/25",
  "222.5.63.0/25",
  "222.5.63.128/25",
  "222.5.62.128/25",
  "59.135.38.128/25",
  "219.108.157.0/25",
  "219.125.145.0/25",
  "121.111.231.0/25",
  "121.111.227.0/25",
  "118.152.214.192/26",
  "118.159.131.0/25",
  "118.159.133.0/25",
  "118.159.132.160/27",
  "118.159.133.192/26",
]

softbank_cidr_list = [
]

willcom_cidr_list = [
]

"""
type
1: DoCoMo
2: EZweb
3: Softbank
4: Willcom

fixme: cache
"""
def ip_list(type):
  dict = { 
    1: docomo_cidr_list,
    2: ezweb_cidr_list,
    3: softbank_cidr_list,
    4: willcom_cidr_list
  }
  ips = []
  for i in dict[type]:
    for ip in IP(i):
      ips.append(str(ip))
  return ips

def is_docomo_ip(ip):
  try:
    return True if ip_list(1).index(ip) else False
  except:
    return False

def is_ezweb_ip(ip):
  pass

def is_softbank_ip(ip):
  pass

def is_willcom_ip(ip):
  pass

def is_mobile_ip(ip):
  pass
