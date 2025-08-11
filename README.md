# Twitter Scraper with Sentiment

这是一个自动采集 Twitter 推文并进行情感分析的工具，每天自动运行一次，数据保存为 CSV。

## 功能
- 批量抓取多个关键词的推文
- 自动计算情感（positive/neutral/negative）
- 统计点赞、转推、评论数
- 计算互动率

## 使用方法
1. Fork 本仓库
2. 修改 `tweet_scraper_with_sentiment.py` 中的 `KEYWORDS` 为你要监控的关键词
3. 推送到 GitHub
4. 在仓库的 **Actions** 页面启用 GitHub Actions
5. 等待每天自动运行，或手动触发
6. 数据会更新到仓库的 `tweets_dataset.csv` 文件中

## 手动运行
进入 **Actions** → 选择 **Twitter Scraper with Sentiment** → **Run workflow**

## 依赖
