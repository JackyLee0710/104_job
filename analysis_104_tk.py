import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pylab import mpl

# 設為中文
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

def analysis_csv(name, words):

    # 開啟 CSV 檔案
    csvfile = open(name, newline='', encoding='utf8')
    rows = csv.reader(csvfile)

    keywords = words.split(".")
    # print(keywords)
    point = []

    # 以迴圈輸出每一列
    for keyword in keywords:
        csvfile.seek(0)
        print(keyword, end="")
        include_word = 0
        count = 0
        for row in rows:
            count += 1
            count_key = 0
            for element in row:
                result = re.compile(keyword.lower()).search(element.lower())
                if result is not None:
                    count_key = 1
            include_word += count_key
            # print(include_word, count)
        count -= 1
        point.append(include_word * 100 / count)
        print(f"\t{include_word*100/count:.1f}%")
    csvfile.close()

    # 取代掉跳脫字符
    a = []
    characters = "\\"
    for keyword in keywords:
        for x in range(len(characters)):
            keyword = keyword.replace(characters[x], "")
            a.append(keyword)
        # print(keyword)

    df = pd.DataFrame({'percent': point},
                      index=a)
    print(df)
    plot = df.plot.pie(y='percent',
                       title='關鍵字占比分析',
                       autopct='%1.1f%%')

    plt.legend(a, loc="best")

    plt.show()

# python.c\+\+.java.sql.linux
