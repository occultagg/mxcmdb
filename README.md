> 本项目早已归档并不再更新
# mxcmdb
## 环境要求
- centos7
- python3.7
- influxdb 1.8.10
- mysql 5.7.44
- ES 5(可选)
## 启动步骤
```shell
# 克隆项目创建虚拟环境并安装依赖
git clone
virtualenv -p <python3.7> venv37
source venv37/bin/activate
pip install -r requirement.txt
# 有个版本导致的问题需要手动修复
sed -i "s/query = query.decode(errors='replace')/query = errors='replace'/g" mxcmdb/venv37/lib/python3.7/site-packages/django/db/backends/mysql/operations.py
```
手动创建数据库和用户(包括mysql和influxdb),并修改mxcmdb/settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxcmdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

INFLUXDB = {
    'HOST': '127.0.0.1',
    'PORT': '8086',
    'DATABASE': 'mxcmdb',
    'USER': 'admin',
    'PASSWD': '',
    }
```
```shell
# 数据库初始化
python manager makemigrations
python manager migrate
# 创建django super user
python manager.py createsuperuser
# 启动
python manager runserver
```
## 功能截图
- 主页
  ![](https://github.com/occultagg/mxcmdb/blob/main/screenshot/index.png)
