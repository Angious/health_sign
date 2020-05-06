# 某高校自动健康打卡脚本

### 安装依赖：

    win/pycharm控制台：
    pip install -r requirements.txt
    Linux非root用户：
    sudo pip install -r requirements.txt
    
### 功能与原理：

使用最为简单的selenium模块+chromedriver实现模拟网页自动点击，为确保稳定，使用江科大VPN访问信息门户。
生成两个36.0-36.9的随机体温填写到表单内。

    temp1 = random.randint(360, 369) * 0.1
    temp2 = random.randint(360, 369) * 0.1
    temp1 = str(temp1)[0:4]
    temp2 = str(temp2)[0:4]
    print("生成的随机体温为：",temp1,temp2)   
    
模拟提交。如果后期网页产生变化可能需要更新代码，你也可以自己添加xpath语法查找输入框使用.sendkeys()语句填写表单


### wxpusher微信推送提醒：
http://wxpusher.zjiecode.com/admin/微信扫码登入，
创建应用，应用APPToken号填入APPToken，
打开微信，扫描应用二维码关注，
在微信下方点击我的->我的UID

### chromedriver安装：
+ Windows下

参考：https://www.cnblogs.com/lfri/p/10542797.html
查看你的Chrome版本：
谷歌浏览器中输入chrome://version/
我的是：
Google Chrome	81.0.4044.129 (正式版本) （64 位） (cohort: Stable)
去https://npm.taobao.org/mirrors/chromedriver/下载大版本与本机Chrome版本对应的chromedriver_win32.zip

+ Linux服务器下：

https://www.cnblogs.com/myvic/p/9450134.html 

配置自己chromedriver路径到代码中去

---

##### 常见问题：
1.定时任务并没有执行
    
    这个问题一般会出现在docker容器中，是由于Docker容器时间与宿主机时间不一致导致的。
    通过$date命令查看宿主机时间； 
    
    [root@slave-1 ~]# date
    FrMay 12 11:20:30 CST 2020
    
    进入docker容器（我docker里面的centos7镜像），输入：
    [root@slave-1 ~]# date
    Fri May 12 03:20:33 UTC 2020
    
    时间正好相差8小时，宿主机采用CST时间格式，容器采用UTC时间格式。
    
解决方法：

    1）共享主机的localtime

    创建容器的时候指定启动参数，挂载localtime文件到容器内，保证两者所采用的时区是一致的。
    # docker run -ti -d --name my-nginx -v /etc/localtime:/etc/localtime:ro  docker.io/nginx  /bin/bash
    
    2) 复制主机的localtime
    
    [root@slave-1 ~]# docker cp /etc/localtime 87986863838b:/etc/
     
    然后再登陆容器，查看时间，发现已经跟宿主机时间同步了
    [root@slave-1 ~]# docker exec -ti 87986863838b /bin/bash
    root@87986863838b:/# date                                                                                                                    
    Fri May 12 11:26:19 CST 2017
    3）创建dockerfile文件的时候，自定义该镜像的时间格式及时区。在dockerfile文件里添加下面内容：
    
    ......
    FROM tomcat
    ENV CATALINA_HOME /usr/local/tomcat
    .......
    #设置时区
    RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
    
    保存后，利用docker build命令生成镜像使用即可,使用dockerfile创建的镜像的容器改变了容器的时区，
    这样不仅保证了容器时间与宿主机时间一致（假如宿主机也是CST）,并且像上面使用tomcat作为父镜像的话，JVM的时区也是CST,
    这样tomcat的日志信息的时间也是和宿主机一致的，像上面那两种方式只是保证了宿主机时间与容器时间一致，JVM的时区并没有改变，tomcat日志的打印时间依旧是UTC。

---

2. docker中文乱码

-


    ·  .py文件靠头加上  #coding = utf-8


-
    
    
    ·  容器输入命令：locale
    显示：
    locale: Cannot set LC_CTYPE to default locale: No such file or directory
    locale: Cannot set LC_MESSAGES to default locale: No such file or directory
    locale: Cannot set LC_ALL to default locale: No such file or directory
    LANG=zh_CN.UTF-8
    LANGUAGE=
    LC_CTYPE="zh_CN.UTF-8"
    LC_NUMERIC="zh_CN.UTF-8"
    LC_TIME="zh_CN.UTF-8"
    LC_COLLATE="zh_CN.UTF-8"
    LC_MONETARY="zh_CN.UTF-8"
    LC_MESSAGES="zh_CN.UTF-8"
    LC_PAPER="zh_CN.UTF-8"
    LC_NAME="zh_CN.UTF-8"
    LC_ADDRESS="zh_CN.UTF-8"
    LC_TELEPHONE="zh_CN.UTF-8"
    LC_MEASUREMENT="zh_CN.UTF-8"
    LC_IDENTIFICATION="zh_CN.UTF-8"
    LC_ALL=
    
    
    locale -a查看容器所有语言环境
    
    C
    C.UTF-8
    POSIX
    接着这里是网上的解决方法:
    
    LANG=C.UTF-8
    然后再激活:
    
    source /etc/profile
    然而实际上这样显示是没有出问题了,但是我的hdfs命令却失效了!!!
    
    提示command not find
    
    然而发现不使用激活环境激活语句,直接也就可以看到中文正常显示了,或者使用这样进行环境变量的设置:
    
    export LANG=C.UTF-8
    当容器中其命令语句失效时,注意是否是使用了source /etc/profile语句.
   
    



有问题请提issue

操

