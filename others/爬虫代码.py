import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import json
import csv
import time
from bs4 import BeautifulSoup
import random
import os
import _thread



#头部信息
headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "scheme":"https",
    'cache-control':'max-age=0',
}



agent_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
         like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR \
        2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E;\
             rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/83.0.4103.116 Safari/537.36',]

#存储网址
global urls
urls = ['https://www.zhihu.com/people/mileijun']
        

#存储标签
global tags
tags = {}


#存储标题
global titles
titles = {}

#实体类
class User:
    def __init__(self,url):

        #主页地址
        self.url = url

        #姓名
        self.name = ''

        #居住地
        self.position = ''

        #职业
        self.job = ''

        #学校
        self.school = ''

        #性别
        self.gender = ''

        #行业
        self.industry = ''

        #专业
        self.major = ''

        #公司
        self.company = ''


#开始爬行
def crawl():
    #urls = read_data()
    count = 0


    #init()

    while count < 30000 and count < len(urls):
        print("第%d个" % (count + 1))

        url = urls[count]
        try:
            #获取个人信息
            get_user_info(url)


            #获取回答信息连接
            s = get_answer_list(url)

            #通过连接获取回答tag信息
            for u in s:
               get_tag(u)


            #将爬过的网址加入列表
            new_urls = get_follow_list(url)

            for u in new_urls:
                if u not in urls:
                    urls.append(u)

        except BaseException as e:
            print(e)

        print('\n\n')


        count += 1

        #存储数据
        
        




#获取网址的个人信息,返回值是user对象
def get_user_info(url):
    
    l = url.split('/')

    #获取urlToken
    urlToken = l[len(l) - 1]

    #更改头部信息
    headers['user-agent'] = random.choice(agent_list)

    #获取请求
    r = requests.get(url=url,headers=headers,timeout=5)
    r.encoding = 'utf-8'
    html = r.text
    
    user = User(url)
    
    #获取性别
    if html.count('Zi Zi--Male') != 0:
        user.gender = '男'
    elif html.count('Zi Zi--Female') != 0:
        user.gender = '女'
    else:
        user.gender = ''


    #获取初始信息
    soup = BeautifulSoup(html, 'html5lib')
    content = soup.find(id='js-initialData').string

    #解析json,获取有效数据
    parse_json(content,user,urlToken)

    print(user.gender)
    print(user.name)
    print(user.industry)
    print(user.job)
    print(user.major)
    print(user.position)
    print(user.school)

    #多开一个线程保存数据
    try:
        _thread.start_new_thread(save, ('',user))
    except:
        print('Error: 无法启动线程')
    


#解析回答中的tag并保存到本地
def get_tag(url):

    #更改头部信息
    headers['user-agent'] = random.choice(agent_list)

    #获取请求
    r = requests.get(url=url,headers=headers,timeout=5)
    r.encoding = 'utf-8'
    html = r.text

    soup = BeautifulSoup(html, 'html5lib')
    items = soup.find_all(attrs={'class':'Tag QuestionTopic'})

    

    for item in items:
        tag = item.contents[0].contents[0].contents[0].contents[0].string
        if tag not in tags.keys():
            tags[tag] = 1
        else:
            tags[tag] += 1
        print(tag)

    title = soup.find_all(attrs={'class':'QuestionHeader-title'})[0].string

    f = soup.find_all(attrs={'class':'NumberBoard-item'})
    
    num1 = int(f[0].contents[0].contents[1].string.replace(',','')) 
    num2 = int(f[1].contents[0].contents[1].string.replace(',',''))

    print(title+':%d %d\n\n'%(num1,num2))

    if title not in titles:
        titles[title] = [num1,num2]


 




#获取用户的前两个回答连接
def get_answer_list(url):

    if url[-1] == '/':
        url += 'answers'
    else:
        url += '/answers'

    l = url.split('/')

    #获取urlToken
    urlToken = l[len(l) - 1]

    #更改头部信息
    headers['user-agent'] = random.choice(agent_list)

    #获取请求
    r = requests.get(url=url,headers=headers,timeout=5)
    r.encoding = 'utf-8'
    html = r.text

    soup = BeautifulSoup(html, 'html5lib')
    items = soup.find_all(attrs={'class':'List-item'})

    urls_set = set()

    for item in items:
        urls_set.add('https:' + item.contents[0].contents[0].contents[0].contents[2]['href'])
        

    return urls_set




