# coding=utf-8
# !/usr/bin/python
import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import json
from base.spider import Spider
sys.path.append('..')
xurl='https://www.cfkj86.com'
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
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

    def extract_middle_text(self,text, start_str, end_str):

        start_index = text.find(start_str)
        if start_index == -1:
            return ""
        end_index = text.find(end_str, start_index + len(start_str))
        if end_index == -1:
            return ""

        middle_text = text[start_index + len(start_str):end_index]
        return middle_text.replace("\\", "")
    

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "1", "type_name": "电影"}, {"type_id": "2", "type_name": "电视剧"},
                            {"type_id": "3", "type_name": "综艺"}, {"type_id": "4", "type_name": "动漫"}], "list": [],
                  "filters": {"1": [{"key": "类型", "name": "类型",
                                     "value": [{"n": "全部", "v": ""}, {"n": "喜剧", "v": "/type/22"},
                                               {"n": "动作", "v": "/type/23"}, {"n": "战争", "v": "/type/25"},
                                               {"n": "爱情", "v": "/type/26"}, {"n": "悬疑", "v": "/type/27"},
                                               {"n": "科幻", "v": "/type/30"}, {"n": "冒险", "v": "/type/31"},
                                               {"n": "动画", "v": "/type/33"}, {"n": "惊悚", "v": "/type/34"},
                                               {"n": "犯罪", "v": "/type/35"}, {"n": "恐怖", "v": "/type/36"},
                                               {"n": "剧情", "v": "/type/37"}, {"n": "灾难", "v": "/type/81"},
                                               {"n": "奇幻", "v": "/type/87"}, {"n": "伦理", "v": "/type/83"},
                                               {"n": "其他", "v": "/type/43"}]}, {"key": "地区", "name": "地区",
                                                                                  "value": [{"n": "全部", "v": ""},
                                                                                            {"n": "中国大陆",
                                                                                             "v": "/area/中国大陆"},
                                                                                            {"n": "中国香港",
                                                                                             "v": "/area/中国香港"},
                                                                                            {"n": "中国台湾",
                                                                                             "v": "/area/中国台湾"},
                                                                                            {"n": "美国",
                                                                                             "v": "/area/美国"},
                                                                                            {"n": "日本",
                                                                                             "v": "/area/日本"},
                                                                                            {"n": "韩国",
                                                                                             "v": "/area/韩国"},
                                                                                            {"n": "印度",
                                                                                             "v": "/area/印度"},
                                                                                            {"n": "泰国",
                                                                                             "v": "/area/泰国"},
                                                                                            {"n": "其他",
                                                                                             "v": "/area/其他"}]},
                                    {"key": "年代", "name": "年代",
                                     "value": [{"n": "全部", "v": ""}, {"n": "2024", "v": "/year/2024"},
                                               {"n": "2023", "v": "/year/2023"}, {"n": "2022", "v": "/year/2022"},
                                               {"n": "2021", "v": "/year/2021"}, {"n": "2020", "v": "/year/2020"},
                                               {"n": "2019", "v": "/year/2019"}, {"n": "2018", "v": "/year/2018"},
                                               {"n": "2017", "v": "/year/2017"}, {"n": "2016", "v": "/year/2016"},
                                               {"n": "2015", "v": "/year/2015"}, {"n": "2014", "v": "/year/2014"},
                                               {"n": "2013", "v": "/year/2013"}, {"n": "2012", "v": "/year/2012"},
                                               {"n": "2011", "v": "/year/2011"}, {"n": "2010", "v": "/year/2010"},
                                               {"n": "2009~2000", "v": "/year/2009~2000"}]},
                                    {"key": "语言", "name": "语言",
                                     "value": [{"n": "全部", "v": ""}, {"n": "国语", "v": "/lang/国语"},
                                               {"n": "英语", "v": "/lang/英语"}, {"n": "粤语", "v": "/lang/粤语"},
                                               {"n": "韩语", "v": "/lang/韩语"}, {"n": "日语", "v": "/lang/日语"},
                                               {"n": "其他", "v": "/lang/其他"}]}], "2": [
                      {"key": "类型", "name": "类型",
                       "value": [{"n": "全部", "v": ""}, {"n": "国产剧", "v": "/type/14"},
                                 {"n": "欧美剧", "v": "/type/15"}, {"n": "港台剧", "v": "/type/16"},
                                 {"n": "日韩剧", "v": "/type/62"}, {"n": "其他剧", "v": "/type/68"}]},
                      {"key": "剧情", "name": "剧情",
                       "value": [{"n": "全部", "v": ""}, {"n": "古装", "v": "/class/古装"},
                                 {"n": "战争", "v": "/class/战争"}, {"n": "喜剧", "v": "/class/喜剧"},
                                 {"n": "家庭", "v": "/class/家庭"}, {"n": "犯罪", "v": "/class/犯罪"},
                                 {"n": "动作", "v": "/class/动作"}, {"n": "奇幻", "v": "/class/奇幻"},
                                 {"n": "剧情", "v": "/class/剧情"}, {"n": "历史", "v": "/class/历史"},
                                 {"n": "短片", "v": "/class/短片"}]}, {"key": "地区", "name": "地区",
                                                                       "value": [{"n": "全部", "v": ""},
                                                                                 {"n": "中国大陆",
                                                                                  "v": "/area/中国大陆"},
                                                                                 {"n": "中国香港",
                                                                                  "v": "/area/中国香港"},
                                                                                 {"n": "中国台湾",
                                                                                  "v": "/area/中国台湾"},
                                                                                 {"n": "美国", "v": "/area/美国"},
                                                                                 {"n": "日本", "v": "/area/日本"},
                                                                                 {"n": "韩国", "v": "/area/韩国"},
                                                                                 {"n": "泰国", "v": "/area/泰国"},
                                                                                 {"n": "其他", "v": "/area/其他"}]},
                      {"key": "年代", "name": "年代",
                       "value": [{"n": "全部", "v": ""}, {"n": "2024", "v": "/year/2024"},
                                 {"n": "2023", "v": "/year/2023"}, {"n": "2022", "v": "/year/2022"},
                                 {"n": "2021", "v": "/year/2021"}, {"n": "2020", "v": "/year/2020"},
                                 {"n": "2019", "v": "/year/2019"}, {"n": "2018", "v": "/year/2018"},
                                 {"n": "2017", "v": "/year/2017"}, {"n": "2016", "v": "/year/2016"},
                                 {"n": "2015", "v": "/year/2015"}, {"n": "2014", "v": "/year/2014"},
                                 {"n": "2013", "v": "/year/2013"}, {"n": "2012", "v": "/year/2012"},
                                 {"n": "2011", "v": "/year/2011"}, {"n": "2010", "v": "/year/2010"},
                                 {"n": "2009~2000", "v": "/year/2009~2000"}]}, {"key": "语言", "name": "语言",
                                                                                "value": [{"n": "全部", "v": ""},
                                                                                          {"n": "普通话",
                                                                                           "v": "/lang/普通话"},
                                                                                          {"n": "英语",
                                                                                           "v": "/lang/英语"},
                                                                                          {"n": "粤语",
                                                                                           "v": "/lang/粤语"},
                                                                                          {"n": "韩语",
                                                                                           "v": "/lang/韩语"},
                                                                                          {"n": "日语",
                                                                                           "v": "/lang/日语"},
                                                                                          {"n": "泰语",
                                                                                           "v": "/lang/泰语"},
                                                                                          {"n": "其他",
                                                                                           "v": "/lang/其他"}]}], "3": [
                      {"key": "类型", "name": "类型",
                       "value": [{"n": "全部", "v": ""}, {"n": "国产综艺", "v": "/type/69"},
                                 {"n": "港台综艺", "v": "/type/70"}, {"n": "日韩综艺", "v": "/type/72"},
                                 {"n": "欧美综艺", "v": "/type/73"}, {"n": "其他综艺", "v": "/type/74"}]},
                      {"key": "剧情", "name": "剧情",
                       "value": [{"n": "全部", "v": ""}, {"n": "真人秀", "v": "/class/真人秀"},
                                 {"n": "音乐", "v": "/class/音乐"}, {"n": "脱口秀", "v": "/class/脱口秀"}]},
                      {"key": "地区", "name": "地区",
                       "value": [{"n": "全部", "v": ""}, {"n": "中国大陆", "v": "/area/中国大陆"},
                                 {"n": "中国香港", "v": "/area/中国香港"}, {"n": "中国台湾", "v": "/area/中国台湾"},
                                 {"n": "美国", "v": "/area/美国"}, {"n": "日本", "v": "/area/日本"},
                                 {"n": "韩国", "v": "/area/韩国"}, {"n": "其他", "v": "/area/其他"}]},
                      {"key": "年代", "name": "年代",
                       "value": [{"n": "全部", "v": ""}, {"n": "2024", "v": "/year/2024"},
                                 {"n": "2023", "v": "/year/2023"}, {"n": "2022", "v": "/year/2022"},
                                 {"n": "2021", "v": "/year/2021"}, {"n": "2020", "v": "/year/2020"}]},
                      {"key": "语言", "name": "语言",
                       "value": [{"n": "全部", "v": ""}, {"n": "国语", "v": "/lang/国语"},
                                 {"n": "英语", "v": "/lang/英语"}, {"n": "粤语", "v": "/lang/粤语"},
                                 {"n": "韩语", "v": "/lang/韩语"}, {"n": "日语", "v": "/lang/日语"},
                                 {"n": "其他", "v": "/lang/其他"}]}], "4": [{"key": "类型", "name": "类型",
                                                                             "value": [{"n": "全部", "v": ""},
                                                                                       {"n": "国产动漫",
                                                                                        "v": "/type/国产动漫"},
                                                                                       {"n": "日韩动漫",
                                                                                        "v": "/type/日韩动漫"},
                                                                                       {"n": "欧美动漫",
                                                                                        "v": "/type/欧美动漫"}]},
                                                                            {"key": "剧情", "name": "剧情",
                                                                             "value": [{"n": "全部", "v": ""},
                                                                                       {"n": "喜剧",
                                                                                        "v": "/class/喜剧"},
                                                                                       {"n": "科幻",
                                                                                        "v": "/class/科幻"},
                                                                                       {"n": "热血",
                                                                                        "v": "/class/热血"},
                                                                                       {"n": "冒险",
                                                                                        "v": "/class/冒险"},
                                                                                       {"n": "动作",
                                                                                        "v": "/class/动作"},
                                                                                       {"n": "运动",
                                                                                        "v": "/class/运动"},
                                                                                       {"n": "战争",
                                                                                        "v": "/class/战争"},
                                                                                       {"n": "儿童",
                                                                                        "v": "/class/儿童"}]},
                                                                            {"key": "地区", "name": "地区",
                                                                             "value": [{"n": "全部", "v": ""},
                                                                                       {"n": "中国大陆",
                                                                                        "v": "/area/中国大陆"},
                                                                                       {"n": "日本", "v": "/area/日本"},
                                                                                       {"n": "美国", "v": "/area/美国"},
                                                                                       {"n": "其他",
                                                                                        "v": "/area/其他"}]},
                                                                            {"key": "年代", "name": "年代",
                                                                             "value": [{"n": "全部", "v": ""},
                                                                                       {"n": "2024", "v": "/year/2024"},
                                                                                       {"n": "2023", "v": "/year/2023"},
                                                                                       {"n": "2022", "v": "/year/2022"},
                                                                                       {"n": "2021", "v": "/year/2021"},
                                                                                       {"n": "2020", "v": "/year/2020"},
                                                                                       {"n": "2019", "v": "/year/2019"},
                                                                                       {"n": "2018", "v": "/year/2018"},
                                                                                       {"n": "2017", "v": "/year/2017"},
                                                                                       {"n": "2016", "v": "/year/2016"},
                                                                                       {"n": "2015", "v": "/year/2015"},
                                                                                       {"n": "2014", "v": "/year/2014"},
                                                                                       {"n": "2013", "v": "/year/2013"},
                                                                                       {"n": "2012", "v": "/year/2012"},
                                                                                       {"n": "2011", "v": "/year/2011"},
                                                                                       {"n": "2010", "v": "/year/2010"},
                                                                                       {"n": "2009~2000",
                                                                                        "v": "/year/2009~2000"}]},
                                                                            {"key": "语言", "name": "语言",
                                                                             "value": [{"n": "全部", "v": ""},
                                                                                       {"n": "国语", "v": "/lang/国语"},
                                                                                       {"n": "英语", "v": "/lang/英语"},
                                                                                       {"n": "日语", "v": "/lang/日语"},
                                                                                       {"n": "其他",
                                                                                        "v": "/lang/其他"}]}]}}

        return result

    def homeVideoContent(self):
        try:
            res = requests.get(url=xurl, headers=headerx)
            res.encoding = "utf-8"
            res = res.text
            videos = []
            doc = self.extract_middle_text(res, 'self.__next_f.push([1,"1b:[\\"$\\",\\"main\\",null,', ']\\n"])')
            js1 = json.loads(doc)
            sources = ['homeNewMovieList', 'homeBroadcastList', 'homeManagerList', 'newestTvList', 'newestVarietyList',
                       'newestCartoonList']
            combined_list = [js1["children"][3]["data"]["data"][source] for source in sources]
            videos = [
                {
                    "vod_id": vod['vodId'],
                    "vod_name": vod['vodName'],
                    "vod_pic": vod['vodPicThumb'],
                    "vod_remarks": f"{vod['vodVersion']} {vod['vodRemarks']}"
                }
                for sublist in combined_list
                for vod in sublist
            ]

            result = {'list': videos}
            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}

        area = ""
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
        if '语言' in ext.keys():
            YyType = ext['语言']
        else:
            YyType = ''
        if '年代' in ext.keys():
            NdType = ext['年代']
        else:
            NdType = ''
        if '剧情' in ext.keys():
            JqType = ext['剧情']
        else:
            JqType = ''
        url = xurl + "/vod/show/id/" + cid + lxType + JqType + DqType + NdType + YyType + "/page/" + str(page)

        try:
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = self.extract_middle_text(res, '([1,"1b:[\\"$\\",\\"$L1f\\",null,', ']\\n"])')
            js1 = json.loads(doc)
            st1 = js1["videoList"]["data"]["list"]

            for vod in st1:
                name = vod['vodName']
                pic = vod['vodPicThumb']
                id = vod['vodId']
                remark = vod['vodVersion'] + " " + vod['vodRemarks']  # 注意这里的空格统一了
                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
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
        did = ids[0]
        videos = []
        result = {}
        res = requests.get(xurl + '/detail/' + did, headers=headerx)
        res.encoding = "utf-8"
        res = res.text
        doc = BeautifulSoup(res, 'html.parser')
        soup = doc.find_all("div", class_="listitem")
        purl = ''
        for i in soup:
            name = i.select_one("a").text
            id = xurl + i.select_one("a")["href"]
            purl = purl + name + '$' + id + '#'
        purl = purl[:-1]
        videos.append({
            "vod_id": '',
            "vod_name": '',
            "vod_pic": "",
            "type_name": "金牌影院",
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
        result["parse"] = 1
        result["playUrl"] = ''
        result["url"] = id
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos=[]
        if not page:
            page = 1
        #https://www.cfkj86.com/vod/search/
        res = requests.get(xurl + '/vod/search/'  + key , headers=headerx)
        res.encoding = "utf-8"
        res = res.text
        doc = self.extract_middle_text(res, '"1c:[\\"$\\",\\"$L20\\",null,', ']\\n"])')
        js1 = json.loads(doc)
        st1 = js1["data"]["data"]["result"]["list"]
        for vod in st1:
            name = vod['vodName']
            pic = vod['vodPic']
            id = vod['vodId']
            remark = vod['vodVersion'] + " " + vod['vodRemarks']
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

    def searchContent(self, key, quick, page=1):
        return self.searchContentPage(key, quick, page)

    def localProxy(self, params):
        pass
