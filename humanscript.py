# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 10:36:56 2017

@author: Nzix
"""

import urllib,urllib2,re,datetime,time,random,xlrd,xlwt,os

cookie = ""

def ticketcheck(membercode,serial_code_1,serial_code_2):
    
    timeout = 3

    global cookie

    if type(membercode) is int:
        membercode = str(membercode)
    teamcode = membercode[0] + "0" + membercode[1]
    link = "http://akb48-sousenkyo.jp/vote.php?membercode=%s&parent=team&parentkey=%s"%(membercode,teamcode)
    attempt = 0
    result = ""
    proxy = 0

    while True:

        attempt = attempt + 1
        if attempt > 3:
            break

        time.sleep(0.5 + random.random())

        headers={}
        headers["Host"] = "akb48-sousenkyo.jp"
        headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1"
        if cookie != "":
            headers["Cookie"] = cookie

        access = urllib2.Request(url=link, headers=headers)

        reconnect = 5
        while True:
            try:
                response = urllib2.urlopen(access,timeout=timeout)
            except:
                reconnect = reconnect - 1
                if reconnect <= 0:
                    exit()
            else:
                print u"网页加载完毕"
                break

        if "set-cookie" in response.headers:
            cookie = response.headers["set-cookie"]
            print u"新会话Cookie"

        votepage = response.read().decode('shift-jis').encode('utf-8')
        
        data = {}
        data["serial_code_1"] = serial_code_1
        data["serial_code_2"] = serial_code_2
        
        form = re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"',votepage)

        for item in form:
            if item[1] != "":
                data[item[0]] = item[1]
        
        data = urllib.urlencode(data)
        
        headers["Cookie"] = cookie
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Origin"] = "http://akb48-sousenkyo.jp"
        headers["Referer"] = link
        
        if attempt == 1:
            timesleep = 5 + random.random() * 2.5
            print u"填写票号中... (%fs)"%timesleep
        else:
            timesleep = 1 + random.random() * 2
            print u"票号无需改动"

        print serial_code_1
        print serial_code_2

        time.sleep(timesleep)

        print u"点击提交"

        submit = urllib2.Request(url="http://akb48-sousenkyo.jp/vote_thanks.php",data=data,headers=headers)
        try:
            response = urllib2.urlopen(submit,timeout=timeout)
        except:
            result = "submit failed"
            print u"网页未响应，后退"
            continue
        
        if response.geturl() != "http://akb48-sousenkyo.jp/vote_thanks.php":
            result = "session fault"
            print u"终端会话超时，后退"
            continue
            
        statuspage = response.read().decode('shift-jis').encode('utf-8')
        message = re.search(r'<p class="mb20">([\s\S]+?)</p>',statuspage).group(1)
        message = re.sub(r'\s*',"",message)
        

        if message.find('ｼﾘｱﾙﾅﾝﾊﾞｰに誤りがあります。ご確認ください。') != -1:
            result = "serial number error"
            print u"票号无效"
            break
        elif message.find('入力されたｼﾘｱﾙﾅﾝﾊﾞｰは、既に投票されています。') != -1:
            timestr = re.search(r'\d{4}年\d{2}月\d{2}日\d{2}時\d{2}分\d{2}秒',message).group(0)
            jptime = datetime.datetime.strptime(timestr,'%Y年%m月%d日%H時%M分%S秒')
            cntime = jptime - datetime.timedelta(days = 1)
            result = "pass muster (%s)"%cntime.strftime('%Y-%m-%d %H:%M:%S GMT+8')
            print u"验票成功，投票时间：%s"%(cntime.strftime('%Y年%m月%d日 %H时%M分%S秒').decode("utf-8"))
            print u"后退"
            break
        elif message.find('入力されたｼﾘｱﾙﾅﾝﾊﾞｰは無効であるか既に投票済みです。') != -1:
            result = "others vote"
            print u"他人投票"
            break
        elif message.find('ご投票いただきありがとうございました。') != -1:
            result = "proxy voting"
            proxy = 1
            attempt = 1
            print u"代投成功"
            print u"后退"
            continue
        else:
            result = "unknown error (%s)"%message
            break

    if proxy == 1:
        result = result + " (proxy)"

    return result




allfiles = os.listdir('./xls/')
if len(allfiles) == 0:
    print "no tickets need to check"
    exit()
 
alltickets = []

for filename in allfiles:
    data = xlrd.open_workbook('./xls/' + filename)
    sheet1 = data.sheets()[0]
    rows = sheet1.nrows
    columns = sheet1.ncols
    
    offsetx = 0
    offsety = 0

    for i in xrange(0,rows*columns):
        if type(sheet1.cell_value(i//columns,i%columns)) is unicode:
            if re.search(r'^\s*\w{8}\s*$',sheet1.cell_value(i//columns,i%columns)) != None:
                offsetx = i//columns
                offsety = i%columns
                break
    
    for r in xrange(offsetx,rows):
        row = []
        if type(sheet1.row_values(r)[offsety]) is unicode and type(sheet1.row_values(r)[offsety + 1]) is unicode:
            if re.search(r'^\s*\w{8}\s*$',sheet1.row_values(r)[offsety])!=None and re.search(r'^\s*\w{8}\s*$',sheet1.row_values(r)[offsety + 1])!=None:
                row.append(re.sub(r'\s*',"",sheet1.row_values(r)[offsety]))
                row.append(re.sub(r'\s*',"",sheet1.row_values(r)[offsety + 1]))
                alltickets.append(row)
            else:
                print "[error]",filename,"line",r+1," ",sheet1.row_values(r)[offsety],sheet1.row_values(r)[offsety + 1]
        else:
            print "[error]",filename,"line",r+1," ",sheet1.row_values(r)[offsety],sheet1.row_values(r)[offsety + 1]

total = len(alltickets)
bits = len(str(total))
print u"工作量 %d票"%total

output = []
for t in xrange(0,total):
    serial_code_1 = alltickets[t][0]
    serial_code_2 = alltickets[t][1]

    print u"第%d票"%(t+1)
    result = ticketcheck(1307,serial_code_1,serial_code_2)
        
    # print str(t+1).zfill(bits)," ",serial_code_1,serial_code_2," ",result
    output.append([serial_code_1,serial_code_2,result])    
    
    
workbook = xlwt.Workbook()
sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)

for i in xrange(0,total):
    sheet1.write(i,0,output[i][0])
    sheet1.write(i,1,output[i][1])
    sheet1.write(i,2,output[i][2])

workbook.save('output.xls')
print u"完成"