import os, sys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

import openai
from retrying import retry

class OpenAIModelMixin(object):
    api_key = OPENAI_API_KEY
    model   = "gpt-3.5-turbo"
    prompt  = None

class ChatCompletion(OpenAIModelMixin):    
    def get_messages(self, content):
        message_list = []

        if self.prompt is not None:
            for p in self.prompt:
                message_list.append(p)

        if isinstance(content, list):
            for c in content:
                message_list.append(
                    {
                        "role": "user",
                        "content": c
                    }
                )

        return message_list

    @retry(stop_max_attempt_number=20)
    def run(self, content):
        message_list = self.get_messages(content)

        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise Exception("OpenAI API Key is not set.")
        
        completion = openai.ChatCompletion.create(
            model      = self.model,
            messages   = message_list,
        )

        return completion

class SummarizeSubtitle(ChatCompletion):
    prompt = [
        {
            "role": "system",
            "content": "我希望你是一名专业的视频内容编辑，帮我总结视频的内容精华。请你将所给的一部分字幕文本进行总结（字幕中可能有错别字，如果你发现了错别字请改正），然后以无序列表的方式返回，记得不要重复句子。确保所有的句子都足够精简，清晰完整，祝你好运！"
        }
    ]

class SummarizeReply(ChatCompletion):
    prompt = [
        {
            "role": "system",
            "content": "我希望你是一名专业的视频内容编辑，现在你需要阅读一条对视频的评论，判断这条评论的语气（严肃、戏谑等）和主要内容（个人经历、表达观点、提出建议等）。下面是一些例子供你参考："
        },

        {
            "role": "user",
            "content": "这是一条对视频的评论："
        },

        {
            "role": "user",
            "content": "真不明白你们怎么想的？现在的中国只要是有人聚居的地方，几乎所有的乡村都有信号，手机都能上网。马前卒说的那些荒郊野外，深山老林的地方有多少人会去？什么人会去？难道告诉你深山老林手机能上网，老百姓就会经常去深山老林吗？吃饱了撑的？经常有去荒郊野外，深山老林的需求的人，主要还是工作原因必须去，他们有专业的通讯装备，可以进行网络活动。至于什么旅游团，这不是扯淡吗？只要是我国正规开发的旅游景点，哪个没信号？"
        },

        {
            "role": "assistant",
            "content": "语气：讽刺，主要内容：表达观点"
        },

        {
            "role": "user",
            "content": "请根据以上的例子进行判断，并以相似的格式输出。确保足够精简，祝你好运！"
        }
    ]