import ssl
import snscrape.modules.twitter as sntwitter
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

# 跳过 SSL 验证（解决 GitHub Actions 报错问题）
ssl._create_default_https_context = ssl._create_unverified_context

# 搜索关键词 & 时间范围
query = "AI lang:en"
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)
since_date = yesterday.strftime("%Y-%m-%d")
until_date = today.strftime("%Y-%m-%d")

query += f" since:{since_date} until:{until_date}"

# 初始化情感分析器
analyzer = SentimentIntensityAnalyzer()

# 采集推文
tweets_data = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > 200:  # 限制数量，避免超时
        break
    sentiment_score = analyzer.polarity_scores(tweet.content)
    sentiment = (
        "positive" if sentiment_score['compound'] > 0.05
        else "negative" if sentiment_score['compound'] < -0.05
        else "neutral"
    )
    tweets_data.append([
        tweet.date, tweet.user.username, tweet.content, sentiment
    ])

# 转为 DataFrame
df = pd.DataFrame(tweets_data, columns=["date", "username", "content", "sentiment"])

# 保存 CSV（追加模式）
csv_file = "tweets_dataset.csv"
try:
    old_df = pd.read_csv(csv_file)
    df = pd.concat([old_df, df], ignore_index=True)
except FileNotFoundError:
    pass

df.to_csv(csv_file, index=False, encoding="utf-8-sig")
print(f"已保存 {len(df)} 条推文到 {csv_file}")
