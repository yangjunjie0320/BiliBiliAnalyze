import sys, os
from bilibili import BiliBiliVideo
from openai_api import SummarizeReply

OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY", None)
BILIBILI_COOKIE = os.environ.get("BILIBILI_COOKIE", None)

def test_other_prompt(bvid, max_page=2):
    bv = BiliBiliVideo(bvid)

    # The replies shall be accessible without login
    bv.bilibili_cookie = None

    bv.dump_info()
    reply_list = bv.dump_reply(max_page=2)[:10]

    sr = SummarizeReply()
    sr.api_key = OPENAI_API_KEY
    sr.prompt = [
        {
            "role": "system",
            "content": "我希望你是一名视频网站的用户，你正在浏览视频的评论区。"
        },

        {
            "role": "system",
            "content": "视频的作者被观众称为督工、马逆、秃头咪蒙等，节目名字是睡前消息，是一个时政节目。"
        },

        {
            "role": "system",
            "content": "视频的标题是：" + bv.title
        },

        {
            "role": "system",
            "content": "基于视频标题和评论内容，请你写一条回复来反对这条评论。请做到言辞犀利，阴阳怪气。"
        }
    ]

    sr.kwargs = {
        "temperature": 0.1,
    }

    print("\n### Reply Summarize")
    print("Total number of replies dumped: %d" %len(reply_list))

    for reply in reply_list:
        c = ["这是一条对视频的评论：", reply[1]]
        m = sr.run(c)

        print("\n - 原评论: %s" %(reply[1].replace("\n", " ；")))
        print(" - 生成的回复: %s" %(m["choices"][0]["message"]["content"]))

if __name__ == "__main__":
    test_other_prompt("BV1vT411e76N", max_page=2)