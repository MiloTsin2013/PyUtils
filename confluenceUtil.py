#!/usr/bin/python
# coding=utf-8

import os
import requests
import json
from pprint import pprint

class ConfluenceUtil():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.loginHeader = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Connection': 'keep-alive',
            'Origin': 'http://{}:{}'.format(self.host, self.port),
            'Host': '{}:{}'.format(self.host, self.port),
        }
        self.header = {'Content-Type':'application/json'}
        self.noCheckHeader = {'X-Atlassian-Token':'no-check'}
        self.session = requests.session()
        # self.session.headers = self.header


    def login(self, user, pwd):
        ''' Confluence 登录'''
        self.user = user
        self.pwd = pwd
        params = {
            'os_username': self.user,
            'os_password': self.pwd,
            'login' : "Log in"
        }
        url = 'http://{}:{}/dologin.action'.format(self.host, self.port)
        result = self.session.post(url=url, headers = self.loginHeader, data = params)
        return result

    def getPageID(self, spaceKey, title):
        '''
        获取页面ID\n
        spaceKey    空间标识\n
        title       页面标题\n
        return pageID , 若页面不存在则返回 -1
        '''
        params = {
            'spaceKey': spaceKey,
            'title': title,
        }
        url = 'http://{}:{}/rest/api/content'.format(self.host, self.port)
        result = self.session.get(url=url, headers=self.header, params=params)
        resultJson = json.loads(result.text)
        # print result.url
        # pprint(resultJson)
        if len(resultJson.get("results",[])) >= 1:
            return resultJson["results"][0].get('id', -1)
        return -1
    
    def getUserID(self, userName):
        '''
        获取用户ID\n
        userName    用户名\n
        return userID , 若用户不存在则返回 -1
        '''
        params = {
            'userName':userName,
        }
        url = 'http://{}:{}/rest/api/search?cql=user+in+(%22{}%22)'.format(self.host, self.port, userName)
        result = self.session.get(url=url, headers=self.header, params=params)
        resultJson = json.loads(result.text)
        if len(resultJson.get("results",[])) >= 1:
            return resultJson["results"][0]["user"].get('userKey', -1)
        return -1
    
    def getPageJson(self, pageID):
        '''
        根据 PageID 获取页面信息（Json形式）\n
        pageID      页面ID
        '''
        url="http://{}:{}/rest/api/content/{}".format(self.host, self.port, pageID)
        response = self.session.get(url=url)
        response.encoding = "utf8"
        return json.loads(response.text)

    def getPageHTML(self, spaceKey, title):
        '''
        获取 Confluence 页面的 HTML\n
        spaceKey    空间标识\n
        title       页面标题\n
        '''
        params = {
            'spaceKey':spaceKey,
            'title':title,
            'expand':'body.view'
        }
        url = 'http://{}:{}/rest/api/content'.format(self.host, self.port)
        result = self.session.get(url=url, headers=self.header, params=params)
        resultJson = json.loads(result.text)
        if len(resultJson.get("results",[])) >= 1:
            return resultJson["results"][0]["body"]['view']['value']
        return -1

    def createPage(self, spaceKey, title, fatherId, value):
        '''
        创建页面\n
        spaceKey    空间标识\n
        title       页面标题\n
        fatherId    父级ID\n
        value       页面内容\n
        return pageID , 若页面创建失败则返回 -1
        '''
        params = {
            "type":"page",
            "space":{
                "key":spaceKey
                },
            "title":title,
            "ancestors": [
                {
                    "id":fatherId
                    }
                ],
            "body":{
                "storage":{
                    "value": value,
                    "representation":"storage"
                }
            }
        }
        url = 'http://{}:{}/rest/api/content'.format(self.host, self.port)
        result = self.session.post(url=url, headers=self.header, data=json.dumps(params))
        resultJson = json.loads(result.text)
        # print result.url
        # pprint(resultJson)
        return resultJson.get('id', -1)
        
    def updatePage(self, spaceKey, title, pageID, value):
        '''
        更新页面\n
        pageID    页面ID\n
        return pageID , 若页面创建失败则返回 -1
        '''
        version = self.getPageJson(pageID)['version']['number']+1
        params = {
            "id":pageID,
            "type":"page",
            "title":title,
            "space":{"key":spaceKey},
            "body":{
                "storage":{
                    "value": value,
                    "representation":"storage"
                    }
                },
            "version":{"number":version}
            }
        url = 'http://{}:{}/rest/api/content/{}'.format(self.host, self.port, pageID)
        result = self.session.put(url=url, headers=self.header, data=json.dumps(params))
        # print result.url
        # print result.status_code # <type 'int'>
        resultJson = json.loads(result.text)
        # pprint(resultJson)
        return resultJson.get('id', -1)

    def deletePage(self, pageID):
        '''
        删除页面\n
        pageID    页面ID\n
        return boolean
        '''
        url = 'http://{}:{}/rest/api/content/{}'.format(self.host, self.port, pageID)
        result = self.session.delete(url=url, headers=self.header)
        # print result.url
        # print result.status_code # <type 'int'>
        if result.status_code == 204:
            return True
        else:
            return False

    def getAnnexJsonByName(self, pageID, filename):
        '''
        通过附件名获取附件Json\n
        pageID      页面ID\n
        filename    附件名
        '''
        params = {'filename':filename}
        url = 'http://{}:{}/rest/api/content/{}/child/attachment'.format(self.host, self.port, pageID)
        result = self.session.get(url=url, headers=self.header, params=params)
        # print result.url
        print result.status_code # <type 'int'>
        # pprint(result.text)
        resultJson = json.loads(result.text)
        # pprint(resultJson)
        return resultJson
        

    def getAnnexIDByName(self, pageID, filename):
        '''
        通过附件名获取附件ID\n
        pageID      页面ID\n
        filename    附件名
        '''
        resultJson = self.getAnnexJsonByName(pageID, filename)
        if len(resultJson.get("results",[])) >= 1:
            return resultJson["results"][0].get('id', -1)
        return -1

    def uploadAnnex(self, pageID, filePath):
        '''
        上传附件(一次一个)\n
        pageID      页面ID\n
        filePath    文件路径\n
        return      annexID
        '''
        # os.system('curl -D- -u {}:{} -X POST -H "X-Atlassian-Token: no-check" -F "file=@{}" http://{}:{}/rest/api/content/{}/child/attachment?allowDuplicated=true'.format(self.user, self.pwd, filePath, self.host, self.port, pageID))
        params = {'allowDuplicated':'true'}
        # files 的 key 为请求参数的字段名，value 元组每一个字段代表的依次为("filename", "fileobject", "content-type", "headers") 缺省即为默认值
        files = {'file': (os.path.split(filePath)[1], open(filePath,'rb'))}
        url = 'http://{}:{}/rest/api/content/{}/child/attachment'.format(self.host, self.port, pageID)
        result = self.session.post(url=url, headers=self.noCheckHeader, data=params, files=files)
        # print result.url
        print result.status_code # <type 'int'>
        # print result.text
        resultJson = json.loads(result.text)
        pprint(resultJson)
        return resultJson.get('id', -1)

    def updateAnnex(self, pageID, annexID, filePath):
        '''
        更新附件\n
        pageID      页面ID\n
        annexID     附件ID\n
        filePath    文件路径\n
        return  annexID
        '''
        params = {'allowDuplicated':'true'}
        # files 的 key 为请求参数的字段名，value 元组每一个字段代表的依次为("filename", "fileobject", "content-type", "headers") 缺省即为默认值
        files = {'file': (os.path.split(filePath)[1], open(filePath,'rb'))}
        url = 'http://{}:{}/rest/api/content/{}/child/attachment/{}/data'.format(self.host, self.port, pageID, annexID)
        result = self.session.post(url=url, headers=self.noCheckHeader, data=params, files=files)
        # print result.url
        print result.status_code # <type 'int'>
        # print result.text
        resultJson = json.loads(result.text)
        pprint(resultJson)
        return resultJson.get('id', -1)
    