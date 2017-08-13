# -*- coding: UTF-8 -*-
import requests
import cookielib
import urllib
import urllib2
import re
import cgi
from bs4 import BeautifulSoup
from Email import sendmail
import time
#def login():
#    print 'logining......'
#    cookies = {}
#    cookies['ASP.NET_SessionId'] = '1nvceqwfj10gob1a0zuo0nlc'
#    s = requests.get('http://121.248.63.139/nstudent/grgl/xskccjcx.aspx', cookies=cookies)
#    print 'login successful!'
#    return s.content

def check_grad(res):
    #print res
    print 'checking grade in http://121.248.63.139/nstudent/grgl/xskccjcx.aspx.......'
    GRADE_URL = 'http://121.248.63.139/nstudent/grgl/xskccjcx.aspx'
    try:
        grade_html = res.get(GRADE_URL)
        print 'check finished!'
    except urllib2.URLError:
        grade_html = None
        pass
    if grade_html.url == GRADE_URL:
        return grade_html.content
    print 'check not ok!'
    return None


#   while 1:
#       print 'checking your grade......'
#       html_tmp = login()
#       time.sleep(600)
#       html = login()
#       if html.__dict__ ==html_tmp.__dict__:
#           print 'The grade update,please check your email!'
#           sendmail(html)
#       time.sleep(600)

def send_grad(email,html):
    print 'sending email......'
    fromaddr = "swhseu@163.com"
    smtpaddr = "smtp.163.com"
    toaddrs = email
    subject = "最新成绩单"
    password = "*********"
    msg = html
    #print html
    if  msg:
        try:
            sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password)
            print 'send email OK!'
        except:
            print 'send email error!'
            pass


def login(username,password):
    print 'login http://121.248.63.139/nstudent/login.aspx.......'
    LOGIN_URL = 'http://121.248.63.139/nstudent/login.aspx'
    #cj = cookielib.CookieJar()
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #html = opener.open(LOGIN_URL).read()
    res = requests.Session()
    html = res.get(LOGIN_URL).content
    __VIEWSTATE = re.findall('id="__VIEWSTATE" value="(.*?)"', html)
    #print __VIEWSTATE
    __EVENTVALIDATION = re.findall('id="__EVENTVALIDATION" value="(.*?)"', html)
    #print __EVENTVALIDATION
    __EVENTTARGET = re.findall('id="__EVENTTARGET" value="(.*?)"', html)
    #print __EVENTTARGET
    __EVENTARGUMENT = re.findall('id="__EVENTARGUMENT" value="(.*?)"', html)
    #print __EVENTARGUMENT
    # __VIEWSTATE	='/wEPDwULLTE2MDg0ODQ3NzYPZBYCAgEPZBYEAgEPFgIeB1Zpc2libGVnZAIDDxYCHwBoFgICBQ8PFgIeBFRleHQFCeWtmeeCnOiIqmRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQJva5ldVp88yKrXaOxeK2lnzS9ufxkjHW5MiqUNrjqKTja4'
    # __EVENTVALIDATION= '/wEWBAKajurgDQLYhPDxAQLy7cL8AgLB777vDDmTVrDrpi6u4IgKuawuPSZf/MnFmLVPRL+ybyzp4uEJ'
    txt_user = username
    txt_password = password
    okx = "19"
    oky = "10"
    data = {}
    data["__EVENTTARGET"] = __EVENTTARGET
    data["__EVENTARGUMENT"] = __EVENTARGUMENT
    data["__VIEWSTATE"] = __VIEWSTATE
    data["__EVENTVALIDATION"] = __EVENTVALIDATION
    data["txt_user"] = txt_user
    data["txt_password"] = txt_password
    data["ok.x"] = okx
    data["ok.y"] = oky

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId = 1lnvt15vl2t3azwdkdr0bdfe',
        'Upgrade-Insecure-Requests': '1',
        }

    encoded_data = data     #urllib.urlencode(data)
    #print encoded_data
    #request = urllib2.Request(LOGIN_URL, encoded_data, headers=hdr)
    #request.add_header('Accept', 'application/json')
    try:
        s = res.post(LOGIN_URL,data=encoded_data,headers = hdr)
        print 'login successfully!'
        return res
    except urllib2.URLError:
        print 'login error!'
        pass
    return None
    #print s
    #html = res.get('http://121.248.63.139/nstudent/grgl/xskccjcx.aspx')
    #print html.content
    #time.sleep(2)
    #response = opener.open(request)


def main():
    print '-------------------Welcome----------------'
    username = raw_input('Please input your username(eg,163897):')
    password = raw_input('Please input your password:')
    email = raw_input('Please input your email address:')
    res = login(username, password)
    html = check_grad(res)
    send_grad(email, html)
    while 1:
        time.sleep(10)
        res = login(username, password)
        html_update = check_grad(res)
        if html != html_update:
            print 'The grade is updated!'
            send_grad(email,html_update)
            html = html_update
        else:
            print 'The grade is not updated!'


if __name__ == '__main__':
    main()
    #update_cookies()
    #send_grad(login())
    #check_grad()

#print html
#Soup = BeautifulSoup(html, "html.parser")
#feixuewei = Soup.find(id="Datagrid1")
#xuewei = Soup.find(id="dgData")

#tr = feixuewei.findAll("tr") #type:BeautifulSoup
#tr =  str(feixuewei.prettify(formatter="html") + xuewei.prettify(formatter="html")).encode(encoding='st')


#print xuewei
#