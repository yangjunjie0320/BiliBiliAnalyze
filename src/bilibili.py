import os, sys
import requests, json, xmltodict

BILIBILI_COOKIE = os.environ.get('BILIBILI_COOKIE', None)

class BiliBiliMixin(object):
    pass

class BiliBiliVideo(BiliBiliMixin):
    bilibili_type = 1

    aid  = None
    cid  = None
    bvid = None
    title = None
    
    subtitle_num  = None
    subtitle_url  = None
    subtitle_list = None

    reply_num  = None
    reply_url  = None
    reply_list = None

    damaku_num   = None
    danmaku_url  = None
    danmaku_list = None

    view_num  = None
    coin_num  = None
    like_num  = None
    fav_num   = None
    share_num = None

    def __init__(self, bv, bilibili_cookie=None):
        self.bilibili_cookie = bilibili_cookie if bilibili_cookie else BILIBILI_COOKIE
        self.bvid = str(bv)

    def get_subtitle_url(self):
        return self.subtitle_url

    def dump_subtitle(self):
        assert self.aid is not None, "aid is not dumped, please run dump_info() first"
        
        subtitle_url  = self.get_subtitle_url()
        subtitle_list = []
        if subtitle_url:
            data = json.loads(requests.get(subtitle_url).text)
            for d in data['body']:
                subtitle_list.append((d['content']))

        self.subtitle_list = subtitle_list if len(subtitle_list) > 0 else None
        return self.subtitle_list

    def get_reply_page_url(self, max_page=10):
        reply_max_page = min(max_page, self.reply_num // 20 + 1)
        reply_page_url_list = []
        for ipage in range(reply_max_page):
            reply_page_url_list.append("https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=" + str(ipage + 1) + "&type=1&oid=" + str(self.aid))
        return reply_page_url_list

    def get_reply_url(self, oid, rpid):
        return f"https://www.bilibili.com/h5/comment/sub?oid={oid}&pageType={self.bilibili_type}&root={rpid}"

    def dump_reply(self, max_page=10):
        assert self.aid is not None, "aid is not dumped, please run dump_info() first"

        reply_page_url_list = self.get_reply_page_url(max_page)

        reply_list = []
        for reply_page_url in reply_page_url_list:
            data = self.requests(reply_page_url)
            if data:
                for r in data['replies']:
                    rpid = r['rpid']
                    oid  = r['oid']
                    
                    reply_list.append(
                        (self.get_reply_url(oid, rpid), r['content']['message'])
                    )

        self.reply_list = reply_list if len(reply_list) > 0 else None
        return reply_list

    def get_danmaku_url(self):
        raise NotImplementedError

    def dump_danmaku(self):
        raise NotImplementedError

    def requests(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        if self.bilibili_cookie:
            headers['Cookie'] = self.bilibili_cookie

        response = requests.get(url, headers=headers)
        res_dict = json.loads(response.text)

        if res_dict['code'] == 0:
            return res_dict['data']
        else:
            return None

    def get_info_url(self):
        assert self.bvid is not None, "bvid is not set"
        return "https://api.bilibili.com/x/web-interface/view?bvid=" + self.bvid

    def dump_info(self):
        if self.title is None:
            url  = self.get_info_url()
            data = self.requests(url)

            if data:
                self.aid  = data['aid']
                self.cid  = data['cid']
                self.title = data['title']

                if len(data['subtitle']['list']) > 0:
                    self.subtitle_url = data['subtitle']['list'][0]['subtitle_url']

                self.reply_num = data['stat']['reply']
                self.damaku_num = data['stat']['danmaku']
                self.view_num = data['stat']['view']
                self.coin_num = data['stat']['coin']
                self.like_num = data['stat']['like']
                self.fav_num = data['stat']['favorite']
                self.share_num = data['stat']['share']

        print("### BiliBiliVideo Basic Info")
        print("- `aid   = %s`"%str(self.aid))
        print("- `cid   = %s`"%str(self.cid))
        print("- `bvid  = %s`"%str(self.bvid))
        print("- `title = %s`"%str(self.title))
        
        print("\n### BiliBiliVideo Stat Info")
        print("- `reply_num  = %s`" % str(self.reply_num))
        print("- `damaku_num = %s`" % str(self.damaku_num))
        print("- `view_num   = %s`" % str(self.view_num))
        print("- `coin_num   = %s`" % str(self.coin_num))
        print("- `like_num   = %s`" % str(self.like_num))
        print("- `fav_num    = %s`" % str(self.fav_num))
        print("- `share_num  = %s`" % str(self.share_num))

if __name__ == "__main__":
    bv = BiliBiliVideo("BV1AY411E71m")
    bv.dump_info()
    bv.dump_reply()