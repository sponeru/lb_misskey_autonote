import pandas as pd
import tweepy
from datetime import datetime, timezone
import pytz
from misskey import Misskey
import schedule
from time import sleep
import os
from server import keep_alive

f = open('datefile.txt', 'r+', encoding='UTF-8')  #時間記録用ファイルを読み込む

  f.seek(0)
  tempdatas = f.readlines()
  tempdatas = tempdatas.replace("\n","")
  writedata = "\n".join(tempdatas)
  f.write(writedata)
