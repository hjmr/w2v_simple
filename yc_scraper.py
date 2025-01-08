# 必要なパッケージの読み込み
import requests
import re
import time
import random
from bs4 import BeautifulSoup

MAIN_SORT_KEY = {
    "更新日時の新しい順": 16,
    "更新日時の古い順": 17,
    "質問日時の新しい順": 20,
    "質問日時の古い順": 21,
    "回答数の多い順": 4,
    "回答数の少ない順": 5,
    "お礼の多い順": 8,
}
DETAIL_SORT_KEY = {"ナイスの多い順": 0, "新しい順": 1, "古い順": 2}
QA_STAT = {"回答受付中": 0, "解決済み": 1, "全て": 3}

MAIN_SORT_KEY = {
    "更新日時の新しい順": 16,
    "更新日時の古い順": 17,
    "質問日時の新しい順": 20,
    "質問日時の古い順": 21,
    "回答数の多い順": 4,
    "回答数の少ない順": 5,
    "お礼の多い順": 8,
}
DETAIL_SORT_KEY = {"ナイスの多い順": 0, "新しい順": 1, "古い順": 2}
QA_STAT = {"回答受付中": 0, "解決済み": 1, "全て": 3}

def get_qa_text(base_link, sort_mode="ナイスの多い順"):
    text_list = []
    sort_id = DETAIL_SORT_KEY[sort_mode]
    link = base_link + "?sort={}".format(sort_id)

    res = requests.get(link)
    soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")

    ans_count_tag = soup.select_one('strong[class*="Chie-QuestionItem__AnswerNumber__"]')
    ans_count = int("".join(ans_count_tag.text.split(","))) if ans_count_tag is not None else 0
    max_page = min(10, (ans_count // 10 + 1) if 0 < ans_count else 1)

    print(f"*** QA: # of answers:{ans_count}, pages:{max_page} ... ")

    print("**** extracting Question ... ", end="")
    # que_text_tag = soup.select_one('div[class*="Chie-QuestionItem__Text__"]')
    que_text_tag = soup.find("div", class_=re.compile(r"Chie-QuestionItem__Text__"))
    if que_text_tag is not None:
        text_list.append(que_text_tag.text)
    print("done.")

    for page_num in range(1, max_page + 1):
        print(f"**** extracting Answers in page {page_num} ... ", end="")
        page_link = link + "&page={}".format(page_num)

        # 過剰な負荷を避けるため，１ページ分の記事を取得する前に 1〜3秒休む
        time.sleep(random.randrange(1, 3))

        res = requests.get(link)
        soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")

        # ans_text_list = soup.select('div[class*="Chie-AnswerItem__ItemText__"]')
        ans_text_list = soup.find_all("div", class_=re.compile(r"Chie-AnswerItem__ItemText__"))
        ans_text_num = 0
        for ans_tag in ans_text_list:
            text_list.append(ans_tag.text)
            ans_text_num += 1
        print(f"{ans_text_num} answers extracted.")

    return "".join(text_list)


def get_qa_link_list(url):
    qa_link_list = []

    # 過剰な負荷を避けるため，１ページ分のリンクリストを取得する前に 1〜3秒休む
    time.sleep(random.randrange(1, 3))

    res = requests.get(url)
    soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
    qa_list = soup.find("div", {"id": "qa_lst"})
    qa_atag_list = qa_list.find_all("a")
    for qa_atag in qa_atag_list:
        qa_link_list.append(qa_atag["href"])
    return qa_link_list


def get_yahoo_chiebukuro_text(category_id, sort_mode="回答数の多い順", qa_stat="解決済み", max_qa_num=10, page_count=1):
    base_url = "https://chiebukuro.yahoo.co.jp/category/{}/question/list?flg={}&sort={}&page={}"
    sort_id = MAIN_SORT_KEY[sort_mode]
    qa_stat_id = QA_STAT[qa_stat]

    print("* launching the process ... ")
    qa_link_list = []
    for page in range(1, page_count + 1):
        print(f"** retrieving QA links from page #{page} ... ", end="")
        url = base_url.format(category_id, qa_stat_id, sort_id, page)
        qa_link_list_sub = get_qa_link_list(url)
        qa_link_list.extend(qa_link_list_sub)
        print(f"{len(qa_link_list_sub)} links retrieved.")
        if max_qa_num < len(qa_link_list):
            break

    # 指定された個数までのQ&Aしか取得しない（デフォルトでは10）
    qa_link_list = qa_link_list[:max_qa_num]

    text_list = []
    for qa_link in qa_link_list:
        print(f"** retrieving QA from {qa_link} ... ")
        text_list.append(get_qa_text(qa_link))
        print("** retrieving QA done.")
    print("* done.")

    return "".join(text_list)


if __name__ == "__main__":
    import sys

    CATEGORY = {"恋愛相談": 2078675272, "大学受験": 2079405665, "住宅": 2078297940, "話題の人物": 2078297579}
    text = get_yahoo_chiebukuro_text(CATEGORY["話題の人物"])
    with open(sys.argv[1], "w") as fo:
        fo.write(text)
