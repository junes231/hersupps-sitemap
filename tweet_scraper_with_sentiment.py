import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ======== 配置部分 ========
KEYWORDS = ["AI", "startup", "crypto", "chatgpt"]  # 要监控的关键词
LANG = "en"                                        # 推文语言
DAYS_BACK = 1                                      # 抓取最近几天
MAX_TWEETS = 300                                   # 每个关键词最大数量
OUTPUT_FILE = "tweets_dataset.csv"                 # 输出 CSV 文件
# =========================

analyzer = SentimentIntensityAnalyzer()

end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=DAYS_BACK)
date_filter = f" since:{start_date} until:{end_date}"

if os.path.exists(OUTPUT_FILE):
    df_all = pd.read_csv(OUTPUT_FILE)
else:
    df_all = pd.DataFrame()

total_new = 0
for keyword in KEYWORDS:
    query = f"{keyword} lang:{LANG}{date_filter}"
    print(f"🔍 正在抓取关键词: {keyword}")
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= MAX_TWEETS:
            break

        sentiment_scores = analyzer.polarity_scores(tweet.content)
        sentiment_label = (
            "positive" if sentiment_scores["compound"] > 0.05 else
            "negative" if sentiment_scores["compound"] < -0.05 else
            "neutral"
        )

        engagement = (tweet.likeCount + tweet.retweetCount + tweet.replyCount)
        engagement_rate = engagement / tweet.user.followersCount if tweet.user.followersCount else 0

        tweets.append({
            "tweet_id": tweet.id,
            "date": tweet.date,
            "keyword": keyword,
            "content": tweet.content,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
            "replies": tweet.replyCount,
            "hashtags": tweet.hashtags if tweet.hashtags else [],
            "followers": tweet.user.followersCount,
            "sentiment": sentiment_label,
            "sentiment_score": sentiment_scores["compound"],
            "engagement_rate": engagement_rate
        })

    df_new = pd.DataFrame(tweets)
    total_new += len(df_new)
    if not df_new.empty:
        df_all = pd.concat([df_all, df_new], ignore_index=True)

df_all.drop_duplicates(subset=["tweet_id"], inplace=True)
df_all.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"✅ Newly added {total_new} Tweets，Total data volume: {len(df_all)} 条")
