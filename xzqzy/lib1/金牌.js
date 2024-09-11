var rule = {
    title: '金牌影视',
    url: "/vod/show/id/fyclassfyfilter",
    host: "https://www.cfkj86.com",
    searchUrl: '/search/$wd/fypage',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    class_name: "电影&电视剧&综艺&动漫",
    class_url: "1&2&3&4",
    filter: "H4sIAAAAAAAAAO1YW08aQRT+L/tssuyygPo7+tb4QCppm1ptxNoYY4MiKtiKGqOitLbxAlYRUGN1Ef0zu7O7/6KLMzs3hkvabWosLyR7vu/M5ZyZc75hWlKkwefT0pvYlDQoWdWa+XVZ6pNGo29j9PdkdOR97IE46prNVNFJFhtm90Oa6UPWzbyZLiCrPDH1LiarKkEzRaOeZ9EgRq3CmnlTY9BggKBLVZBMsb5hjIK5U2tzjUUjZN7DRX7kfgpNF/iRgwQFs6sgscmiZF4rU7bqP1g0RO/X2uB2RPYLkhkwt8OiGkGXtg09ze6IGnlh3ckds74KWdXsnbNzx+6XoMbtkbW6wKJkVWbqyqix+9VcdKiBwwNi5ivmJ50cEPzdzQExrkvmbt08KDg5vIToeCwqMwDLdo5y4LosYCOAGztbATd3orEhgIN0t+IaGR4y4RRsHYL8KcNAJo/h7B3zYyATDufniqkfMQxkwrNcVPgxkEmcEjgGNDFpubk0anUqLd53N2lRA6rmTTAVi47LDwYKDfJokEZVHlVpVOFRhUYDPBqgUGWAQ10DhfbzaD+NRng0QqNhHg3TaIhHQzTKx0qhY6XwsVLoWCl8rBQ6VgofK4WOlcLHSqFjFRj46P7wFM9KHxW7XLKLCXJU8HdXJX637vK9WUaioy9lZPIY9nKVZyATvnvnBzwDmaibxTOQibqdPAOZxPcGrrT53oCVdVPPkmDgbzYYxnUGbH8DW1fO1qU3ZHxsfOJZo0JSxVXXQWXDOdk26itNNHIO7PK8ubTQgqY11jfUJ6m+deXduqEX+MZMHVpwWmjUPp5AzrxbZt3y2UQI09loVD6OEFa5ZDQR+tka5rVir4bh1tx6l/Lk2LAcfzX2QX49LFPzZQ/s/ZSQI78YicbjMmKIG67IATHEWkc4A2Rgh7MrUy+1dYAMsboQOSCGWGAJZ4AMsTISOkCGWCwJHSADO6wsmNnztg6QgTe9V7LSi203DRlPUJP4oTi60DU9xdFTHH+gOPxSEiB35iR27PIXtolj62PTE+4laWJA019RHCCfsO/XwO4l2Ky0URzgZ83MtBImJNN+CpOgv8LEqt3aaZ3VBeTSQekh4EQCdO7cbIo4JABQ44g4QX81CPWPRn7PDbtVSAhpXjfDJHJWL4yb1XY+iIGTNl81s/sd5iGkXuP8zcb5/7XF3qPxiZZwzee3ZaYIbk/YshriyrOIE+bKs4gT8bc8k9vU+gGniR9w7D/UIgfEwA7Jkv1dWJWxA2TgJTH/6wqXBBmdX3ya+MVn36+6lnYOiNH5Xay1eBfP31snh22XBBn/qA917hW9TtB7ID2GB5IfXbPX8R463swvJhzXtOUcAAA=",
    filter_url: "{{fl.类型}}{{fl.地区}}{{fl.字母}}{{fl.语言}}{{fl.版本}}{{fl.资源}}{{fl.排序}}/id/fyclass/page/fypage{{fl.年份}}",
    headers: {
        "User-Agent": "PC_UA",
    },
    推荐: $js.toString(() => {
        let html = request(HOST);
        //log(html)
        let arr = cut(html.replace(/\\\"/g, '\"'), '\"list\":', '\"vodScoreAll\":0}]', (r) => {
            return r.replaceX(/vod(Name)/g, "_name")
        }, true).parseX.flat();
        //log(arr)
        VODS = arr.map(function(it) {
            return {
                vod_name: it.vod_name,
                vod_pic: it.vodPic,
                vod_remarks: it.vodVersion,
                vod_id: HOST + "/detail/" + it.vodId
            }
        })
    }),
    一级: $js.toString(() => {
        let html = request(input);
        let arr = cut(html.replace(/\\\"/g, '\"'), '\"list\":', '\"vodScoreAll\":0}]', (r) => {
            return r.replaceX(/vod(Name)/g, "_name")
        }).parseX.flat();
        //log(arr)
        VODS = arr.map(function(it) {
            return {
                vod_name: it.vod_name,
                vod_pic: it.vodPic,
                vod_remarks: it.vodVersion,
                vod_id: HOST + "/detail/" + it.vodId
            }
        })
    }),
    二级: $js.toString(() => {
        let html = request(input);
        //log(html)
        let json = cut(html.replace(/\\\"/g, '\"'), "\"操作成功\",\"data\":", "\]\}").parseX;
        //log(json)
        let base_vod = {
            vod_id: input,
            vod_name: json.vodName,
            type_name: json.vodClass,
            vod_actor: json.vodActor,
            vod_director: json.vodDirector,
            vod_content: json.vodContent,
            vod_remarks: json.vodArea,
            vod_pic: json.vodPic
        };
        let plays = [];
        json.episodeList.map(it => {
            plays.push(it.name + "$" + HOST + "/vod/play/" + json.vodId + "/sid/" + it.nid);
        })
        //log(plays)
        base_vod.vod_play_from = "金牌播放器";
        base_vod.vod_play_url = plays.join("#");
        VOD = base_vod;
    }),
    搜索: $js.toString(() => {
        function guid() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16 | 0,
                    v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }
        var t = new Date().getTime().toString().split('.')[0];
        var signkey = 'keyword=' + KEY + '&pageNum=' + MY_PAGE + '&pageSize=12&type=false&key=cb808529bae6b6be45ecfab29a4889bc&t=' + t;

        let url = HOST + "/api/mw-movie/anonymous/video/searchByWord?keyword=" + KEY + "&pageNum=" + MY_PAGE + "&pageSize=12&type=false"
        var key = CryptoJS.SHA1(CryptoJS.MD5(signkey).toString()).toString()
        var list = JSON.parse(request(url, {
            headers: {
                Referer: HOST,
                deviceId: guid(),
                sign: key,
                t: t
            }
        })).data.result.list;
        VODS = list.map(function(it) {
            return {
                vod_name: it.vodName,
                vod_pic: it.vodPic,
                vod_remarks: it.vodVersion,
                vod_content: it.vodBlurb,
                vod_id: HOST + "/detail/" + it.vodId
            }
        })
    })
}