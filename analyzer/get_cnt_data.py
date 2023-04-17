from cmdb.models import Project
from django.db.models import Q
from django.conf import settings
import json, requests
from influxdb import InfluxDBClient
from datetime import datetime
import os

#获取实时在线用户数
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def get_cnt():
    project_list = Project.objects.filter(~Q(name='运维'), Q(env='prod'), Q(mx_version='5.0'))
    if not project_list:
        print('{}-无生产项目'.format(datetime.now()))

    url_dict = {}
    result = {}
    for proj in project_list:
        url_dict['{}-{}'.format(proj.name, proj.get_env_display())] = '/'.join(str(proj.cp_addr).split('/')[:3])
    #print(url_dict)
    for proj_name in url_dict.keys():
        if not url_dict[proj_name] == 'None':
            #print(url_dict[proj_name])
            url = url_dict[proj_name] + '/im/v5/open/connections'
            html = requests.request('GET', url, headers=header, verify=False)
            if html.status_code == 200:
                cnt = json.loads(html.text)['data']['cache'][0]['cnt']
                result[proj_name] = cnt
            else:
                print('{}-{}-ERROR-{}-{}'.format(datetime.now(),proj_name,url,html.status_code))
                result[proj_name] = -1

    #host = settings.INFLUXDB['HOST']
    #port = settings.INFLUXDB['PORT']
    #db = settings.INFLUXDB['DATABASE']
    #user = settings.INFLUXDB['USER']
    #passwd = settings.INFLUXDB['PASSWD']
    host = os.environ["INFLUXDB_HOST"]
    port = os.environ["INFLUXDB_PORT"]
    db = os.environ["INFLUXDB_DB_NAME"]
    user = os.environ["INFLUXDB_USER"]
    passwd =  os.environ["INFLUXDB_PASSWD"]

    client = InfluxDBClient(host, int(port), user, passwd, db)

    _ = 0
    for proj_name in result.keys():
        body = [
            {
                "measurement": "cnt_data",
                "tags": {
                    "proj_name": proj_name,
                },
                "fields": {
                    "value": int(result[proj_name]),
                },
            }
        ]
        #print(body)
        try:
            res = client.write_points(body)
        except:
            print('{}-数据写入失败'.format(datetime.now()))

        if not res:
            _ += 1
            print('{}-{}-FALSE'.format(str(datetime.now()), proj_name))
            
    if _ == 0:
        print('{}-TRUE'.format(str(datetime.now())))
    print('--------')
