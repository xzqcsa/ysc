#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "央视"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
	
"动画大放映":   "TOPC1451559025546574", 
"第一动画乐园": "TOPC1451378857272262", 
"周末动画片":   "TOPC1451559836238828", 
"动漫世界":     "TOPC1451559448233349", 
"智慧树":       "TOPC1451447359806385", 
"小小智慧树":   "TOPC1451559205464876", 
"袋袋裤":       "TOPC1451559603261584", 
"大风车":       "TOPC1451558929123462", 
"音乐快递":     "TOPC1451559666055645", 
"大手牵小手":   "TOPC1451558967135492", 
"七巧板":       "TOPC1451559569040502", 
"英雄出少年":   "TOPC1451559695702690", 
"快乐大巴":     "TOPC1451559161446811",
"动感特区":   "TOPC1451559378830189",
"快乐体验":   "TOPC1451559479171411",
"异想天开":   "TOPC1451559633994614",
"看我72变":   "TOPC1451559131256781",
"快乐驿站": "TOPC1451542273075862",
"我爱发明": "TOPC1569314345479107",
"精彩音乐汇"  : "TOPC1451541414450906",
"动物世界": "TOPC1451378967257534",
"星光大道": "TOPC1451467630488780",
"中国节拍": "TOPC1570025984977611",
"民歌·中国"     : "TOPC1451541994820527",

"解码科技史": "TOPC1570876640457386",
"走进科学": "TOPC1451558190239536",
"非常6+1": "TOPC1451467940101208",

"新闻30分"        : "TOPC1451559097947700",   
"新闻直播间" : "TOPC1451559129520755",

"第一时间"  : "TOPC1451530259915198",
"晚间新闻": "TOPC1451528792881669",
"新闻联播": "TOPC1451528971114112",
"午夜新闻" : "TOPC1451558779639282",
"朝闻天下" : "TOPC1451558496100826",
"新闻调查": "TOPC1451558819463311",
"新闻周刊"    : "TOPC1451559180488841",

"东方时空": "TOPC1451558532019883",
"世界周刊": "TOPC1451558687534149",

"新闻1+1"       : "TOPC1451559066181661",  

"24小时"   : "TOPC1451558428005729",


"共同关注": "TOPC1451558858788377",
"环球视线": "TOPC1451558926200436",
"焦点访谈": "TOPC1451558976694518",
"今日环球" : "TOPC1571034705435323",
"天网" : "TOPC1451530382483536",
"天下财经": "TOPC1451531385787654",
"经济大讲堂" : "TOPC1451533652476962",
"经济信息联播" : "TOPC1451533782742171",
"经济半小时"      : "TOPC1601362002656197",
"故事里的中国": "TOPC1451464884159276", 

"动物传奇": "TOPC1451984181884527",
"今日说法": "TOPC1451464665008914",
"开讲啦": "TOPC1451464884159276",
"防务新观察": "TOPC1451526164984187",
"军事报道"  : "TOPC1451527941788652",
"国宝发现": "TOPC1571034869935436",
"正点财经": "TOPC1453100395512779",
"对话": "TOPC1514182710380601", 
"华人世界": "TOPC1451539822927345",
"中国新闻" : "TOPC1451539894330405",
"国宝档案": "TOPC1451540268188575",
"海峡两岸": "TOPC1451540328102649",
"今日关注": "TOPC1451540389082713",
"今日亚洲": "TOPC1451540448405749",
"深度国际": "TOPC1451540709098112",
"外国人在中国": "TOPC1451541113743615",
"远方的家": "TOPC1451541349400938",
"法律讲堂": "TOPC1451542824484472",
"一线" : "TOPC1451543462858283",
"一鸣惊人": "TOPC1451558692971175",
"开门大吉": "TOPC1451465894294259",


