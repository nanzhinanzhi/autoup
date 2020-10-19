# -*- coding: UTF-8 -*-
from email.mime.text import MIMEText
from email.header import Header
import requests,json,time,datetime,smtplib
loginurl ='http://hmgr.sec.lit.edu.cn/wms/healthyLogin'
uploadurl = 'http://hmgr.sec.lit.edu.cn/wms/addHealthyRecord'
queryurl = 'http://hmgr.sec.lit.edu.cn/wms/healthyRecordByUser?'
headers ={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
"Content-Type": "application/json"
}
data = {
        "cardNo": "用户名",
        "password": "SHA256加密后的密码"
    }
# 用户列表，在这里补充用户名，密码，email.
userlist =[{
    "username": "user1",
    "password": "ps1",
    "email"   : "email1"
},
    {
    "username": "user2",
    "password": "ps2",
    "email"   : "email2"
    }]
# 密码SHA256加密
# 登录
def gettoken(data):
    res = requests.post(url=loginurl,headers=headers,data=json.dumps(data))

    if res.status_code ==200:
        print("登录")
        print("请求成功:打印返回内容及token")
        s=json.loads(res.text)
        print(s)
        print(s["data"]["token"])
    else:
        print('请求失败')
    with open('./登录.json', 'w') as fp:
        json.dump(res.text, fp)
    return s

# 提交
def upload():
    updata = {
    "abroadInfo": "",
    "caseAddress": None,
    "contactAddress": "",
    "contactCity": "",
    "contactDistrict": "",
    "contactPatient": "1000904",
    "contactProvince": "",
    "contactTime": None,
    "cureTime": None,
    "currentAddress": "洛阳理工学院",
    "currentCity": "410300",
    "currentDistrict": "410311",
    "currentProvince": "410000",
    "currentStatus": "1000705",
    "diagnosisTime": None,
    "exceptionalCase": 0,
    "exceptionalCaseInfo": "",
    "friendHealthy": 0,
    "goHuBeiCity": "",
    "goHuBeiTime": None,
    "healthyStatus": 0,
    "isAbroad": 0,
    "isInTeamCity": 1,
    "isTrip": 0,
    "isolation": 0,
    "mobile": "",
    "peerAddress": "",
    "peerIsCase": 0,
    "peerList": [],
    "reportDate": "",
    "seekMedical": 0,
    "seekMedicalInfo": "",
    "selfHealthy": 0,
    "selfHealthyInfo": "",
    "selfHealthyTime": None,
    "teamId": 3,
    "temperature": "36.5",
    "temperatureNormal": 0,
    "temperatureThree": "",
    "temperatureTwo": "",
    "travelPatient": "1000803",
    "treatmentHospitalAddress": "",
    "tripList": [],
    "userId": "",
    "villageIsCase": 0
    }
    s = gettoken(data)
    headers["token"]=s["data"]["token"]
    updata["mobile"] = s["data"]["mobile"]
    updata["userId"]=s["data"]["userId"]
    print("打印修改后的header和updata")
    print(headers)
    print(time.strftime("%Y-%m-%d", time.localtime()))
    updata["reportDate"] = time.strftime("%Y-%m-%d", time.localtime())
    res = requests.post(url=uploadurl,headers=headers,data=json.dumps(updata))
    print(json.dumps(updata))
    if res.status_code==200:
        print("提交成功")
        # print(res.text)
# 拼接查询url
def addparam(url, data):
        print(len(data))
        keys = list(data.keys())
        print(keys)
        print(keys[0])
        paramlist = []
        for i in range(len(data)):
            print(i)
            param = keys[i]
            print(keys[i])
            print(data[param])
            paramlist.append(param + "=" + str(data[param]))
            print(param)
        print(paramlist)
        url = url + '&'.join(paramlist)
        print(url)
        return url
def mail(s,receivers):
    # 第三方 SMTP 服务
    mail_host = ""  # 设置服务器
    mail_user = ""  # 用户名
    mail_pass = ""  # 口令
    sender = '' #发送邮件账号
    receivers = receivers # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(str(s['data']['list'][15]), 'plain', 'utf-8')
    message['From'] = Header("难知", 'utf-8')
    message['To'] = Header("客户端", 'utf-8')

    subject = "健康汇报成功"
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def date():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=15)
    startTime = (now - delta).strftime('%Y-%m-%d')
    print(startTime)
    endTime = time.strftime("%Y-%m-%d", time.localtime())
    print(endTime)
    return startTime, endTime
# 邮件

# 查询
def query(queryurl,heads,s,receivers):
    data = {
        "pageNum": 1,
        "pageSize": 20,
        "teamId": 3,
        "userId": "",
        "startTime": "2020-10-04",
        "endTime": "2020-10-19"
    }

    headers["token"]=s["data"]["token"]
    startTime, endTime = date()
    data['startTime'] = startTime
    data['endTime'] = endTime
    data["userId"] = s["data"]["userId"]
    queryurl = addparam(queryurl,data)
    res = requests.get(url=queryurl, headers=headers)
    if res.status_code == 200:
        print("请求成功")
        s = json.loads(res.text)
        print(s)
        if (s['data']['list'][15]!=None):
            mail(s,receivers)

    else:
        print('请求失败')

for i in range(len(userlist)):
    data['cardNo'] = userlist[i]['username']
    data['password'] = userlist[i]['password']
    upload()
    print("验证")
    s = gettoken(data)
    query(queryurl,headers,s,userlist[i]['email'])
