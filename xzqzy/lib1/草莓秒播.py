# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from base.spider import Spider
from urllib.parse import unquote
sys.path.append('..')
xurl1 = "https://3.buka515.top/%E4%B8%8D%E5%8D%A1.js"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}
resx=requests.get(xurl1, headers=headerx, timeout=20)
xurlmatch = re.search(r"<a href=\\'(.*?)\\", resx.text)

if xurlmatch:
    xurl = xurlmatch.group(1)
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


    def homeContent(self, filter):
        result = {}
        result['class'] = []
        res = requests.get(xurl+'/label/baidu.html', headers=headerx, timeout=20)
        res.encoding = "utf-8"
        res = res.text
        doc = BeautifulSoup(res, "html.parser")
        vodss = doc.find_all('ul', class_="row-item-content")
        for vods in vodss:
            vod=vods.find_all('li')
            for item in vod:
                id = item.select_one("a")["href"].replace('.html', "")
                if 'http' in id or id == '/':
                    continue
                name =item.select_one("a font").text.strip()
                result['class'].append({'type_id': id, 'type_name': name})
        return result

    def slets(self,doc):
        videos=[]
        soups = doc.find('ul', class_="content-list")
        soup=soups.find_all('li')
        for item in soup:
            name = item.select_one("div h5 a").text
            id = xurl + item.select_one("div h5 a")["href"]
            pic=item.select_one("a")["style"]
            pic = pic.replace("background-image: url(", "").replace(");", "").replace('"', '')
            remark=item.find('span', class_="note text-bg-r").text
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
        try:
            detail = requests.get(url=xurl+'/label/baidu.html', headers=headerx)
            detail.encoding = "utf-8"
            doc = BeautifulSoup(detail.text, "html.parser")
            videos = self.slets(doc)
            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        if not pg:
            pg = 1
        videos = []
        try:
            res = requests.get(xurl + cid + '/page/' + str(pg) + '.html', headers=headerx)
            res.encoding = "utf-8"
            doc = BeautifulSoup(res.text, "html.parser")
            videos = self.slets(doc)

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
        res = requests.get(did, headers=headerx)
        res.encoding = "utf-8"
        match = re.search(r'<a\s+href="([^"]+)"\s+class="centered-link"', res.text)

        if match:
            purl = xurl+match.group(1)

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
            "vod_play_url": purl
        })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        res = requests.get(id, headers=headerx)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        soups=doc.find('div', class_="player")
        soup=soups.find('script')
        match = re.search(r'"url":"(.*?)",', soup.text)

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
        res = requests.get(xurl + '/index.php/vod/search/page/' + str(page) + '/wd/' + key + '.html', headers=headerx)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        videos = self.slets(doc)

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