#保存标题和标签到本地
def save_title(n):
    with open(r'D:\csv\title.csv',mode="w",encoding="utf-8",newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['title','follow','pageView'])

        for k,v in titles.items():
            csv_writer.writerow([k,v[0],v[1]])
        f.close()



    with open(r'D:\csv\tag.csv',mode="w",encoding="utf-8",newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['name','count'])
       
        for k,v in tags.items():
            csv_writer.writerow([k,v])
        f.close()


    with open(r'D:\csv\url.txt',mode="w",encoding="utf-8",newline='') as f:
        for url in urls:
            f.write(url+'\n')
        f.write(str(n))

#保存用户到本地
def save(str,user):
    with open(r'D:\csv\zhihu_info.csv',mode="a",encoding="utf-8",newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([user.url,user.name,user.position,user.job,user.school,user.gender,user.industry,user.major,user.company])
        f.close()



#写入用户表头
def init():
    with open(r'D:\csv\zhihu_info.csv',mode="a",encoding="utf-8",newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['url','name','position','job','school','gender','industry','major','company'])
        f.close()


def read_data(n):
    with open(r'D:\csv\title.csv','r',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        column1 = [row[n]for row in reader]
        return column1




#获取关注列表
def get_follow_list(url):
    
    if url[-1] == '/':
        url += 'following'
    else:
        url += '/following'


    #更改头部信息
    headers['user-agent'] = random.choice(agent_list)

    #获取请求
    r = requests.get(url=url,headers=headers,timeout=5)
    r.encoding = 'utf-8'
    html = r.text

    #解析页面
    soup = BeautifulSoup(html, 'html5lib')
    elements = soup.find_all(attrs={'class','UserLink-link'})

    urls_set = set()
    count = 0 

    for element in elements:
        urls_set.add('https:' + element['href'])
        count += 1
        if count > 30:
            break

    return urls_set





#将字符串解析为json对象并获取数据
def parse_json(content,user,urlToken):

    #字符串转json对象
    js = json.loads(content)
    js = js['initialState']['entities']['users'][urlToken]
    print(user.url)

    print(user.gender)

    user.name = js['name']
    print(user.name)
    user.industry = js['business']['name']
    print(user.industry)

    if js['locations']:
        if js['locations'][0]:
            user.position = js['locations'][0]['name']
            print(user.position)


    if js['employments']:
        if 'job' in js['employments'][0]:
            user.job = js['employments'][0]['job']['name']
            print(user.job)
        if  'company' in js['employments'][0]:
            user.company = js['employments'][0]['company']['name']
            print(user.company)

    if js['educations']:
        if 'school' in js['educations'][0]:
            user.school = js['educations'][0]['school']['name']
            print(user.school)
        if 'major' in js['educations'][0]:
            user.major = js['educations'][0]['major']['name']
            print(user.major)

   

    

#获取评论
def get_answers():
    chrome_options = Options()

    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()

    url='https://www.zhihu.com/'


    #进入登入界面
    driver.get(url)

    #点击快捷登录
    driver.find_elements_by_class_name('Login-socialButton')[1].click()

    handles = driver.window_handles

    #切换到新界面
    driver.switch_to_window(handles[2])
    
    #切换到iframe
    iframe = driver.find_element_by_id('ptlogin_iframe')

    driver.switch_to_frame(iframe)

    #点击登录qlogin_list
    element = driver.find_element_by_id('qlogin_list')

    
    element.find_element_by_tag_name('a').click()
    

    driver.switch_to_window(handles[0])

    time.sleep(5)

    url='https://www.zhihu.com/question/51459956'
    
    #进入回答界面
    driver.get(url)



    for i in range(0,20):

        print(len(driver.page_source))


        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        if i == 0:
            driver.execute_script("window.scrollTo(0,-10)")

        time.sleep(2)


    html = driver.page_source

    soup = BeautifulSoup(driver.page_source, 'html5lib')

    items = soup.find_all(attrs={'class':'List-item'})

    for item in items:
        pass

    print(str(items[0].find(attrs={'class':'ContentItem-meta'})))
    

if __name__ == '__main__':
    crawl()
    