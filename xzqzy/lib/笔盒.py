# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
import json
from base.spider import Spider

sys.path.append('..')

xurl = "https://biheibo.pro"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36'
}
class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass
    def fl(self, key):
        videos = []
        js1 = json.loads(key)
        js = js1['data']['hits']
        for i in js:
            name = i['vod_name']
            id = xurl + i['detail_url']
            if 'http' in i['detail_url']:
                continue
            pic = i['vod_pic']
            remark = i['vod_class']
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
            }
            videos.append(video)
        return videos

    def homeContent(self, filter):
        res = requests.get(xurl, headers=headerx, timeout=20)
        res.encoding = "utf-8"
        res = res.text
        doc = BeautifulSoup(res, "html.parser")
        result = {}
        result['class'] = []
        vodss = doc.find('div', class_="grid grid-cols-4 text-xl gap-y-5 max-sm:text-base max-sm:grid-cols-2")
        vod = vodss.find_all('a')
        for item in vod:
            id = item.text
            result['class'].append({'type_id': id, 'type_name': id})
        return result

    def homeVideoContent(self):
        detail = requests.get(
            url='https://dlv2byu6cdh8c.cloudfront.net/V1/search?q=%E6%97%A0%E7%A0%81&t=1&page=1&pageSize=24',
            headers=headerx, allow_redirects=False)
        detail.encoding = "utf-8"
        res = detail.text
        videos = self.fl(res)
        result = {'list': videos}
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        if not pg:
            pg = 1
        videos = []
        try:
            url = 'https://dlv2byu6cdh8c.cloudfront.net/V1/search?q=' + cid + '&t=1&page=' + str(pg) + '&pageSize=24'
            res = requests.get(url, headers=headerx)
            res.encoding = "utf-8"
            res = res.text
            videos = self.fl(res)
            result = {'list': videos}

        except:
            pass

        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        videos = []
        result = {}

        videos.append({
            "vod_id": '',
            "vod_name": '',
            "vod_pic": "",
            "type_name": "ぃぅおか🍬 คิดถึง",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": "",
            "vod_play_from": "直链播放",
            "vod_play_url": did
        })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        res = requests.get(id, headers=headerx)
        res.encoding = "utf-8"
        match = re.search(r'\},"url":"(.*?)"', res.text)

        if match:
            purl = match.group(1).replace('\\', '')
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = purl
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        if not page:
            page = 1
        url = 'https://dlv2byu6cdh8c.cloudfront.net/V1/search?q=' + key + '&t=1&page=' + str(page) + '&pageSize=24'
        res = requests.get(url, headers=headerx)
        res.encoding = "utf-8"
        res = res.text
        videos = self.fl(res)

        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result
    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')


    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None
