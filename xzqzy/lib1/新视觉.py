# coding=utf-8
# !/usr/bin/python

import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider
import sys
sys.path.append('..')
xurl = "https://www.6080yy4.com"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}
pm=''

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

    def fl(self,key):
        videos = []
        doc = BeautifulSoup(key, "html.parser")
        soups = doc.find_all('ul', class_="stui-vodlist clearfix")

        vod = [a for div in soups for a in div.find_all('li')]

        for item in vod:
            name = item.select_one("div a")['title']

            id = xurl + item.select_one("div a")["href"]

            pic = item.select_one("div a")['data-original']

            remark = item.find("span", class_="pic-text text-right")
            remark = remark.get_text(strip=True) if remark is not None else ""

            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
            }
            videos.append(video)
        return videos

    def homeContent(self, filter):
        result = {}
        result = {"class":[{"type_id":"1","type_name":"电影"},{"type_id":"2","type_name":"电视剧"},{"type_id":"3","type_name":"综艺"},{"type_id":"4","type_name":"动漫"},{"type_id":"63","type_name":"纪录片"}],"list":[],"filters":{"1":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"喜剧","v":"喜剧"},{"n":"爱情","v":"爱情"},{"n":"恐怖","v":"恐怖"},{"n":"动作","v":"动作"},{"n":"科幻","v":"科幻"},{"n":"剧情","v":"剧情"},{"n":"战争","v":"战争"},{"n":"警匪","v":"警匪"},{"n":"犯罪","v":"犯罪"},{"n":"动画","v":"动画"},{"n":"奇幻","v":"奇幻"},{"n":"武侠","v":"武侠"},{"n":"冒险","v":"冒险"},{"n":"枪战","v":"枪战"},{"n":"悬疑","v":"悬疑"},{"n":"惊悚","v":"惊悚"},{"n":"经典","v":"经典"},{"n":"青春","v":"青春"},{"n":"文艺","v":"文艺"},{"n":"微电影","v":"微电影"},{"n":"古装","v":"古装"},{"n":"历史","v":"历史"},{"n":"运动","v":"运动"},{"n":"农村","v":"农村"},{"n":"儿童","v":"儿童"},{"n":"网络电影","v":"网络电影"}]},{"key":"地区","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"中国香港","v":"中国香港"},{"n":"中国台湾","v":"中国台湾"},{"n":"美国","v":"美国"},{"n":"法国","v":"法国"},{"n":"英国","v":"英国"},{"n":"日本","v":"日本"},{"n":"韩国","v":"韩国"},{"n":"德国","v":"德国"},{"n":"泰国","v":"泰国"},{"n":"印度","v":"印度"},{"n":"意大利","v":"意大利"},{"n":"西班牙","v":"西班牙"},{"n":"加拿大","v":"加拿大"},{"n":"其他","v":"其他"}]},{"key":"年代","name":"年代","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2010","v":"2010"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"排序","name":"排序","value":[{"n":"时间排序","v":"time"},{"n":"人气排序","v":"hits"},{"n":"评分排序","v":"score"}]}],"2":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"爱情","v":"爱情"},{"n":"古装","v":"古装"},{"n":"悬疑","v":"悬疑"},{"n":"都市","v":"都市"},{"n":"喜剧","v":"喜剧"},{"n":"战争","v":"战争"},{"n":"剧情","v":"剧情"},{"n":"青春","v":"青春"},{"n":"历史","v":"历史"},{"n":"网剧","v":"网剧"},{"n":"奇幻","v":"奇幻"},{"n":"冒险","v":"冒险"},{"n":"励志","v":"励志"},{"n":"犯罪","v":"犯罪"},{"n":"商战","v":"商战"},{"n":"恐怖","v":"恐怖"},{"n":"穿越","v":"穿越"},{"n":"农村","v":"农村"},{"n":"人物","v":"人物"},{"n":"商业","v":"商业"},{"n":"生活","v":"生活"},{"n":"短剧","v":"短剧"},{"n":"其他","v":"其他"}]},{"key":"地区","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"中国香港","v":"中国香港"},{"n":"中国台湾","v":"中国台湾"},{"n":"韩国","v":"韩国"},{"n":"日本","v":"日本"},{"n":"美国","v":"美国"},{"n":"英国","v":"英国"},{"n":"泰国","v":"泰国"},{"n":"新加坡","v":"新加坡"},{"n":"其他","v":"其他"}]},{"key":"年代","name":"年代","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2010","v":"2010"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"排序","name":"排序","value":[{"n":"时间排序","v":"time"},{"n":"人气排序","v":"hits"},{"n":"评分排序","v":"score"}]}],"3":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"游戏","v":"游戏"},{"n":"脱口秀","v":"脱口秀"},{"n":"音乐","v":"音乐"},{"n":"情感","v":"情感"},{"n":"生活","v":"生活"},{"n":"职场","v":"职场"},{"n":"真人秀","v":"真人秀"},{"n":"搞笑","v":"搞笑"},{"n":"公益","v":"公益"},{"n":"艺术","v":"艺术"},{"n":"访谈","v":"访谈"},{"n":"益智","v":"益智"},{"n":"体育","v":"体育"},{"n":"少儿","v":"少儿"},{"n":"时尚","v":"时尚"},{"n":"人物","v":"人物"},{"n":"其他","v":"其他"}]},{"key":"地区","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"港台","v":"港台"},{"n":"韩国","v":"韩国"},{"n":"欧美","v":"欧美"},{"n":"其他","v":"其他"}]},{"key":"年代","name":"年代","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2010","v":"2010"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"排序","name":"排序","value":[{"n":"时间排序","v":"time"},{"n":"人气排序","v":"hits"},{"n":"评分排序","v":"score"}]}],"4":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"冒险","v":"冒险"},{"n":"战斗","v":"战斗"},{"n":"搞笑","v":"搞笑"},{"n":"经典","v":"经典"},{"n":"科幻","v":"科幻"},{"n":"玄幻","v":"玄幻"},{"n":"魔幻","v":"魔幻"},{"n":"武侠","v":"武侠"},{"n":"恋爱","v":"恋爱"},{"n":"推理","v":"推理"},{"n":"日常","v":"日常"},{"n":"校园","v":"校园"},{"n":"悬疑","v":"悬疑"},{"n":"真人","v":"真人"},{"n":"历史","v":"历史"},{"n":"竞技","v":"竞技"},{"n":"其他","v":"其他"}]},{"key":"地区","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"日本","v":"日本"},{"n":"韩国","v":"韩国"},{"n":"欧美","v":"欧美"},{"n":"其他","v":"其他"}]},{"key":"年代","name":"年代","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2010","v":"2010"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"排序","name":"排序","value":[{"n":"时间排序","v":"time"},{"n":"人气排序","v":"hits"},{"n":"评分排序","v":"score"}]}],"63":[{"key":"排序","name":"排序","value":[{"n":"时间排序","v":"time"},{"n":"人气排序","v":"hits"},{"n":"评分排序","v":"score"}]}]}}
        return result

    def homeVideoContent(self):
        videos = []
        try:
            detail = requests.get(url=xurl, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc=BeautifulSoup(res,"html.parser")
            soups=doc.find_all('div', class_="module-list module-lines-list")
            for soup2 in soups:
                soup=soup2.find_all('div',class_='module-item-cover')
                for item in soup:
                    name = item.select_one('div a')['title']
                    id = item.select_one('div a')['href']
                    pic = item.select_one('div img')['data-src']
                    remarks=item.find('div',class_='module-item-caption')
                    remarks2=remarks.find('span')
                    if remarks2:
                        remark = item.find('div', class_='module-item-caption').text
                        remark = remark.replace('\n', ' ')

                    else:
                        remark=''
                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                    }
                    videos.append(video)
            # videos = self.fl(res)
            #
            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        if pg:
            page = int(pg)
        else:
            page = 1
        page = int(pg)
        videos = []
        if '类型' in ext.keys():
            lxType = ext['类型']
        else:
            lxType = ''
        if '地区' in ext.keys():
            DqType = ext['地区']
        else:
            DqType = ''
        if '年代' in ext.keys():
            NfType = ext['年代']
        else:
            NfType = ''
        if '排序' in ext.keys():
            PxType = ext['排序']
        else:
            PxType = ''
        url = xurl + '/vodshow/' + cid + '-' + DqType + '-'+PxType+'-' + lxType + '-----'+str(page)+'---'+ NfType + '.html'
        videos = []
        try:
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc=BeautifulSoup(res,"html.parser")
            soups=doc.find('div', class_="module-items")
            soup=soups.find_all('div',class_='module-item')
            for vod in soup:
                name=vod.select_one('div div a')['title']
                id=vod.select_one('div div a')['href']
                pic=vod.select_one('div div img')['data-src']
                remarks = vod.find('div', class_='module-item-text')
                if remarks:
                    remark = remarks.text.replace('\n', ' ')
                else:
                    remark = ''
                remarks1=vod.find('div',class_='module-item-caption')
                if remarks1:
                    remark1 = remarks1.text.replace('\n', ' ')
                else:
                    remark1 = ''
                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark1+remark
                }
                videos.append(video)

        except:
            pass
        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        global pm
        did = ids[0]
        result = {}
        videos = []
        playurl = ''
        if 'http' in did:
            res = requests.get(url=did, headers=headerx)
            name_match = re.search(r'"https://www.6080yy4.com(.*?)"', res.text)
            if name_match:
                did = name_match.group(1)

        res = requests.get(url=xurl+did, headers=headerx)
        res = res.text
        pm_match = re.search(r'<title>(.*?)-', res)
        if pm_match:
            pm = pm_match.group(1)
        doc=BeautifulSoup(res,"html.parser")
        vod_actor=''
        vod_director = ''

        vod_actors=doc.find_all('div', class_='video-info-items')
        for item in vod_actors:
            actor_title = item.find('span', class_='video-info-itemtitle').text
            if actor_title == "主演：":
                vod_actors2=item.find_all('a')
                for item2 in vod_actors2:
                    vod_actor = vod_actor + item2.text + ' '
            if actor_title == "导演：":
                vod_actors2=item.find_all('a')
                for item2 in vod_actors2:
                    vod_director = vod_director + item2.text + ' '
            if actor_title == "剧情：":
                vod_contents=item.find_all('span')
                vod_content=vod_contents[1].text.replace(' ','')
                vod_content=re.sub(r'\s+', ' ', vod_content).strip()

        playform = ''
        purl = ''
        playforms2=doc.find('div', class_='module-heading')
        playforms=playforms2.find_all('div', class_='module-tab-item tab-item')
        for vod in playforms:
            pf=vod.find('span').text
            playform = playform + pf + '$$$'
        playform = playform[:-3]
        purls=doc.find_all('div', class_='sort-item')
        for vods in purls:
            vod=vods.find_all('a')
            for item in vod:
                name = item.find('span').text
                number = re.findall(r'\d+', name)
                if number:
                    number = int(number[0])
                else:
                    number = 0
                id = item['href']
                purl = purl + name + '$' + str(number) + xurl + id + '#'
            purl = purl[:-1] + '$$$'

        purl = purl[:-3]

        videos.append({
            "vod_id": did,
            "vod_name": pm,
            "vod_pic": "",
            "type_name": '',
            "vod_year": '',
            "vod_area": '',
            "vod_remarks": "",
            "vod_actor": vod_actor,
            "vod_director": vod_director,
            "vod_content": vod_content,
            "vod_play_from": playform,
            "vod_play_url": purl
        })

        result['list'] = videos

        return result

    def playerContent(self, flag, id, vipFlags):
        parts = id.split("http")
        if len(parts) > 1:
            before_https, after_https = parts[0], 'http' + parts[1]
        result = {}

        result["parse"] = 1
        result["playUrl"] = ''
        result["url"] = after_https
        result["header"] = headerx
        result["danmaku"] = 'http://gkdm.back1.hpnu.cn/api/danmu?do=danmuku&vodName=' + pm + '&jishu=' + before_https
        return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        if not page:
            page = 1
        detail = requests.get('https://zhuiyingmao4.com/vodsearch/' + key + '----------' + str(page) + '---.html', headers=headerx)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        soups = doc.find('div', class_="module-items module-card-items")
        vods=soups.find_all('div', class_='module-card-item module-item')
        for vod in vods:
            name = vod.select_one('div div a strong').text
            id='https://zhuiyingmao4.com'+vod.select_one('div div a')['href']
            pic=vod.select_one('div div div img')['data-original']
            remark=vod.find('div', class_='module-info-item-content').text
            comma_index = remark.find(',')
            remark = remark[:comma_index].replace('/', '-')
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
            }
            videos.append(video)

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


if __name__ == '__main__':
    spider_instance = Spider()
    # res = spider_instance.homeVideoContent()
    # res=spider_instance.homeContent( 'filter')
    # res=spider_instance.categoryContent( '2', 1, 'filter', {})
    res=spider_instance.detailContent(['https://zhuiyingmao4.com/voddetail/1566315.html'])
    # res=spider_instance.searchContentPage( '庆余年', 'quick', '1')
    # res = spider_instance.playerContent( '1', '3https://www.6080yy4.com/vplay/159119-1-3.html', 'vipFlags')
    print(res)
