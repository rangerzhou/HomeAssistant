"""
Qiyeweichat
{"title":"Homeassistant","message":"text|内容"}
{"title":"Homeassistant","message":"news|内容|打开链接|图片链接"}
{"title":"Homeassistant","message":"textcard|内容|打开链接"}
{"title":"Homeassistant","message":"video|内容|mp4本地地址"}
"""

import logging
import time
import datetime
import requests
import json,os
import voluptuous as vol
import sys

from homeassistant.components.notify import (
    ATTR_MESSAGE, ATTR_TITLE, ATTR_DATA, ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv


CONF_CORPID = 'corpid'
CONF_AGENTID = 'agentId'
CONF_SECRET = 'secret'
CONF_TOUSER = 'touser'

def get_service(hass, config, discovery_info=None):

    corpid = config.get(CONF_CORPID)
    agentId = config.get(CONF_AGENTID)
    secret = config.get(CONF_SECRET)
    touser = config.get(CONF_TOUSER)
    return QiyeweichatNotificationService(hass, corpid, agentId, secret, touser)


class QiyeweichatNotificationService(BaseNotificationService):

    def __init__(self, hass, corpid, agentId, secret, touser):
        self.CORPID = corpid
        self.CORPSECRET = secret
        self.AGENTID = agentId
        self.TOUSER = touser

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        access_token = self._get_access_token()
        return access_token

    def send_message(self, message='', **kwargs):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        title = kwargs.get(ATTR_TITLE)
        if title:
           timestp = datetime.datetime.now()
           sendtime = '{} {}'.format(timestp.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日'), timestp.strftime("%H:%M:%S"))

           msgtype = message.split('|')[0]
           if msgtype == 'text' :
             message = '"content":' + '"' + title + '\r\n' + '--------------------------------------------' + '\r\n' + message.split('|')[1] + '\r\n' + '--------------------------------------------' + '\r\n' + sendtime + '"'
           elif  msgtype == 'textcard' :
             message = '"title":' + '"' + title + '"' + ',' + '"description":' + '"' + message.split('|')[1] + '\r\n' + sendtime + '"' + ',' + '"url":' + '"' + message.split('|')[2] + '"'
           elif  msgtype == 'news' :
             message ='"articles":[{' + '"title":' + '"' + title + '"' + ',' + '"description":' + '"' + message.split('|')[1] + '\r\n' + sendtime + '"' + ',' + '"url":' + '"' + message.split('|')[2] + '"' + ',' + '"picurl":' + '"' + message.split('|')[3] + '"' + '}]'
           elif  msgtype == 'video' :
               path = message.split('|')[2]
               curl = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.get_access_token() + '&type=video'
               files = {'video': open(path, 'rb')}
               r = requests.post(curl, files=files)
               re = json.loads(r.text)
               ree = re['media_id']
               media_id = str(ree)
               message = '"media_id":' + '"' + media_id + '"' + ',' + '"title":' + '"' + title + '"' + ',' + '"description":' + '"' + message.split('|')[1] + '\r\n' + sendtime + '"'
           elif  msgtype == 'image' :
              path = message.split('|')[2]
              curl = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.get_access_token() + '&type=image'
              files = {'image': open(path, 'rb')}
              r = requests.post(curl, files=files)
              re = json.loads(r.text)
              ree = re['media_id']
              media_id = str(ree)
              message = '"media_id":' + '"' + media_id + '"' + ',' + '"title":' + '"' + title + '"' + ',' + '"description":' + '"' + message.split('|')[1] + '\r\n' + sendtime + '"'
           else:
             msgtype = 'text'
             message = '"content":' + '"' + message.split('|')[1] + '"'
           send_data = '{"msgtype": "%s", "safe": "0", "agentid": %s, "touser": "%s", "%s": {%s}}' % (
               msgtype, self.AGENTID, self.TOUSER, msgtype, message)
           send_data8 = send_data.encode('utf-8')
           response = requests.post(send_url,send_data8)
        else:
           _LOGGER.error("Title can NOT be null")
