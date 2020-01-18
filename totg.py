# encoding=utf8
# !/usr/bin/python
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import time
import js2py
import re

# execute this commands before run this script

# pip install beautifulsoup4
# pip install js2py
# pip install request

# update your userids
pushurl = 'https://api.telegram.org/bot机器人密钥/sendMessage?parse_mode=HTML&disable_web_page_preview=1&chat_id=频道id&text='


def getcookies():
    url = 'https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline'
    js = js2py.EvalJs()
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}

    try:
        aesjs = requests.get("https://www.hostloc.com/aes.min.js", headers=headers, timeout=5).text
    except Exception as e:
        print ('ReturnNothing')
        return 'ReturnNothing'
    # print aesjs
    js.execute(aesjs)
    getcookie = requests.get(url).text
    # print getcookie
    getcookie_script = re.findall("<script>(.*?)</script>", getcookie)
    js.execute(getcookie_script[0].split("document")[0])
    data = js.toHex(js.slowAES.decrypt(js.c, 2, js.a, js.b))
    cookie = "L7DFW=" + data
    print (cookie)
    return cookie


def getnewesttitle():
    url = 'https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}

    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False

    result = 'L7DFW' in cookiestr
    print (result)
    if (result):
        print ('hostloc start AES Decrypt ... ')
        headers = {'Cookie': cookiestr,
                   'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
        r = s.get(url, headers=headers)
    else:
        r = s.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    newest = soup.find('span', class_='by')
    # print newest.text
    author = newest.text
    title = newest.parent.text.replace(author,'')

    pid = r.text[r.text.find('tid') + 4:r.text.find('tid') + 10]
    post_url = "https://www.hostloc.com/thread-{}-1-1.html".format(pid)

    # print post_url
    print ('monitor is runing ,please wait for a monent')

    resultArr = [title, post_url, author]
    return resultArr


def sendmessage(newesttitle, postUrl, author):
    nowtime = time.strftime("%m-%d %H:%M:%S", time.localtime())
    # finalUrl = pushurl+ newesttitle + '&url=' + postUrl
    finalUrl = pushurl + '<b>hostloc新帖提醒</b>' + '\n' + nowtime + ' ' +  author +  '<a href=\"' + postUrl + '\">' + newesttitle + '</a>'

    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    s.get(finalUrl)

    print('send a new message to wechat')


cookiestr = getcookies()
firstArr = getnewesttitle()
newesttitle = firstArr[0]
sendmessage(firstArr[0], firstArr[1], firstArr[2])
while True:
    try:
        time.sleep(30)
        try:
            newArr = getnewesttitle()
        finally:
            time.sleep(5)
            pass
        thenexttitle = newArr[0]
        postUrl = newArr[1]
        author = newArr[2]
        print('monitoring...')
        print('old message is ' + newesttitle.encode('utf-8').decode())
        print('new message is ' + thenexttitle.encode('utf-8').decode())
        print(postUrl.encode('utf-8').decode())
        if thenexttitle != newesttitle:
            newesttitle = thenexttitle
            print('find new message ,reading....')
            sendmessage(thenexttitle, postUrl,author)

            pass
        else:
            pass
    except RuntimeError:
        print(RuntimeError)
    pass
