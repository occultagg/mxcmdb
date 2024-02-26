> 本项目只是用于归档早已不再更新
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
- 登录后主页
  ![](https://github.com/occultagg/mxcmdb/blob/main/screenshot/login.png)
- 项目列表
  支持模板导入,支持手动录入,以表格方式展示,支持前端搜索(js脚本名)
  ![项目列表](https://github.com/occultagg/mxcmdb/blob/main/screenshot/projects-list.png)
  ![手动录入](https://github.com/occultagg/mxcmdb/blob/main/screenshot/manumally.png)
  ![项目信息](https://github.com/occultagg/mxcmdb/blob/main/screenshot/server-list.png)
- 运维文档
  markdown渲染,在线markdown编辑器
  ![运维文档](https://github.com/occultagg/mxcmdb/blob/main/screenshot/docs.png)
  ![在线编辑](https://github.com/occultagg/mxcmdb/blob/main/screenshot/markdown-editor.png)
- 数据统计
  定时任务获取数据写入influxdb,通过e-chart展示
  ![数据统计](https://github.com/occultagg/mxcmdb/blob/main/screenshot/data.png)

