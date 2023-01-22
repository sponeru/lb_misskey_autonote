import pandas as pd
import tweepy
from datetime import datetime, timezone
import pytz
from misskey import Misskey
import schedule
from time import sleep
import os
from server import keep_alive

mk = Misskey(os.environ['MISSKEY_URL'], i=os.environ['MISSKEY_TOKEN'])
client = tweepy.Client(consumer_key=os.environ['TWETTER_CONSUMER_KEY'],
                       consumer_secret=os.environ['TWETTER_CONSUMER_SECRET'],
                       access_token=os.environ['TWETTER_ACCESS_TOKEN'],
                       access_token_secret=os.environ['TWITTER_ACCESS_SECRET'],
                       bearer_token=os.environ['TWITTER_BEARER_TOKEN'])
f = open('datefile.txt', 'r+', encoding='UTF-8')  #時間記録用ファイルを読み込む

#他のアカウントでやりたかったら次の2行を編集すればなんとかなる
search_word_lastbullet_user = 'from:assaultlily_lb -\”app.adjust.com\”'  #キャンペーンツイートを除外 Twitterの検索と同じ構文です	
urlbase_lb = "https://twitter.com/assaultlily_lb/status/"  #TwitterのURLのベース(後ろに勝手にIDがつく)

item_number = 10  #最新10件のデータ収得


#関数:　UTCをJSTに変換する (サイトからの引用)
def change_time_JST(u_time):
  #イギリスのtimezoneを設定するために再定義する
  utc_time = datetime(u_time.year, u_time.month,u_time.day, \
  u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
  #タイムゾーンを日本時刻に変換
  jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
  return jst_time


def send_lb():  #ツイートの取得とノート
  lastbullet_tweets = client.search_recent_tweets(
    query=search_word_lastbullet_user,
    max_results=item_number,
    tweet_fields=["created_at"])

  datelist = f.readlines()
  recenttime_lb = datetime.fromisoformat(datelist[0])

  lastbullet_tweets = list(lastbullet_tweets[0])
  for tweet in lastbullet_tweets:
    if change_time_JST(
        tweet.created_at
    ) > recenttime_lb:  #元ツイの投稿時間が最後に更新した時間より後であればノートを作成する処理に入る
      tempstr = tweet.text  #
      tempstr = tempstr.split("\n")  #
      print(tempstr)  #
      for i, a in enumerate(tempstr):  #       元ツイート文の先頭に引用符を付けるだけのクソみたいな処理
        if a != "\n":  #
          tempstr[i] = "> " + a  #
      tempstr = "\n".join(tempstr)  #
      tempstr = tempstr.replace("@", "＠")
      print(tempstr)  #
      mk.notes_create(
        text=str("Twitterが更新されました！\n") +
        str("?[URL](" + urlbase_lb + str(tweet.id) + ")\n" + tempstr))  #ノートを作成

  #ここから最後に更新した時間を記録する処理
  f.seek(0)
  f.truncate(0)
  tempdatas = [change_time_JST(datetime.now(timezone.utc)).isoformat()]
  writedata = "\n".join(tempdatas)
  f.write(writedata)


#ここからマルチバトルの通知処理 要らなければここから10行消しても良い
def bonus_alart_a():
  mk.notes_create(text="[定期通知]\n[3分前]マルチバトルのボーナスタイムがもうすぐ始まります！" + "(12時の部)")


def bonus_alart_b():
  mk.notes_create(text="[定期通知]\n[3分前]マルチバトルのボーナスタイムがもうすぐ始まります！" + "(18時の部)")


def bonus_alart_c():
  mk.notes_create(text="[定期通知]\n[3分前]マルチバトルのボーナスタイムがもうすぐ始まります！" + "(23時の部)")


#スケジュールに登録
schedule.every().hour.at(":05").do(send_lb)

#マルチバトルの通知処理を消したら以下の3行も消しておく
schedule.every().day.at("12:42").do(bonus_alart_a)
schedule.every().day.at("18:27").do(bonus_alart_b)
schedule.every().day.at("23:12").do(bonus_alart_c)

#ここから常時実行
send_lb()
keep_alive()
while True:
  schedule.run_pending()
  sleep(1)
