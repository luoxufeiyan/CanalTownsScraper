from get_char_info import CharInfo

if __name__ == '__main__':
    ci = CharInfo()
    char_df = ci.get_char_info()  # 获取人物属性
    char_df.to_csv('out/char.csv')
