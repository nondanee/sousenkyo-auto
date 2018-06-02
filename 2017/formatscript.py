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
                break

        if "set-cookie" in response.headers:
            cookie = response.headers["set-cookie"]

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

        time.sleep(0.5)

        submit = urllib2.Request(url="http://akb48-sousenkyo.jp/vote_thanks.php",data=data,headers=headers)
        try:
            response = urllib2.urlopen(submit,timeout=timeout)
        except:
            result = u"ネットワークタイムアウト"
            continue
        
        if response.geturl() != "http://akb48-sousenkyo.jp/vote_thanks.php":
            result = u"お客様の端末は非推奨です"
            continue
            
        statuspage = response.read().decode('shift-jis').encode('utf-8')
        message = re.search(r'<p class="mb20">([\s\S]+?)</p>',statuspage).group(1)
        message = re.sub(r'\s*',"",message)
        

        if message.find('ｼﾘｱﾙﾅﾝﾊﾞｰに誤りがあります。ご確認ください。') != -1:
            result = u"ｼﾘｱﾙﾅﾝﾊﾞｰに誤りがあります"
            break
        elif message.find('入力されたｼﾘｱﾙﾅﾝﾊﾞｰは、既に投票されています。') != -1:
            timestr = re.search(r'投票日時:\d{4}年\d{2}月\d{2}日\d{2}時\d{2}分\d{2}秒',message).group(0)
            result = timestr.decode("utf-8")
            break
        elif message.find('入力されたｼﾘｱﾙﾅﾝﾊﾞｰは無効であるか既に投票済みです。') != -1:
            result = u"入力されたｼﾘｱﾙﾅﾝﾊﾞｰは無効であるか既に投票済みです"
            break
        elif message.find('ご投票いただきありがとうございました。') != -1:
            result = u"ご投票いただきありがとうございました"
            proxy = 1
            attempt = 1
            continue
        else:
            result = message.decode("utf-8")
            break

    return (result,proxy)




allfiles = os.listdir('./xls/')
if len(allfiles) == 0:
    print "no tickets need to check"
    exit()

if os.path.exists("./output/") == False:
    os.mkdir("./output/")


for filename in allfiles:

    tickets = []

    data = xlrd.open_workbook('./xls/' + filename)
    sheet1 = data.sheets()[0]
    rows = sheet1.nrows
    columns = sheet1.ncols
    
    offsetx = 0
    offsety = 0

    for i in xrange(0,rows*columns):
        if type(sheet1.cell_value(i//columns,i%columns)) is unicode:
            noblankcell = re.sub(u'[\s|(\u3000)|(\xa0)]*',"",sheet1.cell_value(i//columns,i%columns))
            if re.search(r'^\w{8}$',noblankcell) != None:
                offsetx = i//columns
                offsety = i%columns
                break
    
    for r in xrange(offsetx,rows):
        row = []
        if type(sheet1.row_values(r)[offsety]) is unicode and type(sheet1.row_values(r)[offsety + 1]) is unicode:
            noblankcell1 = re.sub(u'[\s|(\u3000)|(\xa0)]*',"",sheet1.row_values(r)[offsety])
            noblankcell2 = re.sub(u'[\s|(\u3000)|(\xa0)]*',"",sheet1.row_values(r)[offsety + 1])
            if re.search(r'^\w{8}$',noblankcell1)!=None and re.search(r'^\w{8}$',noblankcell2)!=None:
                row.append(noblankcell1)
                row.append(noblankcell2)
                tickets.append(row)
            else:
                if noblankcell1 != "" and noblankcell2 != "":
                    row.append(noblankcell1)
                    row.append(noblankcell2)
                    row.append(u'ｼﾘｱﾙﾅﾝﾊﾞｰはそれぞれ8桁ずつ半角英数字で入力してください')
                    tickets.append(row)
                    print "[error]",filename,"line",r+1," ",noblankcell1,noblankcell2
        else:
            print "[error]",filename,"line",r+1," ",sheet1.row_values(r)[offsety],sheet1.row_values(r)[offsety + 1]


    total = len(tickets)
    bits = len(str(total))
    print "%s total %d"%(filename,total)

    output = []
    for t in xrange(0,total):
        serial_code_1 = tickets[t][0]
        serial_code_2 = tickets[t][1]

        if len(tickets[t])==3:
            output.append([serial_code_1,serial_code_2,tickets[t][2],u"否"]) 
            continue

        result = ticketcheck(1307,serial_code_1,serial_code_2)

        if result[1] == 1:
            miss = u"是"
        elif result[1] == 0:
            miss = u"否"
            
        print str(t+1).zfill(bits)," ",serial_code_1,serial_code_2," ",result[0],miss
        output.append([serial_code_1,serial_code_2,result[0],miss]) 
        
        
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)



    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = u'等线'
    # font.colour_index = 2 #red
    font.height = 14 * 20 #16 point
    font.bold = False

    for i in xrange(0,total):

        if output[i][3] == u'否' and re.search(u'投票日時',output[i][2]) != None:
            font.colour_index = 0
        else:
            font.colour_index = 2

        style.font = font

        sheet1.write(i,0,i+1,style)
        sheet1.write(i,1,output[i][0],style)
        sheet1.write(i,2,output[i][1],style)
        sheet1.write(i,3,output[i][2],style)
        sheet1.write(i,4,output[i][3],style)
        sheet1.write(i,5,u'nondanee',style)

    sheet1.col(0).width = 256 * 8
    sheet1.col(1).width = 256 * 14
    sheet1.col(2).width = 256 * 14
    sheet1.col(3).width = 256 * 56
    sheet1.col(4).width = 256 * 8
    sheet1.col(5).width = 256 * 15


    namepart = filename.split(".")[0]

    workbook.save('./output/' + namepart + "-checked.xls")

print "Done"