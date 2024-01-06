import datetime
from huawei import huawei_device
def create_mail_body(device_name,alert_type,alert_description):
    now_time=str(datetime.datetime.now()).split('.')[0]
    with open('template/head.html', encoding='utf-8') as f:
        text_head = f.read()
    with open('template/body.html', encoding='utf-8') as f:
        text_body = f.read()
    body = text_head + "\n" + text_body.format(device_name, alert_type, alert_description, now_time)
    return body    

def huawei_runner():
    device_name='HuaweiIOS'
    ios_xe=huawei_device()
    huawei_data={}
    huawei_data['config']=ios_xe.get_config()
    huawei_data['interface']=ios_xe.get_interface()
    huawei_data['routeTable']=ios_xe.get_route()
    huawei_data['monitor']={'cpu':ios_xe.monitor()}

    for interface in huawei_data['interface']:
        if interface['status']!='up':
            alert_des=f'{device_name}的接口{interface['name']}被关闭了'
            body=create_mail_body(device_name,'Error',alert_des)
            ios_xe.send_mail(subject='设备接口故障',body=body)

            ios_xe.recover_interface(interface['name'])
            huawei_data['interface']=ios_xe.get_interface()
            print('接口已恢复')

    dst='172.16.10.0'
    mask='255.255.255.0'
    next='192.168.200.100'
    if dst not in huawei_data['routeTable']:
        ios_xe.post_route(dst,mask,next)
        huawei_data['routeTable']=ios_xe.get_route()
        print(f'新增了一条路由指向{dst},数据已更新')

    ios_xe.to_json(huawei_data,'data/huawei.json')
    ios_xe.device.disconnect()