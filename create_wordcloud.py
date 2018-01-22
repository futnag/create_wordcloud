import wordcloud
import matplotlib.pyplot as plt
from datetime import datetime
from twitter import Twitter, OAuth
import neologdn
import re
import MeCab

# apiキーを記入してください
api_key = 
api_secret = 
access_token_key = 
access_token_secret = 


def normalize_string(text):
    """
    文字列から余計な記号などを取り除く
    """
    normalized_text = neologdn.normalize(text).lower()
    replaced_text = re.sub("[!?@「」()、。・（）…/_:;\s]", "", normalized_text)
    return replaced_text


def create_wordcloud(user, text):
    """
    ワードクラウドを作成し、同一ディレクトリ内に保存する
    """
    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
    wc = wordcloud.WordCloud(background_color="white",font_path=fpath, width=900, height=500).generate(text)
    plt.figure(figsize=(15,8))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(user + str(datetime.now()) + ".png")


def main():
    target_user = input()
    count = 100 #一度のアクセスで何件取ってくるか

    t = Twitter(auth=OAuth(
        access_token_key,
        access_token_secret,
        api_key,
        api_secret,
    ))

    user_tweets = []

    timeline = t.statuses.user_timeline(screen_name=target_user, count=count)

    for tweet in timeline:
        user_tweets.append(tweet['text'])

    tweet_data = list(map(normalize_string, user_tweets))

    result_text = []
    mec = MeCab.Tagger("-Ochasen")

    for tw in tweet_data:
        temp = mec.parse(tw).split('\n')
        for t in temp:
            word_data = t.split()
            word = word_data[0]
            stopwords = ['http', 'EOS', 'rt', 'http', 'tweet', 'peing', '人', 'あと',\
                         '感じ','httpst', 'rt', 'com', 'the', 'http', '今日']
            check = [sw in word for sw in stopwords]

            if any(check):
                break
            else:
                tow = word_data[-1]
                stop = ["非自立", "代名詞" , "数", "接尾"]
                validation = all(map(lambda x: x not in tow, stop))

                if tow[0:2] == "名詞" and validation:
                    result_text.append(word)

    create_wordcloud(target_user, " ".join(result_text))


if __name__ == '__main__':
    main()

