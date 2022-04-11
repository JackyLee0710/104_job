import requests
import json
import time
import random


def get_job_info(url):

    code = url.split("/")[-1].split("?")[0]

    url_request = f"https://www.104.com.tw/job/ajax/content/{code}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'Referer': url_request,
        'x-requested-with': 'XMLHttpRequest'
    }

    r = requests.get(url_request, headers=headers).text
    data = json.loads(r)
    print(data)

    # 職稱
    job = data['data']['header']['jobName']
    # print(job)

    # 公司
    company = data['data']['header']['custName']
    # print(company)

    # 位置
    location = data['data']['jobDetail']['addressRegion'] + data['data']['jobDetail']['addressDetail']
    # print(location)

    # 工作內容
    job_content = data['data']['jobDetail']['jobDescription']
    # print(job_content)

    # 科系
    major = data['data']['condition']['major']
    # print(major)

    # 擅長工具
    tools = data['data']['condition']['specialty']
    all_tools = list()
    for tool in tools:
        all_tools.append(tool['description'])
    # print(all_tools)

    # 工作技能
    skills = data['data']['condition']['skill']
    all_skills = list()
    for skill in skills:
        all_skills.append(skill['description'])
    # print(all_skills)

    # 其他條件
    other_requirement = data['data']['condition']['other']
    # print(other_requirement)

    a = list()
    a.append(job)
    a.append(company)
    a.append(location)
    a.append(job_content)
    a.append(major)
    a.append(all_tools)
    a.append(all_skills)
    a.append(other_requirement)
    a.append(url)

    # time.sleep(random.uniform(1, 2))


    # a = list()
    # a.append(job)
    # a.append(company)
    # a.append(location)
    # a.append(content)
    # print("\n擅長工具：")
    # print("\n工作技能：")
    # a.append(other_req)
    # a.append(url)
    # # print(a)
    #
    # print("\n")
    return a

# get_job_info("https://www.104.com.tw/job/ajax/content/7fbet")
# get_job_info("https://www.104.com.tw/job/ajax/content/71rxc")