"星推荐": "TOPC1451469943519994",
"等着我": "TOPC1451378757637200",
"生活提示": "TOPC1451526037568184",
"讲武堂": "TOPC1451526241359341",
"是真的吗"   : "TOPC1451534366388377",
"环球综艺": "TOPC1571300682556971",
"中国电影报道"   : "TOPC1451354597100320",

"空中剧院"  : "TOPC1451558856402351",
"三农群英会": "TOPC1600745974233265",
"金牌喜剧班": "TOPC1611826337610628",
"正大综艺" : "TOPC1650782829200997",
"面对面" : "TOPC1451559038345600",
"曲苑杂谈": "TOPC1451984417763860",

"综艺盛典": "TOPC1451985071887935",
"音乐厅"  : "TOPC1451534421925242",



"生活圈": "TOPC1451546588784893",
"棋牌乐": "TOPC1451550531682936",
"体坛快讯" : "TOPC1451550970356385",
"武林大会": "TOPC1451551891055866",
"百家讲坛": "TOPC1451557052519584",
"地理中国": "TOPC1451557421544786",
"健康之路" : "TOPC1451557646802924",
"探索·发现" : "TOPC1451557893544236", 
"探索发现": "TOPC1451557893544236",
"自然传奇": "TOPC1451558150787467",
"环球科技视野": "TOPC1451463780801881",
"我爱发明2021": "TOPC1451557970755294",
"锦绣梨园": "TOPC1451558363250650",
"九州大戏台": "TOPC1451558399948678",

	


"人与自然": "TOPC1451525103989666",
"美食中国": "TOPC1571034804976375",
"方圆剧阵"   : "TOPC1571217727564820",
"梨园周刊": "TOPC1574909786070351",
"跟着书本去旅行" : "TOPC1575253587571324",
"名家书场": "TOPC1579401761622774",
"超级新农人": "TOPC1597627647957699",
"家庭幽默大赛": "TOPC1451375222891702",
"高端访谈": "TOPC1665739007799851",
"田间示范秀": "TOPC1563178908227191",
"乡村大舞台": "TOPC1563179546003162",
"乡村振兴面对面": "TOPC1568966531726705",

"印象乡村": "TOPC1563178734372977"	
}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		extend['id'] = tid
		extend['p'] = pg
		filterParams = ["id", "p", "d"]
		params = ["", "", ""]
		for idx in range(len(filterParams)):
			fp = filterParams[idx]
			if fp in extend.keys():
				params[idx] = '{0}={1}'.format(filterParams[idx],extend[fp])
		suffix = '&'.join(params)
		url = 'https://api.cntv.cn/NewVideo/getVideoListByColumn?{0}&n=20&sort=desc&mode=0&serviceId=tvcctv&t=json'.format(suffix)
		if not tid.startswith('TOPC'):
			url = 'https://api.cntv.cn/NewVideo/getVideoListByAlbumIdNew?{0}&n=20&sort=desc&mode=0&serviceId=tvcctv&t=json'.format(suffix)
		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		vodList = jo['data']['list']
		videos = []
		for vod in vodList:
			guid = vod['guid']
			title = vod['title']
			img = vod['image']
			brief = vod['brief']
			videos.append({
				"vod_id":guid+"###"+img,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		aid = array[0].split('###')
		tid = aid[0]
		url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={0}".format(tid)

		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		title = jo['title'].strip()
		link = jo['hls_url'].strip()
		vod = {
			"vod_id":tid,
			"vod_name":title,
			"vod_pic":aid[1],
			"type_name":'',
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":""
		}
		vod['vod_play_from'] = 'CCTV'
		vod['vod_play_url'] = title+"$"+link

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		rsp = self.fetch(id,headers=self.header)
		content = rsp.text.strip()
		arr = content.split('\n')
		urlPrefix = self.regStr(id,'(http[s]?://[a-zA-z0-9.]+)/')
		url = urlPrefix + arr[-1]
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = ''
		return result

	config = {
		"player": {},
		
		"filter": {"TOPC1451557970755294": [{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}]}
	}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
