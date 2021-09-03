import requests
from bs4 import BeautifulSoup
import pandas as pd

# character index page
CHARACTER_LIST_URL = "https://wiki.biligame.com/jiangnan/%E8%A7%92%E8%89%B2%E5%9B%BE%E9%89%B4"
# prefix for character detail page
CHARACHER_DETAIL_PAGE_PREFIX = "https://wiki.biligame.com"


class CharInfo():
    # 获取人物五维属性和天赋，数据均为不升阶版本
    def get_char_info(self):
        # init DataFrame
        char_col_names = ["姓名", "建造", "农牧", "制作", "理财", "探险", "天赋"]
        char_df = pd.DataFrame(columns=char_col_names)
        r = requests.get(CHARACTER_LIST_URL)
        html_str = r.text
        # print(r.status_code) # TODO status check
        soup = BeautifulSoup(html_str, 'html.parser')
        character_lst = soup.find_all('div', attrs={'style': 'z-index: 2;'})
        # get link of each character page
        char_urls = [CHARACHER_DETAIL_PAGE_PREFIX +
                     char.find('a')['href'] for char in character_lst]
        # iterate each character
        for char_url in char_urls:
            r = requests.get(char_url)
            html_str = r.text
            # print(r.status_code)
            soup = BeautifulSoup(html_str, 'html.parser')
            char_name = soup.find(
                'th', attrs={'style': 'font-size:xx-large;font-family:宋体;'}).text.strip()
            char_tianfu = soup.find('div', attrs={'id': 'tf-star2'}).text
            char_jianzao = soup.find('div', attrs={'id': 'Canvas'})[
                'data-value1_50']
            char_nongmu = soup.find('div', attrs={'id': 'Canvas'})[
                'data-value2_50']
            char_zhizuo = soup.find('div', attrs={'id': 'Canvas'})[
                'data-value3_50']
            char_licai = soup.find('div', attrs={'id': 'Canvas'})[
                'data-value4_50']
            char_tanxian = soup.find('div', attrs={'id': 'Canvas'})[
                'data-value5_50']
            char_df = char_df.append({'姓名': char_name, '建造': char_jianzao, '农牧': char_nongmu, '制作': char_zhizuo,
                                     '理财': char_licai, '探险': char_tanxian, '天赋': char_tianfu}, ignore_index=True)
        return char_df
