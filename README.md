# BiliBiliAnalyze

This version could be running with simple command:
```bash
export path=/Users/$(whoami)/Downloads/ # the directory of this project
export branch=main                     # the branch of this project
mkdir -p $path/BiliBiliAnalyze/
git clone --branch $branch git@github.com:yangdatou/BiliBiliAnalyze.git $path/BiliBiliAnalyze/BiliBiliAnalyze-$branch/
cd $path/BiliBiliAnalyze/BiliBiliAnalyze-$branch/

echo OPENAI_API_KEY=$OPENAI_API_KEY
echo BILIBILI_COOKIE=$BILIBILI_COOKIE

pip install -r requirements.txt
cd ./src/;  export PYTHONPATH=$PYTHONPATH:$(pwd); cd -;
cd ./test/; export PYTHONPATH=$PYTHONPATH:$(pwd); cd -;

cd test/
python test_reply_summarize.py    > test_reply_summarize.md
tail test_reply_summarize.md

python test_subtitle_summarize.py > test_subtitle_summarize.md
tail test_subtitle_summarize.md

cd -
```

If the above commands work as expected, you can run the following command to analyze the replies of a video:
```bash
export BV=BV1vT411e76N
export MAX_PAGE=2
python -c "from test_reply_summarize import test_reply_summarize; test_reply_summarize('$BV', '$MAX_PAGE')"
```
