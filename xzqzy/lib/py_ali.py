# coding=utf-8
# !/usr/bin/python
import sys
import time
import json
import hashlib
from base64 import b64decode
from Crypto.Cipher import AES
from difflib import SequenceMatcher
from collections import OrderedDict
from urllib.parse import quote, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    fileidList = []
    shareidList = []
    header = {
        "Referer": "https://www.aliyundrive.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
    }

    def getName(self):
        return "首页"

    def init(self, extend):
        try:
            self.extendDict = json.loads(extend)
        except:
            self.extendDict = {}

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeVideoContent(self):
        from re import sub
        videos = []
        header = {
            'Host': 'frodo.douban.com', 'Connection': 'Keep-Alive',
            'Referer': 'https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat'}
        url = 'https://frodo.douban.com/api/v2/subject_collection/subject_real_time_hotest/items?start=0&count=30&apikey=0ac44ae016490db2204ce0a042db2916'
        try:
            vodList = self.fetch(url, headers=header, verify=False).json()['subject_collection_items']
            for vod in vodList:
                remark = vod['rating']['value']
                if remark != '':
                    remark = '{}分'.format(remark)
                else:
                    remark = '暂无评分'
                videos.append({
                    "vod_db_id": vod['id'],
                    "vod_name": vod['title'],
                    "vod_pic": sub(r'photo/(.*?)/', 'photo/l/', vod['pic']['large']) + '@User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36@Referer=https://www.douban.com/',
                    "vod_remarks": remark
                })
        except:
            pass
        result = {'list': videos}
        return result

    def homeContent(self, filter):
        result = {}
        result['class'] = [{'type_id': 'hot_gaia', 'type_name': '热门电影'}, {'type_id': 'tv_hot', 'type_name': '热播剧集'}, {'type_id': 'show_hot', 'type_name': '热播综艺'}, {'type_id': 'movie', 'type_name': '电影筛选'}, {'type_id': 'tv', 'type_name': '电视筛选'}, {'type_id': 'rank_list_movie', 'type_name': '电影榜单'}, {'type_id': 'rank_list_tv', 'type_name': '电视榜单'}]
        if filter:
            from datetime import datetime
            currentYear = datetime.now().year
            result['filters'] = {'hot_gaia': [{'key': 'sort', 'name': '排序', 'value': [{'n': '热度', 'v': 'recommend'}, {'n': '最新', 'v': 'time'}, {'n': '评分', 'v': 'rank'}]}, {'key': 'area', 'name': '地区', 'value': [{'n': '全部', 'v': '全部'}, {'n': '华语', 'v': '华语'}, {'n': '欧美', 'v': '欧美'}, {'n': '韩国', 'v': '韩国'}, {'n': '日本', 'v': '日本'}]}], 'tv_hot': [{'key': 'type', 'name': '分类', 'value': [{'n': '综合', 'v': 'tv_hot'}, {'n': '国产剧', 'v': 'tv_domestic'}, {'n': '欧美剧', 'v': 'tv_american'}, {'n': '日剧', 'v': 'tv_japanese'}, {'n': '韩剧', 'v': 'tv_korean'}, {'n': '动画', 'v': 'tv_animation'}]}], 'show_hot': [{'key': 'type', 'name': '分类', 'value': [{'n': '综合', 'v': 'show_hot'}, {'n': '国内', 'v': 'show_domestic'}, {'n': '国外', 'v': 'show_foreign'}]}], 'movie': [{'key': '类型', 'name': '类型', 'value': [{'n': '全部类型', 'v': ''}, {'n': '喜剧', 'v': '喜剧'}, {'n': '爱情', 'v': '爱情'}, {'n': '动作', 'v': '动作'}, {'n': '科幻', 'v': '科幻'}, {'n': '动画', 'v': '动画'}, {'n': '悬疑', 'v': '悬疑'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '惊悚', 'v': '惊悚'}, {'n': '冒险', 'v': '冒险'}, {'n': '音乐', 'v': '音乐'}, {'n': '历史', 'v': '历史'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '恐怖', 'v': '恐怖'}, {'n': '战争', 'v': '战争'}, {'n': '传记', 'v': '传记'}, {'n': '歌舞', 'v': '歌舞'}, {'n': '武侠', 'v': '武侠'}, {'n': '情色', 'v': '情色'}, {'n': '灾难', 'v': '灾难'}, {'n': '西部', 'v': '西部'}, {'n': '纪录片', 'v': '纪录片'}, {'n': '短片', 'v': '短片'}]}, {'key': '地区', 'name': '地区', 'value': [{'n': '全部地区', 'v': ''}, {'n': '华语', 'v': '华语'}, {'n': '欧美', 'v': '欧美'}, {'n': '韩国', 'v': '韩国'}, {'n': '日本', 'v': '日本'}, {'n': '中国大陆', 'v': '中国大陆'}, {'n': '美国', 'v': '美国'}, {'n': '中国香港', 'v': '中国香港'}, {'n': '中国台湾', 'v': '中国台湾'}, {'n': '英国', 'v': '英国'}, {'n': '法国', 'v': '法国'}, {'n': '德国', 'v': '德国'}, {'n': '意大利', 'v': '意大利'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '印度', 'v': '印度'}, {'n': '泰国', 'v': '泰国'}, {'n': '俄罗斯', 'v': '俄罗斯'}, {'n': '加拿大', 'v': '加拿大'}, {'n': '澳大利亚', 'v': '澳大利亚'}, {'n': '爱尔兰', 'v': '爱尔兰'}, {'n': '瑞典', 'v': '瑞典'}, {'n': '巴西', 'v': '巴西'}, {'n': '丹麦', 'v': '丹麦'}]}, {'key': 'sort', 'name': '排序', 'value': [{'n': '近期热度', 'v': 'T'}, {'n': '首映时间', 'v': 'R'}, {'n': '高分优先', 'v': 'S'}]}, {'key': '年代', 'name': '年代', 'value': [{'n': '全部年代', 'v': ''}, {'n': '2020年代', 'v': '2020年代'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2010年代', 'v': '2010年代'}, {'n': '2000年代', 'v': '2000年代'}, {'n': '90年代', 'v': '90年代'}, {'n': '80年代', 'v': '80年代'}, {'n': '70年代', 'v': '70年代'}, {'n': '60年代', 'v': '60年代'}, {'n': '更早', 'v': '更早'}]}], 'tv': [{'key': '类型', 'name': '类型', 'value': [{'n': '不限', 'v': ''}, {'n': '电视剧', 'v': '电视剧'}, {'n': '综艺', 'v': '综艺'}]}, {'key': '电视剧形式', 'name': '电视剧形式', 'value': [{'n': '不限', 'v': ''}, {'n': '喜剧', 'v': '喜剧'}, {'n': '爱情', 'v': '爱情'}, {'n': '悬疑', 'v': '悬疑'}, {'n': '动画', 'v': '动画'}, {'n': '武侠', 'v': '武侠'}, {'n': '古装', 'v': '古装'}, {'n': '家庭', 'v': '家庭'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '科幻', 'v': '科幻'}, {'n': '恐怖', 'v': '恐怖'}, {'n': '历史', 'v': '历史'}, {'n': '战争', 'v': '战争'}, {'n': '动作', 'v': '动作'}, {'n': '冒险', 'v': '冒险'}, {'n': '传记', 'v': '传记'}, {'n': '剧情', 'v': '剧情'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '惊悚', 'v': '惊悚'}, {'n': '灾难', 'v': '灾难'}, {'n': '歌舞', 'v': '歌舞'}, {'n': '音乐', 'v': '音乐'}]}, {'key': '综艺形式', 'name': '综艺形式', 'value': [{'n': '不限', 'v': ''}, {'n': '真人秀', 'v': '真人秀'}, {'n': '脱口秀', 'v': '脱口秀'}, {'n': '音乐', 'v': '音乐'}, {'n': '歌舞', 'v': '歌舞'}]}, {'key': '地区', 'name': '地区', 'value': [{'n': '全部地区', 'v': ''}, {'n': '华语', 'v': '华语'}, {'n': '欧美', 'v': '欧美'}, {'n': '国外', 'v': '国外'}, {'n': '韩国', 'v': '韩国'}, {'n': '日本', 'v': '日本'}, {'n': '中国大陆', 'v': '中国大陆'}, {'n': '中国香港', 'v': '中国香港'}, {'n': '美国', 'v': '美国'}, {'n': '英国', 'v': '英国'}, {'n': '泰国', 'v': '泰国'}, {'n': '中国台湾', 'v': '中国台湾'}, {'n': '意大利', 'v': '意大利'}, {'n': '法国', 'v': '法国'}, {'n': '德国', 'v': '德国'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '俄罗斯', 'v': '俄罗斯'}, {'n': '瑞典', 'v': '瑞典'}, {'n': '巴西', 'v': '巴西'}, {'n': '丹麦', 'v': '丹麦'}, {'n': '印度', 'v': '印度'}, {'n': '加拿大', 'v': '加拿大'}, {'n': '爱尔兰', 'v': '爱尔兰'}, {'n': '澳大利亚', 'v': '澳大利亚'}]}, {'key': 'sort', 'name': '排序', 'value': [{'n': '近期热度', 'v': 'T'}, {'n': '首播时间', 'v': 'R'}, {'n': '高分优先', 'v': 'S'}]}, {'key': '年代', 'name': '年代', 'value': [{'n': '全部', 'v': ''}, {'n': '2020年代', 'v': '2020年代'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2010年代', 'v': '2010年代'}, {'n': '2000年代', 'v': '2000年代'}, {'n': '90年代', 'v': '90年代'}, {'n': '80年代', 'v': '80年代'}, {'n': '70年代', 'v': '70年代'}, {'n': '60年代', 'v': '60年代'}, {'n': '更早', 'v': '更早'}]}, {'key': '平台', 'name': '平台', 'value': [{'n': '全部', 'v': ''}, {'n': '腾讯视频', 'v': '腾讯视频'}, {'n': '爱奇艺', 'v': '爱奇艺'}, {'n': '优酷', 'v': '优酷'}, {'n': '湖南卫视', 'v': '湖南卫视'}, {'n': 'Netflix', 'v': 'Netflix'}, {'n': 'HBO', 'v': 'HBO'}, {'n': 'BBC', 'v': 'BBC'}, {'n': 'NHK', 'v': 'NHK'}, {'n': 'CBS', 'v': 'CBS'}, {'n': 'NBC', 'v': 'NBC'}, {'n': 'tvN', 'v': 'tvN'}]}], 'rank_list_movie': [{'key': '榜单', 'name': '榜单', 'value': [{'n': '实时热门电影', 'v': 'movie_real_time_hotest'}, {'n': '一周口碑电影榜', 'v': 'movie_weekly_best'}, {'n': '豆瓣电影Top250', 'v': 'movie_top250'}]}], 'rank_list_tv': [{'key': '榜单', 'name': '榜单', 'value': [{'n': '实时热门电视', 'v': 'tv_real_time_hotest'}, {'n': '华语口碑剧集榜', 'v': 'tv_chinese_best_weekly'}, {'n': '全球口碑剧集榜', 'v': 'tv_global_best_weekly'}, {'n': '国内口碑综艺榜', 'v': 'show_chinese_best_weekly'}, {'n': '国外口碑综艺榜', 'v': 'show_global_best_weekly'}]}]}
            maxYear = float('-inf')
            for tv in result['filters']['tv']:
                if tv['key'] == '年代':
                    for item in tv['value']:
                        v = item['v']
                        if v.isnumeric():
                            numericValue = int(v)
                            maxYear = max(maxYear, numericValue)
                    for year in range(currentYear, 0, -1):
                        if year > maxYear:
                            pos = tv['value'].index({'n': str(maxYear), 'v': str(maxYear)})
                            tv['value'].insert(pos, {'n': str(year), 'v': str(year)})
                        else:
                            break
                    break
            for movie in result['filters']['movie']:
                if movie['key'] == '年代':
                    for item in movie['value']:
                        v = item['v']
                        if v.isnumeric():
                            numericValue = int(v)
                            maxYear = max(maxYear, numericValue)
                    for year in range(currentYear, 0, -1):
                        if year > maxYear:
                            pos = movie['value'].index({'n': str(maxYear), 'v': str(maxYear)})
                            movie['value'].insert(pos, {'n': str(year), 'v': str(year)})
                        else:
                            break
                    break
        return result

    def categoryContent(self, cid, page, filter, ext):
        from re import sub
        page = int(page)
        result = {}
        videos = []
        header = {
            'Content-Type': 'application/json',
            'Host': 'frodo.douban.com', 'Connection': 'Keep-Alive',
            'Referer': 'https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat'}
        if cid == 'hot_gaia':
            if 'area' in ext.keys():
                area = ext['area']
            else:
                area = '全部'
            if 'sort' in ext.keys():
                sort = ext['sort']
            else:
                sort = 'recommend'
            params = {'area': area, 'sort': sort, 'start': ((int(page) - 1) * 30), 'count': 30, 'apikey': '0ac44ae016490db2204ce0a042db2916'}
            url = f'https://frodo.douban.com/api/v2/movie/{cid}?'
            for key in params:
                url += f'&{key}={params[key]}'
            append = 'items'
        elif cid == 'tv_hot' or cid == 'show_hot':
            if 'type' in ext.keys():
                cid = ext['type']
            url = f'https://frodo.douban.com/api/v2/subject_collection/{cid}/items?'
            params = {'start': (int(page) - 1) * 30, 'count': 30, 'apikey': '0ac44ae016490db2204ce0a042db2916'}
            for key in params:
                url += f'&{key}={params[key]}'
            append = 'subject_collection_items'
        elif cid == 'tv' or cid == 'movie':
            tags = ''
            tagsList = []
            if '类型' in ext.keys():
                movieType = ext['类型']
            else:
                movieType = ''
            if '地区' in ext.keys():
                area = ext['地区']
            else:
                area = ''
            if 'sort' in ext.keys():
                sort = ext['sort']
            else:
                sort = 'T'
            selectedCategories = {"类型": movieType, "地区": area}
            for key in ext:
                if '形式' in key:
                    selectedCategories.update({key: ext[key]})
                if key == 'sort':
                    continue
                tagsList.append(ext[key])
            tagsList = [item for item in tagsList if item != '']
            if len(tagsList) == 1:
                tags = tagsList[0]
            elif len(tagsList) > 1:
                tags = json.dumps(tagsList, ensure_ascii=False)
            url = f'https://frodo.douban.com/api/v2/{cid}/recommend?'
            params = {'tags': tags, 'sort': sort, 'refresh': 0, 'selected_categories': json.dumps(selectedCategories, ensure_ascii=False), 'start': (int(page) - 1) * 30, 'count': 30, 'apikey': '0ac44ae016490db2204ce0a042db2916'}
            for key in params:
                url += f'&{key}={params[key]}'
            append = 'items'
        else:
            if '榜单' in ext.keys():
                cid = ext['榜单']
            else:
                cid = cid.split('_')[2] + '_real_time_hotest'
            url = f'https://frodo.douban.com/api/v2/subject_collection/{cid}/items?'
            params = {'start': ((int(page) - 1) * 30), 'count': 30, 'apikey': '0ac44ae016490db2204ce0a042db2916'}
            for key in params:
                url += f'&{key}={params[key]}'
            append = 'subject_collection_items'
        data = self.fetch(url, headers=header, verify=False, timeout=5).json()
        for video in data[append]:
            vid = video['id']
            if not vid.isnumeric():
                continue
            img = sub(r'photo/(.*?)/', 'photo/l/', video['pic']['large']) + '@User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36@Referer=https://www.douban.com/'
            name = video['title'].strip()
            try:
                remark = video['rating']['value']
            except:
                remark = video['episodes_info']
            if remark != '':
                remark = '{}分'.format(remark)
            else:
                remark = '暂无评分'
            videos.append({
                "vod_db_id": vid,
                "vod_name": name,
                "vod_pic": img,
                "vod_remarks": remark
            })
        lenvodList = len(videos)
        if page * 30 < data['total']:
            pagecount = page + 1
        else:
            pagecount = page
        result['list'] = videos
        result['page'] = page
        result['pagecount'] = pagecount
        result['limit'] = lenvodList
        result['total'] = lenvodList
        return result

    def detailContent(self, did):
        name = ''
        did = did[0]
        if '###' in did:
            idsList = did.split('###')
            tag = idsList[0]
            tid = idsList[1]
            if tag == 'wogg':
                if '---' in tid:
                    tids = tid.split('---')
                    tid = tids[0]
                    name = tids[1]
                if not 'www.aliyundrive.com' in tid:
                    url = 'http://wogg.xyz/index.php/voddetail/{}.html'.format(tid)
                    r = self.fetch(url, headers={"User-Agent": "okhttp/3.12.13"}, verify=False)
                    m = self.regStr(reg='https://www.aliyundrive.com/s/[^"]+', src=r.text.replace('www.alipan.com', 'www.aliyundrive.com'), group=0)
                else:
                    m = self.regStr(reg='https://www.aliyundrive.com/s/[^"]+', src=tid.replace('www.alipan.com', 'www.aliyundrive.com'), group=0)
                tid = m.replace('\\', '')
            elif tag == 'ps':
                if '---' in tid:
                    tids = tid.split('---')
                    tid = tids[0]
                    name = tids[1]
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'Referer': 'https://www.alipansou.com' + '/s/' + tid
                }
                r = self.fetch('https://www.alipansou.com' + '/cv/' + tid, allow_redirects=False, headers=header, timeout=5)
                tid = self.regStr(r.text.replace('www.alipan.com', 'www.aliyundrive.com'), 'https://www.aliyundrive.com/s/[^"]+', 0).replace('\\', '')
            elif tag == 'cz':
                header = {
                    'Referer': 'https://www.czzy88.com/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
                }
                url = 'https://www.czzy88.com/' + tid + '.html'
                r = self.getContent({'pf': 'cz', 'url': url}, header)
                html = self.html(r.content.decode())
                name = self.xpText(html, "//div[contains(@class,'moviedteail_tt')]/h1/text()")
                pic = self.xpText(html, "//div[contains(@class,'dyimg')]/img/@src")
                content = self.xpText(html, "//div[contains(@class,'yp_context')]/text()").strip().replace('\t\t', '')
                vodList = {
                    'vod_id': did,
                    'vod_name': name,
                    'vod_pic': pic,
                    'vod_content': content,
                    'vod_play_from': '厂长'
                }
                playUrl = ''
                playInfosList = html.xpath("//div[contains(@class,'paly_list_btn')]/a")
                i = 0
                for playInfos in playInfosList:
                    i += 1
                    playUrl += '#' + self.xpText(playInfos, "./text()").replace('\xa0', '') + '$' + self.xpText(playInfos, "./qyg5.js") + '---{}---{}'.format(name, i)
                vodList['vod_play_url'] = playUrl.strip('#')
                result = {'list': [vodList]}
                return result
        else:
            tid = did
        if 'www.aliyundrive.com' in tid or 'www.alipan.com' in tid:
            tid = tid.replace('www.alipan.com', 'www.aliyundrive.com')
            if '---' in tid:
                tids = tid.split('---')
                tid = tids[0]
                name = tids[1]
            shareId = self.regStr(reg='www.aliyundrive.com\\/s\\/([^\\/]+)(\\/folder\\/([^\\/]+))?', src=tid, group=1)
            fileId = self.regStr(reg='www.aliyundrive.com\\/s\\/([^\\/]+)(\\/folder\\/([^\\/]+))?', src=tid, group=3)
            url = 'https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous'
            params = {'share_id': shareId}
            data = self.postJson(url, json=params, headers=self.header, verify=False, timeout=5).json()
            fileInfos = []
            if 'file_infos' in data:
                fileInfos = data['file_infos']
            if len(fileInfos) <= 0:
                return {'list': [], 'msg': '分享链接已失效'}
            fileInfo = fileInfos[0]
            if fileId == None or len(fileId) <= 0:
                fileId = fileInfo['file_id']
            if name == '':
                name = data['share_name']
            vodList = {
                'vod_id': tid,
                'vod_name': name,
                'vod_pic': data['avatar'],
                'vod_content': tid,
                'vod_play_from': '原画$$$普画'
            }
            fileType = fileInfo['type']
            if fileType != 'folder':
                if fileType != 'file' or fileInfo['category'] != 'video':
                    return {'list': [], 'msg': '分享链接已失效'}
                fileId = 'root'
            shareToken = self.getshareToken(shareId, '')
            itemsDict = self.listFiles({}, shareId, fileId, shareToken)
            if len(itemsDict) == 0:
                return {'list': [], 'msg': '无可播放资源'}
            itemsDict = sorted(itemsDict.items(), key=lambda x: x[0])
            videoList = []
            playList = []
            for item in itemsDict:
                videoList.append(item[0] + '$' + '{}---'.format(name) + quote(item[1]))
            playList.append('#'.join(videoList))
            vodList['vod_play_url'] = '$$$'.join(playList + playList)
            result = {
                'list': [vodList]
            }
        else:
            url = tid.replace('#', '***')
            vodList = {
                'vod_id': tid,
                'vod_name': tid,
                'vod_content': tid,
                'vod_play_from': '直链$$$嗅探$$$解析',
                'vod_play_url': '推送${}$$$推送${}$$$推送${}'.format(url, url, url)
            }
            result = {'list': [vodList]}
        return result

    def playerContent(self, flag, pid, vipFlags):
        result = {}
        pid = pid.replace('***', '#')
        result["url"] = pid
        if flag == '原画':
            name = pid.split('---')[0]
            pos = pid.split('---')[1]
            pid = pid.split('---')[2]
            params = self.getDanmaku(name, pos)
            result = self.ognContent(flag, pid)
            if params:
                danmuUrl = f'https://api-lmteam.koyeb.app/danmu?params={quote(json.dumps(params))}'
                result['danmaku'] = danmuUrl
            return result
        elif flag == '普画':
            name = pid.split('---')[0]
            pos = pid.split('---')[1]
            pid = pid.split('---')[2]
            params = self.getDanmaku(name, pos)
            result = self.fhdContent(flag, pid)
            if params:
                danmuUrl = f'https://api-lmteam.koyeb.app/danmu?params={quote(json.dumps(params))}'
                result['danmaku'] = danmuUrl
            return result
        elif flag == '直链':
            result["parse"] = 0
        elif flag == '嗅探':
            result["parse"] = 1
        elif flag == '解析':
            result["jx"] = 1
        elif flag == '厂长':
            result["parse"] = 0
            header = {
                'Referer': 'https://www.czzy88.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }
            url = pid.split('---')[0]
            name = pid.split('---')[1]
            pos = pid.split('---')[2]
            params = self.getDanmaku(name, pos)
            if params:
                danmuUrl = f'https://api-lmteam.koyeb.app/danmu?params={quote(json.dumps(params))}'
                result['danmaku'] = danmuUrl
            r = self.getContent({'pf': 'cz', 'url': url}, header)
            try:
                b64 = self.regStr(reg='\"([^\"]+)\";var [\d\w]+=function dncry.*md5.enc.Utf8.parse\(\"([\d\w]+)\".*md5.enc.Utf8.parse\(([\d]+)\)', src=r.text, group=1)
                key = self.regStr(reg='\"([^\"]+)\";var [\d\w]+=function dncry.*md5.enc.Utf8.parse\(\"([\d\w]+)\".*md5.enc.Utf8.parse\(([\d]+)\)', src=r.text, group=2).encode()
                iv = self.regStr(reg='\"([^\"]+)\";var [\d\w]+=function dncry.*md5.enc.Utf8.parse\(\"([\d\w]+)\".*md5.enc.Utf8.parse\(([\d]+)\)', src=r.text, group=3).encode()
                enc = b64decode(b64)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                data = cipher.decrypt(enc)
                content = data[:-data[-1]].decode()
                playUrl = self.regStr(reg='video: *\{url: *\"([^\"]+)\"', src=content)
                subUrl = self.regStr(reg='subtitle: *\{url: *\"([^\"]+)\"', src=content)
                if len(subUrl) > 0:
                    result['subs'] = [{'url': subUrl, 'name': 'czspp'}]
            except:
                url = self.regStr(reg='<iframe.*?src=\"(.*?)\".*?</iframe>', src=r.text)
                header.update({'sec-ch-ua-platform': '"Windows"', 'Sec-Fetch-Dest': "iframe", 'Sec-Fetch-Mode': "navigate", 'Sec-Fetch-Site': "cross-site", "Upgrade-Insecure-Requests": "1", "sec-ch-ua-mobile": "?0", "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"', "Cookies": 'DNT=1'})
                r = self.getContent({'pf': 'cz', 'url': url}, header)
                try:
                    b64 = self.regStr(reg='var rand = \"(.*?)\".*var player = \"(.*?)\"', src=r.text.replace('\n', ''), group=2)
                    iv = self.regStr(reg='var rand = \"(.*?)\".*var player = \"(.*?)\"', src=r.text.replace('\n', ''), group=1).encode()
                    enc = b64decode(b64)
                    cipher = AES.new('VFBTzdujpR9FWBhe'.encode(), AES.MODE_CBC, iv)
                    data = cipher.decrypt(enc)
                    content = data[:-data[-1]].decode()
                    playUrl = json.loads(content)['url']
                except:
                    playUrl = ''
                    content = self.regStr(r.text.replace('\n', ''), '\"data\":\"(.*?)\"')[::-1]
                    for i in range(0, len(content), 2):
                        combinedChars = content[i] + content[i + 1]
                        decimalValue = int(combinedChars, 16)
                        playUrl += chr(decimalValue)
                    pos = int((len(playUrl) - 7) / 2)
                    playUrl = playUrl[:pos] + playUrl[pos + 7:]
            result["url"] = playUrl
        else:
            result = {}
        return result

    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def searchContentPage(self, key, quick, page):
        self.fileidList = []
        self.shareidList = []
        page = int(page)
        items = []
        keyword = key
        if page == 1:
            siteList = ['cz', 'ps', 'zt', 'xy', 'wogg']
        else:
            siteList = self.getCache('alisiteList_{}_{}'.format(keyword, page))
            self.delCache('alisiteList_{}_{}'.format(keyword, page))
            if not siteList:
                return {'list': items}

        contents = []
        if quick:
            siteList = ['cz']

        with ThreadPoolExecutor(max_workers=5) as executor:
            searchList = []
            try:
                for site in siteList:
                    tag = site
                    future = executor.submit(self.runSearch, key, tag, page)
                    searchList.append(future)
                for result in as_completed(searchList, timeout=10):
                    contents.append(result.result())
            except:
                pass
            finally:
                executor.shutdown(wait=False)
        nextpageList = []
        for content in contents:
            if content is None:
                continue
            contkey = list(content.keys())[0]
            infos = content[contkey]
            items = items + content[contkey][0]
            nextpageList.append(infos[1])
            if not infos[1]:
                siteList.remove(contkey)
        self.setCache('alisiteList_{}_{}'.format(keyword, page+1), siteList)
        result = {
            'list': items,
            'hasNext': True in nextpageList
        }
        return result

    def runSearch(self, key, tag, pg):
        try:
            defname = 'self.search' + tag
            result = eval(defname)(key, tag, pg)
            return result
        except Exception as e:
            return {tag: [[], False]}

    def searchcz(self, key, tag, pg):
        items = []
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37"
        }
        r = self.post('https://ymck.pro/API/v2.php', headers=header, data={'q': key, 'size': 25}, timeout=5, verify=False)
        vList = json.loads(b64decode(self.cleanText(r.text)))[1:]
        vidList = []
        for video in vList[1:]:
            if 'website' not in video or video['website'] != '厂长资源':
                continue
            name = video['text']
            vid = self.regStr(reg='http.*?//.*?/(\S+/.*?).html', src=video['url'])
            if vid in vidList:
                continue
            else:
                vidList.append(vid)
            items.append({
                'vod_id': 'cz###' + vid,
                'vod_name': name,
                "vod_remarks": '厂长'
            })
        return {tag: [items, False]}

    def searchps(self, key, tag, pg):
        pg = int(pg)
        items = []
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37",
            # "Content-Type": "text/html; charset=UTF-8",
            "Referer": "https://www.alipansou.com/"
        }
        r = self.fetch(f'https://www.alipansou.com/search?page={pg}&k={key}&t=7', headers=header, verify=False, timeout=5)
        html = self.html(self.cleanText(r.content.decode('utf-8')))
        vList = html.xpath("//van-row/a")
        for video in vList:
            href = self.xpText(video, "./qyg5.js")
            if 'xunlei' in href:
                continue
            vid = self.regStr(reg=r'/s/(.*)', src=href)
            nameElement = self.xpText(video, ".//template/div")
            name = ''.join(nameElement.xpath('./qyg0.js')).strip()
            if name.count(key) > 1 or len(name) - len(key) > 10:
                name = ''.join(OrderedDict.fromkeys(name))
            if SequenceMatcher(None, name, key).ratio() < 0.6 and not key in name:
                continue
            items.append({
                'vod_id': 'ps###' + vid + "---{}".format(key),
                'vod_name': name,
                'vod_pic': './qyg6.png',
                "vod_remarks": '阿里盘搜'
            })
        try:
            maxPage = int(self.xpText(html, ".//van-row/van-col/van-pagination/@page-count"))
        except:
            maxPage = pg
        if len(items) == 0:
            maxPage = pg
        return {tag: [items, pg < maxPage]}

    def searchzt(self, key, tag, pg):
        items = []
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37",
            "Referer": "http://a.gitcafe.net/"
        }
        params = {
            "action": "search",
            "from": "web",
            "token": "c128f28b5aca32c462c6bb0e032e77ebacca8c",
            "keyword": key
        }
        r = self.post('https://gitcafe.net/tool/alipaper/', data=params, headers=header, timeout=5)
        vList = json.loads(self.cleanText(r.text))['data']
        for video in vList:
            if video['alikey'] in self.shareidList:
                continue
            self.shareidList.append(video['alikey'])
            name = video['title']
            if len(name) > len(key) + 20:
                name = ''.join(OrderedDict.fromkeys(name))
            items.append({
                'vod_id': 'https://www.aliyundrive.com/s/' + video['alikey'] + "---{}".format(key),
                'vod_name': name,
                'vod_pic': './qyg6.png',
                "vod_remarks": '阿里纸条'
            })
        return {tag: [items, False]}

    def searchxy(self, key, tag, pg):
        items = []
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": f"http://www.yunso.net/index/user/s?wd={quote(key)}"
        }
        r = self.post(f'http://www.yunso.net/api/validate/search?wd={key}&page={pg}&uk=&mode=90001&stype=20100&scope_content=', data=f'/api/validate/search?wd={key}&page={pg}&uk=&mode=90001&stype=20100&scope_content=', verify=False, headers=header, timeout=5)
        data = json.loads(self.cleanText(r.text))
        html = self.html(data['data'].replace('</>', ''))
        vList = html.xpath("//div[contains(@class,'layui-card-header')]")
        count = 0
        for video in vList:
            name = self.xpText(video, './qyg1.js').strip()
            if name.count(key) > 1 or len(name) > len(key) + 20:
                name = ''.join(OrderedDict.fromkeys(name))
            vid = b64decode(self.xpText(video, './qyg2.js')).decode().replace('www.alipan.com', 'www.aliyundrive.com')
            if 'www.aliyundrive.com' not in vid:
                continue
            shareId = self.regStr(vid, 'www.aliyundrive.com\/s\/([^\/]+)(\/folder\/([^\/]+))?')
            if shareId not in self.shareidList:
                self.shareidList.append(shareId)
            else:
                count += 1
                continue
            items.append({
                'vod_id': vid + "---{}".format(key),
                'vod_name': name,
                'vod_pic': './qyg6.png',
                "vod_remarks": '阿里小云'
            })
        return {tag: [items, len(items) + count == 20]}

    def searchwogg(self, key, tag, pg):
        pg = int(pg)
        items = []
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
        url = 'http://wogg.xyz/index.php/vodsearch/{}----------{}---.html'.format(key, pg)
        r = self.fetch(url, headers=header, verify=False, timeout=5)
        html = self.html(self.cleanText(r.text))
        vList = html.xpath("//div[contains(@class,'module-items')]/div")
        nextpage = True
        for video in vList:
            img = self.xpText(video, './qyg3.js')
            if not img.startswith('http'):
                img = self.regStr(img, '\((http.*?)\)')
            title = self.xpText(video, './qyg4.js').strip()
            vid = self.xpText(video, ".//div[contains(@class,'video-info-footer')]/a/@href")
            vid = self.regStr(vid, '/(\d+)\.html')
            items.append({
                'vod_id': 'wogg###' + vid + "---{}".format(key),
                'vod_name': title,
                'vod_pic': img,
                "vod_remarks": '阿里玩偶哥哥'
            })
        maxPageLiset = html.xpath(".//div[@id='page']/a")
        if maxPageLiset != []:
            maxPage = self.xpText(maxPageLiset[-1], './qyg5.js')
            maxPage = self.regStr(maxPage, '-(\d+)-')
            if pg == int(maxPage):
                nextpage = False
        else:
            nextpage = False
        return {tag: [items, nextpage]}

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None

    def ognContent(self, flag, oid):
        oid = unquote(oid)
        ids = oid.split('+')
        shareId = ids[0]
        fileId = ids[2]
        if 'thread' in self.extendDict:
            thread = self.extendDict['thread']
        else:
            thread = '0'
        token = self.extendDict['token']
        if token.startswith('http'):
            token = quote(token)
        subtitleList = self.subtitleContent(oid)
        result = {
            'parse': '0',
            'playUrl': '',
            'url': f"http://127.0.0.1:UndCover/proxy?do=py&type=media&shareId={shareId}&fileId={fileId}&token={token}&thread={thread}",
            'header': self.header,
            'subs': subtitleList
        }
        return result

    def fhdContent(self, flag, fid):
        fid = unquote(fid)
        ids = fid.split('+')
        shareId = ids[0]
        fileId = ids[2]
        token = self.extendDict['token']
        if token.startswith('http'):
            token = quote(token)
        subtitleList = self.subtitleContent(fid)
        result = {
            'parse': '0',
            'playUrl': '',
            'url': f"http://127.0.0.1:UndCover/proxy?do=py&type=m3u8&shareId={shareId}&fileId={fileId}&token={token}",
            'header': self.header,
            'subs': subtitleList
        }
        return result

    def subtitleContent(self, sid):
        ids = sid.split('+')
        shareId = ids[0]
        shareToken = ids[1]
        subtitle = ids[4]
        token = self.extendDict['token']
        if token.startswith('http'):
            token = quote(token)
        if len(subtitle) == 0:
            return []
        tokenDict = self.getToken(self.extendDict['token'])
        header = self.header.copy()
        header['Content-Type'] = 'application/json'
        header['x-share-token'] = shareToken
        header['authorization'] = tokenDict['authorization']
        subtitleList = subtitle.strip("&&&").split('&&&')
        subs = []
        for sub in subtitleList:
            subList = sub.split('###')
            subname = subList[0]
            if subname.split('.')[-1].lower() == 'ssa' or subname.split('.')[-1].lower() == 'ass':
                subformat = 'text/x-ssa'
            elif subname.split('.')[-1].lower() == 'srt':
                subformat = 'application/x-subrip'
            elif subname.split('.')[-1].lower() == 'vtt':
                subformat = 'text/vtt'
            else:
                subformat = 'text/plain'
            fileId = subList[1]
            subs.append({'url': f"http://127.0.0.1:UndCover/proxy?do=py&type=media&shareId={shareId}&fileId={fileId}&token={token}&subformat{subformat}", 'name': subname, 'format': subformat})
        return subs

    def delFiles(self, header, toDriveId, tempidsList):
        delidsList = []
        for fileId in tempidsList:
            jsonStr = '{\"requests\":[{\"body\":{\"drive_id\":\"%s\",\"file_id\":\"%s\"},\"headers\":{\"Content-Type\":\"application/json\"},\"id\":\"%s\",\"method\":\"POST\",\"url\":\"/file/delete\"}],\"resource\":\"file\"}' % (toDriveId, fileId, fileId)
            r = self.post('https://api.aliyundrive.com/v3/batch', data=jsonStr, headers=header, verify=False, timeout=5)
            if r.status_code == 200 and r.json()['responses'][0]['status'] == 404:
                delidsList.append(fileId)
        for fileId in delidsList:
            tempidsList.remove(fileId)
        if tempidsList != []:
            self.setCache('tempidsList', tempidsList)
        else:
            self.delCache('tempidsList')

    def proxyMedia(self, params):
        thread = 0
        downloadUrl = ''
        token = params['token']
        fileId = params['fileId']
        shareId = params['shareId']
        if 'thread' in params:
            thread = int(params['thread'])
        tokenDict = self.getToken(token, True)
        shareToken = self.getshareToken(shareId, '')
        header = self.header.copy()
        header['Content-Type'] = 'application/json'
        header['x-share-token'] = shareToken
        header['authorization'] = tokenDict['authorization']
        toDriveId = tokenDict['drive_id']
        tempidsList = self.getCache('tempidsList')
        if not tempidsList:
            tempidsList = []
        if tempidsList != []:
            self.delFiles(header, toDriveId, tempidsList)
        key = f'alidownloadUrl_{shareId}_{fileId}'
        data = self.getCache(key)
        if data and 'downloadUrl' in data:
            header = self.header.copy()
            if 'range' in params:
                header['Range'] = params['range']
            contentType = data['contentType']
            if contentType == "video/MP2T":
                action = {'url': data['downloadUrl'], 'header': header, 'param': '', 'type': 'redirect'}
                return [302, contentType, action, data['downloadUrl']]
            action = {'url': data['downloadUrl'], 'header': header, 'param': '', 'type': 'stream'}
            return [206, "application/octet-stream", action, '']

        code = 200
        contentType = "application/octet-stream"
        if tokenDict['open_token'] == '':
            thread = 10
        if 'thread' in params:
            thread = int(params['thread'])
        if thread == 0:
            code = 206
            contentType = "application/octet-stream"
            try:
                jsonStr = "{\"requests\":[{\"body\":{\"file_id\":\"%s\",\"share_id\":\"%s\",\"auto_rename\":true,\"to_parent_file_id\":\"root\",\"to_drive_id\":\"%s\"},\"headers\":{\"Content-Type\":\"application/json\"},\"id\":\"0\",\"method\":\"POST\",\"url\":\"/file/copy\"}],\"resource\":\"file\"}" % (fileId, shareId, toDriveId)
                r = self.post('https://api.aliyundrive.com/v3/batch', data=jsonStr, headers=header, verify=False, timeout=5)
                if r.status_code == 400:
                    r = self.post('https://user.aliyundrive.com/v2/user/get', headers=header, verify=False)
                    toDriveId = r.json()['resource_drive_id']
                    jsonStr = "{\"requests\":[{\"body\":{\"file_id\":\"%s\",\"share_id\":\"%s\",\"auto_rename\":true,\"to_parent_file_id\":\"root\",\"to_drive_id\":\"%s\"},\"headers\":{\"Content-Type\":\"application/json\"},\"id\":\"0\",\"method\":\"POST\",\"url\":\"/file/copy\"}],\"resource\":\"file\"}" % (fileId, shareId, toDriveId)
                    r = self.post('https://api.aliyundrive.com/v3/batch', data=jsonStr, headers=header, verify=False, timeout=5)
                myFileId = r.json()['responses'][0]['body']['file_id']
                tempidsList.append(myFileId)
                header['authorization'] = tokenDict['open_authorization']
                data = self.postJson('https://open.aliyundrive.com/adrive/v1.0/openFile/getDownloadUrl',
                                  json={
                                      "expire_sec": 115200,
                                      'file_id': myFileId,
                                      'drive_id': toDriveId
                                  },
                                  headers=header,
                                  verify=False,
                                  timeout=5).json()
                downloadUrl = data['url']
                try:
                    if 'auth_key=' in downloadUrl:
                        expiresAt = int(self.regStr(reg="auth_key=(\d+)-", src=downloadUrl)) - 60
                    elif 'x-oss-expires=' in downloadUrl:
                        expiresAt = int(self.regStr(reg="x-oss-expires=(\d+)", src=downloadUrl)) - 60
                    else:
                        expiresAt = int(time.time()) - 60
                except:
                    expiresAt = int(time.time()) - 60
                self.setCache(key, {"thread": 0, 'downloadUrl': downloadUrl, 'expiresAt': expiresAt, 'shareId': shareId, 'fileId': fileId, "contentType": contentType})
            except:
                if 'thread' in params and int(params['thread']) != 0:
                    thread = int(params['thread'])
                else:
                    thread = 10
            finally:
                if tempidsList != []:
                    header['authorization'] = tokenDict['authorization']
                    self.delFiles(header, toDriveId, tempidsList)
        if thread > 0:
            code = 302
            contentType = "video/MP2T"
            header['authorization'] = tokenDict['authorization']
            r = self.postJson(
                'https://api.aliyundrive.com/v2/file/get_share_link_download_url',
                json={
                    'share_id': shareId,
                    'file_id': fileId,
                    "expire_sec": 600,
                },
                headers=header,
                verify=False,
                timeout=5)
            downloadUrl = r.json()['url']
            try:
                if 'auth_key=' in downloadUrl:
                    expiresAt = int(self.regStr(reg="auth_key=(\d+)-", src=downloadUrl)) - 60
                elif 'x-oss-expires=' in downloadUrl:
                    expiresAt = int(self.regStr(reg="x-oss-expires=(\d+)", src=downloadUrl)) - 60
                else:
                    expiresAt = int(time.time()) - 60
            except:
                expiresAt = int(time.time()) - 60
            try:
                # self.fetch('http://192.168.1.254:7777')
                self.fetch('http://127.0.0.1:7777')
            except:
                # self.fetch('http://192.168.1.254:9978/go')
                self.fetch('http://127.0.0.1:9978/go')
            downloadUrl = f'http://127.0.0.1:7777?url={quote(downloadUrl)}&thread={thread}'
            self.setCache(key, {"thread": thread, 'downloadUrl': downloadUrl, 'expiresAt': expiresAt, 'shareId': shareId, 'fileId': fileId, "contentType": contentType})
            action = {'url': downloadUrl, 'header': self.header, 'param': '', 'type': 'redirect'}
            return [code, contentType, action, downloadUrl]
        header = self.header.copy()
        if 'range' in params:
            header['Range'] = params['range']
        action = {'url': downloadUrl, 'header': header, 'param': '', 'type': 'stream'}
        return [code, contentType, action, '']

    def proxyTs(self, params):
        mediaId = params['mediaId']
        _, m3u8Infos = self.getM3u8(params)
        url = m3u8Infos[str(mediaId)]
        if url.count('https') > 1:
            url = self.regStr(url, 'http.*?(http.*?://.*)')
        action = {'url': url, 'header': self.header, 'param': '', 'type': 'stream'}
        return [200, "video/MP2T", action, '']

    def proxyM3u8(self, params):
        content, _ = self.getM3u8(params)
        action = {'url': '', 'header': self.header, 'param': '', 'type': 'string'}
        return [200, "application/vnd.apple.mpegurl", action, content]

    def getM3u8(self, params):
        token = params['token']
        fileId = params['fileId']
        shareId = params['shareId']
        key = f'alim3u8Cache_{fileId}_{shareId}'
        data = self.getCache(key)
        if data:
            return data['content'], data['m3u8Infos']

        tokenDict = self.getToken(token)
        shareToken = self.getshareToken(shareId, '')
        params = {
            "share_id": shareId,
            "category": "live_transcoding",
            "file_id": fileId,
            "template_id": "",
        }
        header = self.header.copy()
        header['x-share-token'] = shareToken
        header['x-device-id'] = tokenDict['device_id']
        header['x-signature'] = tokenDict['signature']
        header['authorization'] = tokenDict['authorization']
        r = self.postJson(
            'https://api.aliyundrive.com/users/v1/users/device/create_session',
            json={
                'deviceName': 'Edge浏览器',
                'modelName': 'Windows网页版',
                'pubKey': tokenDict['public_key'],
            },
            headers=header,
            verify=False,
            timeout=5)
        result = r.json()
        if 'success' not in result or not result['success']:
            return '', {}
        header['authorization'] = tokenDict['authorization']
        url = 'https://api.aliyundrive.com/v2/file/get_share_link_video_preview_play_info'
        data = self.postJson(url, json=params, headers=header, verify=False, timeout=5).json()
        quality = ['UHD', 'QHD', 'FHD', 'HD', 'SD']
        videoList = data['video_preview_play_info']['live_transcoding_task_list']
        url = ''
        for q in quality:
            if len(url) > 0:
                break
            for video in videoList:
                if video['template_id'] == q:
                    url = video['url']
                    break
        r = self.fetch(url, headers=self.header, verify=False, timeout=5)
        host = '/'.join(url.split('/')[0:-1]) + '/'
        m3u8List = []
        m3u8Infos = {}
        slices = r.text.split("\n")
        count = 0
        deadlineList = []
        for mediaSlice in slices:
            if 'auth_key' in mediaSlice or 'x-oss-expires' in mediaSlice:
                try:
                    if 'auth_key=' in mediaSlice:
                        deadline = int(self.regStr(reg="auth_key=(\d+)-", src=mediaSlice))
                    elif 'x-oss-expires=' in mediaSlice:
                        deadline = int(self.regStr(reg="x-oss-expires=(\d+)", src=mediaSlice))
                    else:
                        deadline = int(time.time()) + 660
                except:
                    deadline = int(time.time()) + 660
                deadlineList.append(deadline)
                count += 1
                m3u8Infos[str(count)] = host + mediaSlice
                mediaSlice = f"http://127.0.0.1:UndCover/proxy?do=py&type=ts&shareId={shareId}&fileId={fileId}&token={token}&mediaId={count}"
            m3u8List.append(mediaSlice)
        expiresAt = min(deadlineList) - 60
        content = '\n'.join(m3u8List).strip()
        self.setCache(key, {'content': content, 'm3u8Infos': m3u8Infos, 'expiresAt': expiresAt})
        return content, m3u8Infos

    def getshareToken(self, shareId, sharePwd):
        key = f'shareToken_{shareId}'
        data = self.getCache(key)
        if data:
            return data['share_token']

        params = {
            'share_id': shareId,
            'share_pwd': sharePwd
        }
        url = 'https://api.aliyundrive.com/v2/share_link/get_share_token'
        data = self.postJson(url, json=params, headers=self.header, verify=False, timeout=5).json()
        ShareToken = data['share_token']
        self.setCache(key, {"share_token": ShareToken, "expiresAt": int(time.time()) + data['expires_in'] - 60})
        return ShareToken

    def listFiles(self, resultDict, shareId, fileId, shareToken, dirName='', nextMaker='', subtDict={}, folderList=[]):
        url = 'https://api.aliyundrive.com/adrive/v3/file/list'
        header = self.header.copy()
        header['x-share-token'] = shareToken
        params = {
            'limit': 200,
            'marker': nextMaker,
            'share_id': shareId,
            'order_by': 'updated_at',
            'parent_file_id': fileId,
            'order_direction': 'DESC',
            'image_url_process': 'image/resize,w_1920/format,jpeg',
            'image_thumbnail_process': 'image/resize,w_160/format,jpeg',
            'video_thumbnail_process': 'video/snapshot,t_1000,f_jpg,ar_auto,w_300'
        }
        retry = 0
        while retry <= 5:
            r = self.postJson(url, json=params, headers=header, verify=False, timeout=5)
            if r.status_code == 200:
                break
            retry += 1
        data = r.json()
        nextMaker = data['next_marker']
        if dirName != '':
            dirName = '[' + dirName + ']|'
        pos = 0
        itemsList = sorted(data['items'], key=lambda x: x['name'])
        for item in itemsList:
            if item['type'] == 'folder':
                folder = item['file_id'] + '&&&' + item['name']
                folderList.append(folder)
            else:
                if 'video' in item['mime_type'] or 'video' in item['category']:
                    pos += 1
                    remark = self.getSize(item['size'])
                    resultDictKey = dirName + item['name'].replace("#", "_").replace("$", "_") + remark
                    resultDict[resultDictKey] = str(pos) + '---' + shareId + "+" + shareToken + "+" + item['file_id'] + "+" + item['category'] + "+"
                elif 'others' == item['category'] and item['file_extension'] in ['srt', 'ass', 'ssa', 'vtt']:
                    remark = self.getSize(item['size'])
                    subtDictKey = dirName + item['name'].replace("#", "_").replace("$", "_") + remark
                    subtDict[subtDictKey] = item['file_id']
        if len(nextMaker) > 0:
            self.listFiles(resultDict, shareId, fileId, shareToken, dirName, nextMaker, subtDict, folderList)
        for folder in folderList:
            folderList.remove(folder)
            if '&&&' in folder:
                folderInfos = folder.split('&&&')
                fileId = folderInfos[0]
                dirName = folderInfos[1]
            return self.listFiles(resultDict, shareId, fileId, shareToken, dirName, nextMaker, subtDict, folderList)
        for vkey in resultDict.keys():
            for sKey in subtDict.keys():
                if ']|' in sKey:
                    subKey = sKey.split(']|')[1].split('/[')[0]
                else:
                    subKey = sKey.split('/[')[0]
                if subKey + '###' + subtDict[sKey] + '&&&' not in resultDict[vkey]:
                    resultDict[vkey] = resultDict[vkey] + subKey + '###' + subtDict[sKey] + '&&&'
        return resultDict

    def getSize(self, size):
        size = int(size)
        if size > 1024 * 1024 * 1024 * 1024.0:
            fs = "TB"
            sz = round(size / (1024 * 1024 * 1024 * 1024.0), 2)
        elif size > 1024 * 1024 * 1024.0:
            fs = "GB"
            sz = round(size / (1024 * 1024 * 1024.0), 2)
        elif size > 1024 * 1024.0:
            fs = "MB"
            sz = round(size / (1024 * 1024.0), 2)
        elif size > 1024.0:
            fs = "KB"
            sz = round(size / (1024.0), 2)
        else:
            fs = "KB"
            sz = round(size / (1024.0), 2)
        remark = '/[' + str(sz) + fs + ']'
        return remark

    def getToken(self, token, getOpen=True):
        if token.startswith('http'):
            token = unquote(token)
            header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
            r = self.fetch(url=token, headers=header, verify=False, timeout=5)
            token = r.text.strip()
        tokenDict = self.getCache('aliToken')
        if tokenDict:
            return tokenDict['tokenDict']

        tokenDict = {}
        header = self.header.copy()
        data = self.postJson(url='https://auth.aliyundrive.com/v2/account/token',
                          json={'grant_type': 'refresh_token', 'refresh_token': token},
                          headers=header,
                          verify=False,
                          timeout=5).json()
        tokenDict['token'] = data['refresh_token']
        tokenDict['authorization'] = f"{data['token_type']} {data['access_token']}"
        tokenDict['user_id'] = data['user_id']
        tokenDict['drive_id'] = data['default_drive_id']
        tokenDict['device_id'] = data['device_id']
        tokenDict['export_in'] = data['expires_in']
        header['authorization'] = tokenDict['authorization']
        # 获取 opentoken
        if getOpen:
            try:
                header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) aDrive/4.1.0 Chrome/108.0.5359.215 Electron/22.3.1 Safari/537.36'
                r = self.postJson(
                    url='https://open.aliyundrive.com/oauth/users/authorize?client_id=76917ccccd4441c39457a04f6084fb2f&redirect_uri=https://alist.nn.ci/tool/aliyundrive/callback&scope=user:base,file:all:read,file:all:write&state=',
                    json={
                        'authorize': 1,
                        'scope': 'user:base,file:all:read,file:all:write'
                    },
                    headers=header,
                    verify=False,
                    timeout=5)
                code = self.regStr(r.text, 'code=(.*?)\"')
                data = self.postJson(url='https://api-cf.nn.ci/alist/ali_open/code',
                                  json={
                                      'code': code,
                                      'grant_type': 'authorization_code'
                                  },
                                  headers=header,
                                  verify=False,
                                  timeout=5).json()
                openExportIn = data['expires_in']
                openToken = data['refresh_token']
                opAuthorization = f"{data['token_type']} {data['access_token']}"
            except:
                openToken = ''
                opAuthorization = ''
                openExportIn = 7200
        else:
            openToken = ''
            opAuthorization = ''
            openExportIn = 7200
        tokenDict['open_token'] = openToken
        tokenDict['open_authorization'] = opAuthorization
        tokenDict['expires_at'] = int(int(time.time()) + min(tokenDict['export_in'], openExportIn) / 2)
        # 获取 signature 和 public_key
        params = {"user_id": tokenDict['user_id'], "device_id": tokenDict['device_id']}
        data = self.fetch(f"https://api-lmteam.koyeb.app/proxy?spider=apifan&function=aliSignature&params={quote(json.dumps(params))}").json()
        tokenDict['public_key'] = data['public_key']
        tokenDict['signature'] = data['signature']
        self.setCache('aliToken', {"tokenDict": tokenDict, "expiresAt": tokenDict['expires_at']})
        return tokenDict

    def getDanmaku(self, name, pos):
        info = []
        pos = int(pos)
        pos = pos - 1
        if pos < 0:
            pos = 0
        try:
            url = f'https://api.so.360kan.com/index?force_v=1&kw={name}&from=&pageno=1&v_ap=1&tab=all'
            header = {
                'Referer': 'https://so.360kan.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'}
            r = self.fetch(url, headers=header, timeout=15)
            diffList = []
            vodList = r.json()['data']['longData']['rows']
            for vod in vodList:
                diffList.append(SequenceMatcher(None, vod['titleTxt'], name).ratio())
            diffList.sort(reverse=True)
            for i in range(0, len(diffList)):
                infos = vodList[i]
                enId = infos['en_id']
                catId = infos['cat_id']
                videoType = infos['cat_name']
                if videoType in ["电影", "电视剧"]:
                    if 'seriesPlaylinks' in infos and len(infos['seriesPlaylinks']) != 0:
                        if type(infos['seriesPlaylinks'][-1]) == str:
                            info = infos['seriesPlaylinks'][:-1]
                            info.append({'url': infos['seriesPlaylinks'][-1]})
                        else:
                            info = infos['seriesPlaylinks']
                    else:
                        site = list(infos['playlinks'].keys())[0]
                        if type(infos['playlinks'][site]) == str:
                            info = [{'url': infos['playlinks'][site]}]
                        else:
                            info = infos['playlinks'][site]
                elif videoType == '动漫':
                    site = list(infos['playlinks'].keys())[0]
                    s = quote(f'[{{\"cat_id\": \"{catId}\", \"ent_id\": \"{enId}\", \"site\": \"{site}\"}}]')
                    r = self.fetch(f'https://api.so.360kan.com/episodesv2?v_ap=1&s={s}', headers=header, timeout=15)
                    data = r.json()['data'][0]['seriesHTML']
                    if 'seriesPlaylinks' in data and len(data['seriesPlaylinks']) != 0:
                        if type(data['seriesPlaylinks'][-1]) == str:
                            info = data['seriesPlaylinks'][:-1]
                            info.append({'url': data['seriesPlaylinks'][-1]})
                        else:
                            info = data['seriesPlaylinks']
                    else:
                        if type(data['playlinks'][site]) == str:
                            info = [{'url': data['playlinks'][site]}]
                        else:
                            info = data['playlinks'][site]
                    retry = 0
                    while enId != data['en_id'] and retry < 10:
                        retry += 1
                        site = list(infos['playlinks'].keys())[0]
                        s = quote(f'[{{\"cat_id\": \"{catId}\", \"ent_id\": \"{enId}\", \"site\": \"{site}\"}}]')
                        r = self.fetch(f'https://api.so.360kan.com/episodesv2?v_ap=1&s={s}', headers=header, timeout=15)
                        data = r.json()['data'][0]['seriesHTML']
                        enId = data['en_id']
                        if 'seriesPlaylinks' in data and len(data['seriesPlaylinks']) != 0:
                            if type(data['seriesPlaylinks'][-1]) == str:
                                info.append(data['seriesPlaylinks'][:-1])
                                info.append({'url': data['seriesPlaylinks'][-1]})
                            else:
                                info.append(data['seriesPlaylinks'])
                        else:
                            site = list(data['playlinks'].keys())[0]
                            if type(data['playlinks'][site]) == str:
                                info.append([{'url': data['playlinks'][site]}])
                            else:
                                info.append(data['playlinks'][site])
                elif videoType == '综艺':
                    site = list(infos['playlinks'].keys())[0]
                    enTid = infos['id']
                    year = infos['year']
                    offset = int(infos['playlinks_total'][site]) - 1 - pos
                    if offset >= 5:
                        r = self.fetch(f'https://api.so.360kan.com/episodeszongyi?site={site}&y={year}&entid={enTid}&offset={offset}&count=8', headers=header, timeout=15)
                        data = r.json()['data']['list']
                        if data:
                            pos = 0
                            info = [{'url': data[0]['url']}]
                    else:
                        if 'seriesPlaylinks' in infos and len(infos['seriesPlaylinks']) != 0:
                            if type(infos['seriesPlaylinks'][-1]) == str:
                                info = infos['seriesPlaylinks'][:-1]
                                info.append({'url': infos['seriesPlaylinks'][-1]})
                            else:
                                info = infos['seriesPlaylinks']
                        else:
                            if type(infos['playlinks'][site]) == str:
                                info = [{'url': infos['playlinks'][site]}]
                            else:
                                info = infos['playlinks'][site]
                try:
                    url = info[pos]['url']
                    break
                except:
                    pass
            if 'qq.com' in url:
                params = {'platform': 'qq', 'url': url}
            elif 'mgtv.com' in url:
                params = {'platform': 'mgtv', 'url': url}
            elif 'iqiyi.com' in url:
                params = {'platform': 'iqiyi', 'url': url}
            elif 'youku.com' in url:
                params = {'platform': 'youku', 'url': url}
            elif 'bilibili.com' in url:
                params = {'platform': 'bilibili', 'url': url}
            else:
                return None
            return params
        except:
            pass

    def getContent(self, params, header={}):
        pf = params['pf']
        try:
            if pf == 'cz':
                header = {
                    'Referer': 'https://www.czzy88.com/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                }
                url = params['url']
                data = self.getCache('czCookie')
                if data:
                    cookie = data['cookieDict'].copy()
                    r = self.fetch(params['url'], headers=header, verify=False, cookies=cookie, timeout=5)
                    if 'huadong' in r.text or 'renji' in r.text or 'btwaf' in r.text:
                        self.delCache('czCookie')
                        return self.getContent(params, header)
                    return r

                from requests import session
                session = session()
                r = session.get(url, headers=header, verify=False, timeout=5)
                content = r.content.decode()
                cookie = session.cookies
                if 'huadong' in content or 'renji' in content:
                    url = 'https://www.czzy88.com' + self.regStr(content, 'src=\"(.*?)\"')
                    r = session.get(url, headers=header, verify=False, timeout=5)
                    if 'huadong' in url:
                        key = self.regStr(r.text, 'key=\"(.*?)\"')
                        value = self.regStr(r.text, 'value=\"(.*?)\"')
                        val = ""
                        for i in range(len(value)):
                            code = ord(value[i])
                            val += str(code + 1)
                        value = hashlib.md5(val.encode()).hexdigest()
                        url = 'https://www.czzy88.com{}&key={}&value={}'.format(self.regStr(r.text, 'c.get\(\"(\S+\?type=\S+)&key='), key, value)
                        session.get(url, headers=header, verify=False, timeout=5)
                        cookie = session.cookies
                    elif 'renji' in url:
                        key = self.regStr(r.text, 'var key=\"(.*?)\"')
                        value = self.regStr(r.text, 'value=\"(.*?)\"')
                        val = ''
                        for i in range(0, len(value)):
                            code = ord(value[i])
                            val += str(code)
                        value = hashlib.md5(val.encode()).hexdigest()
                        url = 'https://www.czzy88.com{}&key={}&value={}'.format(self.regStr(r.text, 'c.get\(\"(\S+\?type=\S+)&key='), key, value)
                        session.get(url, headers=header, verify=False, timeout=5)
                        cookie = session.cookies
                    r = session.get(params['url'], headers=header, verify=False, cookies=cookie, timeout=5)
                elif 'btwaf' in content:
                    imgData = session.get('https://www.czzy88.com/get_btwaf_captcha_base64?captcha={}'.format(int(time.time())), timeout=5).json()['msg']
                    code = self.postJson('https://api-lmteam.koyeb.app/ocr', json={'imgList': [imgData], 'lenth': 4}).json()['result']
                    session.get(f'https://www.czzy88.com/Verification_auth_btwaf?captcha={code}', headers=header, timeout=5)
                    cookie = session.cookies
                    r = session.get(params['url'], headers=header, verify=False, cookies=cookie, timeout=5)
                else:
                    r._content = content.encode('utf-8')
                    r.cookies = session.cookies
                    r.url = url
                try:
                    result = int(self.regStr(r.text, 'method=\"post\">(\d+) \+ (\d+) =', 1)) + int(self.regStr(r.text, 'method=\"post\">(\d+) \+ (\d+) =', 2))
                    cookie.set('result', str(result))
                    cookie.set('esc_search_captcha', '1')
                    r = session.get(params['url'], headers=header, verify=False, cookies=cookie, timeout=5)
                    session.close()
                except:
                    session.close()
                self.setCache('czCookie', {'cookieDict': cookie.get_dict(), 'expiresAt': int(time.time()) + 5400})
                return r
            else:
                return None
        except:
            return None

    def getCache(self, key):
        # value = self.fetch(f'http://192.168.1.254:9978/cache?do=get&key={key}', timeout=5).text
        value = self.fetch(f'http://127.0.0.1:9978/cache?do=get&key={key}', timeout=5).text
        if len(value) > 0:
            if value.startswith('{') and value.endswith('}') or value.startswith('[') and value.endswith(']'):
                value = json.loads(value)
                if type(value) == dict:
                    if not 'expiresAt' in value or value['expiresAt'] >= int(time.time()):
                        return value
                    else:
                        self.delCache(key)
                        return None
            return value
        else:
            return None

    def setCache(self, key, value):
        if len(value) > 0:
            if type(value) == dict or type(value) == list:
                value = json.dumps(value, ensure_ascii=False)
        # self.post(f'http://192.168.1.254:9978/cache?do=set&key={key}', data={"value": value}, timeout=5)
        self.post(f'http://127.0.0.1:9978/cache?do=set&key={key}', data={"value": value}, timeout=5)

    def delCache(self, key):
        self.fetch(f'http://127.0.0.1:9978/cache?do=del&key={key}', timeout=5)
