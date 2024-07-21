# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
import json
from base.spider import Spider


sys.path.append('..')
xurl1 = "https://jzy176.top"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}
res=requests.get(xurl1, headers=headerx)
match = re.search(r'2;URL=(.*?)">', res.text)
if match:
    xurl=match.group(1).replace("/?", "")
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
    'Referer':'https://yjs01.cc'
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

    def slets(self,doc):
        videos=[]
        soup = doc.find("div", class_='mod index-list')
        sourcediv = soup.find_all('dl')
        for item in sourcediv:
            name = item.select_one("dd a h3").text.strip()
            id = xurl + item.select_one("dd a")["href"]
            pic = item.select_one("dt a img ")["data-src"]
            remark = item.select_one("dt a i").text.strip()
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
            }
            videos.append(video)
        return videos

    def homeVideoContent(self):
        videos = []
        url = xurl
        try:
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            doc = BeautifulSoup(detail.text, "html.parser")
            videos = self.slets(doc)
            result = {'list': videos}
            return result
        except:
            pass

    def homeContent(self, filter):
        result = {}
        result['class'] = []
        res = requests.get(xurl, headers=headerx, timeout=10)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        sourcediv = doc.find_all('div', class_='menu clearfix')
        vod = [a for div in sourcediv for a in div.find_all('a')]
        for item in vod:
            name = item.text
            if name == "精品一区" or name == "API二区":
                continue
            id = item['href']
            id = id.replace('.html', '')
            result['class'].append({'type_id': id, 'type_name': name})
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if not pg:
            pg = 1
        url = xurl + cid + "/index/" + str(pg) + '.html'
        detail = requests.get(url=url, headers=headerx, timeout=10)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        videos = self.slets(doc)

        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        res = requests.get(url=did, headers=headerx)
        source_match = re.search(r'iframe src="(.*?)"', res.text)
        if source_match:
            url = source_match.group(1)
        res = requests.get(url=xurl+url, headers=headerx)
        purl_match = re.search(r'"url":"(.*?)"', res.text)
        if purl_match:
            purl = purl_match.group(1).replace('\\', '')
        videos.append({
            "vod_id": did,
            "vod_name": '',
            "vod_pic": "",
            "type_name": "ぃぅおか🍬 คิดถึง",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": "",
            "vod_play_from": '直链播放',
            "vod_play_url": purl
        })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        headerp = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
            'Referer': xurl
        }
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        result["header"] = headerp
        return result

    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def searchContentPage(self, key, quick, page):
        videos = []
        result = {}
        if not page:
            pg = 0
        else:
            pg = page
        url = xurl + '/search/yjs/' + key + "/" + str(pg) + '.html'
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        videos = self.slets(doc)
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None

