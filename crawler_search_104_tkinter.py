import requests
import os
import re
import csv
from bs4 import BeautifulSoup
from crawler_104_wo_sele import get_job_info


def get_104_info(search, page_input):
    job_info_list = [["職缺", "公司", "地點", "工作內容", "科系需求", "工具", "需求技能", "其他條件", "104徵才網站"]]

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

    # search = input("請輸入想搜尋的關鍵字：")
    # page_input = input("要看的頁數：")

    try:
        pages = int(page_input)
        if pages < 1:
            pages = 1
    except ValueError:
        pages = 1

    for page in range(1, pages + 1):
        # 1年以下加1~3年：jobexp=1%2C3，1~3年：jobexp=3
        url = f"https://www.104.com.tw/jobs/search/?ro=0&keyword={search}&page={page}&jobexp=1"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        job_lists = soup.select("article.b-block--top-bord.job-list-item.b-clearfix.js-job-item")
        for job_list in job_lists:
            # print(job_list)
            job_url = job_list.select_one("a", {"target": "_blank"})["href"]
            print(f"https:{job_url}")
            job_info = get_job_info(f"https:{job_url}")
            job_info_list.append(job_info)

    # print(job_info_list)
    with open(f'{search}相關職缺.csv', 'w', newline='', encoding="utf8") as csvfile:
        writer = csv.writer(csvfile)
        # 寫入二維表格
        writer.writerows(job_info_list)
    print("\n已經存成csv檔")


if __name__ == '__main__':
    search = input("請輸入想搜尋的關鍵字：")
    page_input = input("要看的頁數：")
    get_104_info(search, page_input)
