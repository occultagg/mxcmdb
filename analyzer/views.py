from django.shortcuts import render
from cmdb.models import Project
from django.db.models import Q
from influxdb import InfluxDBClient
from django.conf import settings
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def analyzer(request, days=1):
    print(request.method)
    projects = Project.objects.filter(~Q(name='运维'), Q(env='prod'))
    #获取iinfluxdb数据
    res = {}
    host = settings.INFLUXDB['HOST']
    port = settings.INFLUXDB['PORT']
    db = settings.INFLUXDB['DATABASE']
    user = settings.INFLUXDB['USER']
    passwd = settings.INFLUXDB['PASSWD']
    client = InfluxDBClient(host, int(port), user, passwd, db)
    
    #influxdb中无数据就跳出
    query = "SELECT * FROM cnt_data"
    try:
        test = client.query(query)
    except:
        print('ERROR-influxdb连接失败.')
        return render(request, 'analyzer/analyzer.html', context={'error_message': '连接influxdb失败.'})

    if not test:
        return render(request, 'analyzer/analyzer.html', context={'error_message': 'influxdb无数据.'})

    #生成x轴
    #获取最新时间    
    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    x = [now.strftime('%Y/%m/%d-%H时')]
    count = 0
    _ = now
    while count < 24*days:
        _ = _ - datetime.timedelta(hours=1)
        x.append(_.strftime('%Y/%m/%d-%H时'))
        count += 1
    x.reverse() 

    #根据x轴时间获取y轴数据
    for proj in projects:
        y = []
        for time in x:
            proj_name = proj.name + '-' + proj.get_env_display()
            x_point = datetime.datetime.strptime(time, '%Y/%m/%d-%H时')
            x_next_point = x_point + datetime.timedelta(hours=1)
            query = "SELECT * FROM cnt_data WHERE proj_name='{}' and time>='{}' and time<'{}' tz('Asia/Shanghai');".format(proj_name, x_point, x_next_point)
            #print(query)
            y_point = client.query(query)
            y_data = list(y_point.get_points(measurement='cnt_data'))
            if y_data == [] or y_data[0]['value'] == -1:
                data = 'null'
            elif len(y_data) > 1:
                return render(request, 'analyzer/analyzer.html', context={'error_message': '数据采集周期设置有误,请设置为1小时并清除问题数据.'})
            else:
                data = y_data[0]['value']
            y.append(data)
        res[proj_name] = y

    project_list = list(res.keys()) 
    context = {
        'project_list': project_list,
        'res': res,
        'x': x,
        'days': days,
    }
    return render(request, 'analyzer/analyzer.html', context=context)
