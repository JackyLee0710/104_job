import csv
import tkinter as tk
import webbrowser
from tkinter import ttk
from crawler_search_104_tkinter import get_104_info
from pathlib import Path
from analysis_104_tk import analysis_csv
import time


root = tk.Tk()
root.title('104找工作')


def button_event():
    # print(myentry.get())
    # print(myentry2.get())
    # 顯示正在搜尋
    time_start = time.time()
    my_message.delete(0.0, tk.END)
    my_message.insert(tk.END, "搜尋中...請稍等...")
    my_message.update()
    get_104_info(myentry.get(), myentry2.get())
    with open(f'{myentry.get()}相關職缺.csv', 'r', newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        # 讀取csv檔
        my_message.delete(0.0, tk.END)
        my_message.insert(tk.END, f"{'-'*20}已經將下列職缺資訊存成\"{myentry.get()}相關職缺.csv\"{'-'*20}\n")
        for row in reader:
            my_message.insert(tk.END, f"\n{row[0]:　<24}{row[1]:　<24}\n")
    time_end = time.time()
    time_check.set(f"這次搜尋共花費了{(time_end - time_start):.2f}秒")


def analysis_data():
    analysis_win = tk.Toplevel(root)
    analysis_win.title('關鍵字分析')
    # 找出當前資料夾所有csv檔
    file_list = []
    files = Path(".").glob("*.csv")
    for file in files:
        file_list.append(file)
    label_1 = tk.Label(analysis_win, text='分析檔案：')
    label_1.grid(row=0, column=0)
    combo_1 = ttk.Combobox(analysis_win, values=file_list)
    combo_1.grid(row=0, column=1)
    combo_1.current(0)

    label_2 = tk.Label(analysis_win, text='關鍵字比較：')
    label_2.grid(row=1, column=0)

    default_search = tk.StringVar()
    entry_2 = tk.Entry(analysis_win, textvariable=default_search, width=22)
    entry_2.grid(row=1, column=1)
    default_search.set(r"python.c\+\+.java.sql.linux")

    def analysis_data():
        csv_file = combo_1.get()
        words = entry_2.get()
        analysis_csv(csv_file, words)

    button_1 = ttk.Button(analysis_win, text='Analysis', command=analysis_data)
    button_1.grid(row=2, column=1, sticky='w')


def opencsv():
    # 建一個新視窗
    csvreview = tk.Toplevel(root)
    csvreview.title('職缺詳細資訊')

    # 取得當前目錄下的所有csv檔名稱
    file_list = []
    files = Path(".").glob("*.csv")
    for file in files:
        file_list.append(file)

    label_file = tk.Label(csvreview, text='選擇檔案：')
    label_file.grid(row=0, column=0, sticky='e')

    combo_file = ttk.Combobox(csvreview, value=file_list)
    combo_file.grid(row=0, column=1, sticky='w')
    combo_file.current(0)

    # 下拉選單選中一個csv檔後的行為
    def file_selected(event):
        new_job_list = []
        with open(f'{combo_file.get()}', 'r', newline='', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            # 讀取csv檔
            count = 0
            for row in reader:
                if count == 1:
                    new_job_list.append(f"{row[0]} {row[1]}")
                count = 1
        combo_jobs['value'] = new_job_list

    combo_file.bind("<<ComboboxSelected>>", file_selected)

    label_jobs = tk.Label(csvreview, text='選擇職缺：')
    label_jobs.grid(row=1, column=0, sticky='e')

    job_list = ["--"]
    combo_jobs = ttk.Combobox(csvreview, value=job_list, width=70)
    combo_jobs.grid(row=1, column=1, sticky='w')
    combo_jobs.current(0)

    content = tk.Text(csvreview, height=20, width=100, bd=4)
    content.grid(row=3, column=0, columnspan=2)

    def job_selected(event):
        with open(f'{combo_file.get()}', 'r', newline='', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            # 讀取csv檔
            for row in reader:
                if f"{row[0]} {row[1]}" == combo_jobs.get():
                    content.delete(0.0, tk.END)
                    content.insert(tk.END, f"職缺：\n{row[0]}\n\n公司名稱：\n{row[1]}\n\n工作地點：\n{row[2]}\n\n工作內容：\n{row[3]}\n"
                                           f"\n科系需求：\n{row[4]}\n\n工具：\n{row[5]}\n\n需求技能：\n{row[6]}\n\n其他條件：\n{row[7]}\n\n")
                    url = row[8]

                    def callback(url):
                        webbrowser.open_new(url)

                    link1 = tk.Label(csvreview, text="網站連結", fg="blue", cursor="hand2")
                    link1.grid(row=4, column=1, sticky='e')
                    link1.bind("<Button-1>", lambda e: callback(url))

    combo_jobs.bind("<<ComboboxSelected>>", job_selected)


mylabel = tk.Label(root, text='職缺關鍵字：')
mylabel.grid(row=0, column=0, sticky='e')
searching = tk.StringVar()
myentry = tk.Entry(root, textvariable=searching)
myentry.grid(row=0, column=1, sticky='w')
searching.set("python")

mylabel2 = tk.Label(root, text='顯示頁數：')
mylabel2.grid(row=1, column=0, sticky='e')
page = tk.StringVar()
myentry2 = tk.Entry(root, textvariable=page)
myentry2.grid(row=1, column=1, sticky='w')
page.set("1")

my_message = tk.Text(root, height=20, width=100, bd=4)
# columnspan => 合併0,1欄
my_message.grid(row=3, column=0, columnspan=2)
scrollbar1 = tk.Scrollbar(root, command=my_message.yview)
my_message.configure(yscrollcommand=scrollbar1.set)
scrollbar1.grid(row=3, column=2, sticky=tk.NS)
my_message.insert(tk.END, "會在104搜尋輸入的關鍵字相關職缺，並存成csv檔\n可以調整搜尋頁數，每頁大約會有20個結果\n搜尋後請稍等幾秒鐘，每頁內容約需要2-3秒存取")

mybutton = ttk.Button(root, text='Search', command=button_event)
mybutton.grid(row=2, column=1, sticky='w')

buttonExample = ttk.Button(root, text="內容分析", command=analysis_data)
buttonExample.grid(row=1, column=1, sticky='e')

time_check = tk.StringVar()
exec_time = tk.Label(root, textvariable=time_check)
exec_time.grid(row=2, column=1, sticky='e')

button_3 = ttk.Button(root, text='詳細資訊', command=opencsv)
button_3.grid(row=0, column=1, sticky='e')

root.mainloop()
