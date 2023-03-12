import sys, os
from bilibili import BiliBiliVideo
from openai_api import SummarizeReply

OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY", None)
BILIBILI_COOKIE = os.environ.get("BILIBILI_COOKIE", None)

def test_reply_summarize(bvid, max_page=2):
    bv = BiliBiliVideo(bvid)

    # The replies shall be accessible without login
    bv.bilibili_cookie = None

    bv.dump_info()
    reply_list = bv.dump_reply(max_page=2)[:4]

    sr = SummarizeReply()
    sr.api_key = OPENAI_API_KEY
    sr.kwargs = {
        "temperature": 0.5,
    }

    print("\n### Reply Summarize")
    print("Total number of replies dumped: %d" %len(reply_list))

    for reply in reply_list:
        
        c = ["这个视频的作者被观众称为督工、马逆、秃头咪蒙等，节目名字是睡前消息，视频标题是：", bv.title]
        c = ["这是一条对视频的评论：", reply[1]]
        m = sr.run(c)

        print("\n - [%s](%s): %s" %(m["choices"][0]["message"]["content"], reply[0], reply[1].replace("\n", " ；")))

if __name__ == "__main__":
    test_reply_summarize("BV1vT411e76N", max_page=2)