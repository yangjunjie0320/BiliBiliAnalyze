import sys, os
from bilibili import BiliBiliVideo
from openai_api import ChatCompletion

OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY", None)
BILIBILI_COOKIE = os.environ.get("BILIBILI_COOKIE", None)

def edit_subtitle(text, title=None, max_tokens=1000, max_batch=1000):
    prompt = [
        {
            "role": "user",
            "content": "我希望你是一名专业的视频内容编辑，请你将所给的一部分字幕文本进行订正（字幕中可能有错别字，如果你发现了错别字请改正，比如所有的Cheat GT或者Cheat GPT都应该改为ChatGPT）；并在适当的位置添加标点符号，不要分段或加入空行。"
        },

        {
            "role": "user",
            "content": "请直接输出订正后的字幕文本，不必加入任何其他内容。"
        }
    ]

    cc = ChatCompletion()
    cc.api_key = OPENAI_API_KEY
    cc.prompt  = prompt

    cc.kwargs = {
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }

    tt = "#".join(text)
    tt = tt.replace("，", "")
    tt = tt.replace("。", "")
    tt = tt.replace("\n", "")
    text = tt.split("#")
    batch_size = len(tt) // ((len(tt) // max_batch - 1) or 1) + 1
    print("len(s) = %d; batch_size = %d" %(len(tt), batch_size))

    s = ""
    a = ""
    part_count = 0

    with open(f"./tmp/edited-subtitle-{title}.md", "w") as f:
        for it, tt in enumerate(text):
            s += tt if len(s) > 0 else tt

            if len(s) > batch_size or it == len(text) - 1:
                part_count += 1

                c = ["以下是这个视频的字幕的一部分：", s]
                m = cc.run(c)

                print("\n\n%s" %(m["choices"][0]["message"]["content"]))
                f.write("\n# Subtitle Part %d\n\n" %(part_count))
                f.write("## Original\n\n")
                f.write(s)
                f.write("\n\n")
                f.write("## Edited\n\n")
                f.write(m["choices"][0]["message"]["content"])
                f.write("\n\n")

                s = ""
                a += m["choices"][0]["message"]["content"]
                a += "\n"

    return a


def summarize_article(text, title=None, max_tokens=1000, max_batch=1000):
    prompt = [
        {
            "role": "user",
            "content": "我希望你是一名专业的文字编辑，请你将所给的一篇文章改写，做到以下几点："
        },
        {
            "role": "system",
            "content": "1. 用markdown语法写作，每个段落用空行分隔，每个标题用#开头；2. 语言简练、书面化；3. 文本中可能有错别字，如果你发现了错别字请改正。"
        },
    ]

    cc = ChatCompletion()
    cc.api_key = OPENAI_API_KEY
    cc.prompt  = prompt

    cc.kwargs = {
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }

    text = ",".join("。".join(text.split("\n")).split("。")).split(",")
    tt = "\n".join(text)
    batch_size = len(tt) // ((len(tt) // max_batch - 1) or 1) + 1
    print("len(s) = %d; batch_size = %d" %(len(tt), batch_size))

    s = ""
    a = ""
    part_count = 0

    with open(f"./tmp/article-{title}.md", "w") as f:
        for it, tt in enumerate(text):
            s += ", " + tt if len(s) > 0 else tt

            if len(s) > batch_size or it == len(text) - 1:
                part_count += 1

                c = ["以下是文本的一部分：", s]
                m = cc.run(c)

                print("\n\n%s" %(m["choices"][0]["message"]["content"]))
                f.write("\n# Article Part %d\n\n" %(part_count))
                f.write("## Original\n\n")
                f.write(s)
                f.write("\n\n")
                f.write("## Summary\n\n")
                f.write(m["choices"][0]["message"]["content"])
                f.write("\n\n")

                s = ""
                a += m["choices"][0]["message"]["content"]
                a += "\n"

    return a

def test_other_prompt(bvid, max_batch=1000, max_tokens=1000):
    # bv = BiliBiliVideo(bvid)
    # bv.bilibili_cookie = BILIBILI_COOKIE
    # bv.dump_info()

    # subtitle_list = bv.dump_subtitle()
    # ss = edit_subtitle(subtitle_list, title="%s-1" % bvid, max_tokens=max_tokens, max_batch=max_batch)
    # with open(f"./tmp/article-{bvid}-v1.md", "w") as f:
    #     f.write(ss)

    with open(f"./tmp/article-{bvid}-v1.md", "r") as f:
        ss = f.read()
        ss.replace("\r", "")
        print(ss)

        article_list = ss.split("\n")
        ss = summarize_article(ss, title="%s-2" % bvid, max_tokens=max_tokens, max_batch=max_batch)
        with open(f"./tmp/article-{bvid}-v2.md", "w") as f:
            f.write(ss)

        with open(f"./article-{bvid}.md", "w") as f:
            f.write(ss)


if __name__ == "__main__":
    test_other_prompt("BV1MY4y1R7EN", max_batch=500, max_tokens=1000)