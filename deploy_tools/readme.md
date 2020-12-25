自动化配置服务器和部署WEB服务
=======================
    
##一、自动化的启动

在本地，以 windows 10 操作系统为例：

    pip install fabric3 -i https://mirrors.aliyun.com/pypi/simple
    cd deploy_tools
    set DOMAIN=records-staging.dyez.internal
    set USERNAME=dyez221
    fab deploy:host=%USERNAME%@%DOMAIN%

##二、自动化运行步骤的手动方式解析

###（一）、在服务器上，安装相关软件

以 Ubuntu 18.04.3 LTS 为例（已经安装 Python 3.6, pip, 和 git）： 

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3-venv nginx
    

### （二）、在服务器上，获取代码，安装相应的 python 包，并准备静态文件和数据库

    export DOMAIN=records-staging.dyez.internal
    mkdir -p ~/sites/$DOMAIN
    cd ~/sites/$DOMAIN
    python3 -m venv virtualenv
    git clone https://gitee.com/zjdyez/StudentCenter.git .
    ./virtualenv/bin/pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
    ./virtualenv/bin/python manage.py collectstatic --noinput
    ./virtualenv/bin/python manage.py migrate --noinput
    touch .env
    echo DJANGO_DEBUG_FALSE=y >> .env
    echo DOMAIN=$DOMAIN >> .env
    echo DJANGO_SECRET_KEY=$(
        python3 -c"import random; print(''.join(random.SystemRandom().
        choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50)))"
        ) >> .env
    unset DJANGO_SECRET_KEY DJANGO_DEBUG_FALSE DOMAIN
    set -a; source .env; set +a

### （三）、在服务器上，配置 Nginx 的虚拟主机

    cd ~/sites/$DOMAIN
    cat ./deploy_tools/nginx.template.conf \
    | sed "s/DOMAIN/$DOMAIN/g" \
    | sudo tee /etc/nginx/sites-available/$DOMAIN
    sudo ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/$DOMAIN
    readlink -f /etc/nginx/sites-enabled/$DOMAIN
    sudo rm /etc/nginx/sites-enabled/default
    sudo systemctl start nginx
    sudo systemctl reload nginx

### （四）在服务器上，配置 gunicorn

    cd ~/sites/$DOMAIN
    cat ./deploy_tools/gunicorn-systemd.template.service \
    | sed "s/DOMAIN/$DOMAIN/g" \
    | sudo tee /etc/systemd/system/gunicorn-$DOMAIN.service
    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn-$DOMAIN
    sudo systemctl start gunicorn-$DOMAIN
    sudo journalctl -u gunicorn-$DOMAIN
         
##三、知识点

###（一）、配置服务器（Provisioning）

    1、获得一个服务器的账号和主目录（可登录服务器，且具有sudo权限）
    2、安装python、pip、venv、nginx
    3、配置nginx 和 gunicorn
    
###（二）、 部署WEB服务（Deployment）

    1、在服务器上，创建站点目录（~/sites/DOMAIN）
    2、准备代码（git pull）
    3、创建 python 虚拟环境
    4、安装 python 包，包括 django、gunicorn等
    5、准备数据库
    6、收集静态文件
    7、启动gunicorn服务
    8、功能测试（FT）
    
### （三）、目录结构

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc