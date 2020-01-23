import sys
from bs4 import BeautifulSoup
import requests


def get_qa_text(link):
    text_list = []
    res = requests.get(link)
    soup = BeautifulSoup(res.text.encode(res.encoding), 'html.parser')
    qa_text_list = soup.find_all('p', {'class': 'queTxt'})
    for t in qa_text_list:
        text_list.append(t.text)
    return ''.join(text_list)


def get_qa_link_list(url):
    qa_link_list = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text.encode(res.encoding), 'html.parser')
    qa_list = soup.find('ul', {'id': 'qalst'})
    qa_dt_list = qa_list.find_all('dt')
    for qa_link in qa_dt_list:
        link_tag = qa_link.find('a')
        qa_link_list.append(link_tag['href'])
    return qa_link_list


SORT_KEY = {'mod_date': 17, 'q_date': 2, 'vode_date': 3, 'num_ans': 4, 'num_thanks': 8}
KIND_FLAG = {'open_for_answer': 0, 'solved': 1, 'open_for_vote': 2, 'all': 3}


def get_yahoo_chiebukuro_text(did, sort=SORT_KEY['mod_date'], flag=KIND_FLAG['open_for_answer'], count=1):
    base_url = 'https://chiebukuro.yahoo.co.jp/dir/list.php?did={}&flg={}&sort={}&type=list&page={}'
    qa_link_list = []
    for page in range(1, count+1):
        url = base_url.format(did, flag, sort, page)
        qa_link_list.extend(get_qa_link_list(url))

    text_list = []
    for qa_link in qa_link_list:
        text_list.append(get_qa_text(qa_link))
    return ''.join(text_list)


if __name__ == '__main__':
    category = {'恋愛相談': 2078675272, '大学受験': 2079405665, '住宅': 2078297940}
    text = get_yahoo_chiebukuro_text(category['大学受験'], sort=SORT_KEY['num_ans'], count=1)
    with open(sys.argv[1], 'w') as fo:
        fo.write(text)
