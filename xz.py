# -*- coding: utf8 -*-
import pdfkit
import requests
import  chardet
import re
from urllib.request import urlopen

path_wk = r'.\wkhtmltopdf\bin\wkhtmltopdf.exe'   #pdf转换工具 ，非windwos系统可自行安装然后指定位置
config = pdfkit.configuration(wkhtmltopdf = path_wk)
# 设置pdf格式
options = {
        'encoding': "utf-8"
    }
# 也可以设置生成pdf的大小等
options = {
        'encoding': "utf-8",
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm'
    }

#获取文章名称
def get_title(url):
    response = requests.get(url)

    if response.status_code == 404 or str(response.status_code)[0:2] == "40":
        return 0
    response2 = urlopen(url, timeout=5)
    html_byte = response2.read()

    charset = chardet.detect(html_byte)['encoding']  # 探测页面的编码方式

    result = requests.get(url)
    if (charset.lower() == "GB2312" or charset.lower() == "gbk"):
        result.encoding = 'gbk'
    else:
        result.encoding = 'utf-8'
    content = result.text
    title = re.findall('<title>(.*)</title>', content)[0]
    return title

#过滤掉部分可能导致文件创建异常的字符
def filename_filter(filename):  
    string1="\/:*?\"<>|"
    #print(string1)
    for s1 in string1:
        filename= filename.replace(s1," ")
        print
    return(filename)


if __name__ == '__main__':
    try:
        for i in range(8590,0,-1):   #逆序循环爬取，注意这里要添加最新文章的页码 https://xz.aliyun.com/t/8590
            try:
                id = str(i)
                print(id)
                url =  "https://xz.aliyun.com/t/" + id
                f = get_title(url)
                if not f:
                    continue
                f = filename_filter(f)
                print(f)
                filename = "./"+id+" ："+f + ".pdf"
                pdfkit.from_url(url, filename, configuration=config,options=options)
            except Exception as e:
                print(str(e))
                pass
    except Exception as e:
        print(str(e))
        pass
