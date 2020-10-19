# 洛阳理工学院健康汇报自动打卡

1. 修改up.py

第17行写入用户名，密码，邮件

```
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
```

第126行设置第三方stmp服务

```
   # 第三方 SMTP 服务
    mail_host = ""  # 设置服务器
    mail_user = ""  # 用户名
    mail_pass = ""  # 口令
    sender = '' #发送邮件账号
```

2. 服务器部署

1.将up.py和run.sh上传到服务器，我这里部署的路径是

```
/root/python_workspace
```

2.安装crontable(我的服务器是centos7)

```
yum install -y crontabs
```

3.赋予执行权限

```
chmod +x run.sh
chmod +x up.py
```

4.创建定时任务

```
crontab -e
5 0  * * * /root/python_workspace/run.sh >/tmp/123.log
crontab -l -u root
```

