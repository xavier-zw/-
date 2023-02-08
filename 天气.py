import requests
import tkinter
from tkinter import ttk
import re
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def UI(prcouse_dict,stert_url,url_list,city_list):
    prcouse_lsit = list(prcouse_dict.keys())
    ui =tkinter.Tk()
    ui.title("天气信息")
    ui.geometry("750x800")

    variable1 = tkinter.StringVar()
    listbox1 = ttk.Combobox(ui,width=12,textvariable = variable1)
    listbox1["values"]=prcouse_lsit
    listbox1.current(0)
    listbox1.place(relx = 0.1,rely = 0.05)

    button1 = tkinter.Button(ui,text="切换",command=lambda: getUrl_city(stert_url, url_list, city_list, variable1, prcouse_dict,listbox2,text1))
    button1.place(relx=0.3, rely=0.05)

    variable2 = tkinter.StringVar()
    listbox2 = ttk.Combobox(ui,width=12,textvariable = variable2)
    getUrl_city(stert_url, url_list, city_list, variable1, prcouse_dict,listbox2,ui)
    listbox2["values"] = city_list
    listbox2.current(0)
    listbox2.place(relx = 0.4,rely = 0.05)

    button2 = tkinter.Button(ui,text = "查看",command = lambda:getMeaage_weak(listbox2,city_list,url_list,text1,text2))
    button2.place(relx = 0.6,rely = 0.05)

    text1 = tkinter.Text(ui, bd=2, width=98, height=14)
    text1.place(relx=0.05, rely=0.15)

    text2 = tkinter.Text(ui, bd=3, width=98, height=30)
    text2.place(relx=0.05, rely=0.45)

    ui.mainloop()

def getHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("error")

def getUrl_city(stert_url,url_list,city_list,variable1,prcouse_dict,listbox2,text):
    url_list.clear()
    city_list.clear()
    stert_url = stert_url + prcouse_dict[variable1.get()] + ".shtml"
    html = getHtml(stert_url)
    soup = BeautifulSoup(html,"html.parser")
    divs = soup.findAll("div",class_="conMidtab3")
    for div in divs:
        try:
            a = div.find("a", attrs={"href": True})#当不知道标签里的具体属性值匹配是可以用True 也可以用正则表达是匹配
            if a.text in city_list:
                break
            if a.text != "详情":
                url_list.append(a.get("href"))
                city_list.append(a.text)
        except:
            print("error")
    listbox2["values"] = city_list
    listbox2.current(0)

def getMeaage_weak(listbox2,city_list,url_list,text,ui):
    text.delete(0.0,tkinter.END)
    url_dict = dict(zip(city_list,url_list))
    html = getHtml(url_dict[listbox2.get()])
    soup = BeautifulSoup(html,"html.parser")
    lis = soup.find("ul",class_="t clearfix")
    days,temperature,wind,tem = [],[],[],[]
    for li in lis:
        try:
            message = str(li.text)
            message = message.replace("\n"," ")
            message = re.sub(" +"," ",message).strip()
            days.append(message.split(" ")[0])
            tem.append(message.split(" ")[1])
            temperature.append(message.split(" ")[2])
            wind.append(message.split(" ")[3])
        except:
            continue
    text.insert(tkinter.END," |".join(days))
    text.insert(tkinter.END,"\n\n\n")
    text.insert(tkinter.END," | ".join(tem))
    text.insert(tkinter.END, "\n\n\n")
    text.insert(tkinter.END," | ".join(temperature))
    text.insert(tkinter.END, "\n\n\n")
    text.insert(tkinter.END," | ".join(wind))

    maxs = []
    mins = []
    for tems in temperature:
        try:
            maxs.append(int(tems.split("/")[0].replace("℃","")))
            mins.append(int(tems.split("/")[1].replace("℃","")))
        except:
            mins.append(int(tems.split("/")[0].replace("℃","")))
            continue
    fig = plt.figure(figsize=(7, 4.5), dpi=100)
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title("未来一周的天气变化",fontsize = 24)
    plt.xlabel("时间",fontsize =12)
    plt.ylabel("温度 °C",fontsize =12)
    plt.plot(days,maxs,"r-o")
    plt.plot(days, mins, "b-o")
    plt.ylim(min(mins)-10,max(maxs)*2)
    canvs = FigureCanvasTkAgg(fig,ui)
    canvs.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)
    canvs.draw()

if __name__ == '__main__':
    prcouse_dict = {"北京": "beijing", "安徽": "anhui", "重庆": "chongqing", "福建": "fujian", "甘肃": "gansu", "广东": "guangdong",
                    "广西": "guangxi", "贵州": "guizhou", "海南": "hainan", "河北": "hebei", "河南": "henan", "湖北": "hubei",
                    "湖南": "hunan", "黑龙江": "heilongjiang", "吉林": "jilin", "江苏": "jiangsu", "江西": "jiangxi",
                    "辽林": "liaoning",
                    "内蒙古": "neimenggu", "宁夏": "ningxia", "青海": "qinghai", "山东": "shandong", "陕西": "shan-xi",
                    "山西": "shanxi",
                    "上海": "shanghai", "四川": "sichuan", "天津": "tianjin", "西藏": "xizang", "新疆": "xinjiang",
                    "云南": "yunnan",
                    "浙江": "zhejiang", "香港": "hongkong", "澳门": "macao", "台湾": "taiwan"}
    stert_url = "http://www.weather.com.cn/textFC/"
    url_list = []
    city_list = []
    UI(prcouse_dict,stert_url,url_list,city_list)