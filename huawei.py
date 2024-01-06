from connection import Net
class huawei_device(Net):
    def __init__ (self):
        super().__init__('huawei','192.168.200.1','admin1','Admin@2023')

    def get_config(self):
        cmd='display cu'
        info=self.device.send_command(cmd)
        data_str=info.split('\n')[1:]
        return data_str

    
    def get_interface(self):
        cmd='display ip int brief'
        info=self.device.send_command(cmd)
        data_list=[]
        for line in info.split('\n')[12:]:
            line_list=line.split()
            if_name=line_list[0]
            if_ip=line_list[1]
            status=line_list[-1]
            data_list.append({
                'name':if_name,
                'ip':if_ip,
                'status':status
            })
        return  data_list
    
    def recover_interface(self,if_name):
        self.connect()
        cmd_list=[f'interface{if_name}','undo shutdown']
        self.device.send_config_set(cmd_list)
    
    def get_route(self):
        cmd = 'dis ip routing-table'
        info=self.device.send_command(cmd)
        data_str='\n'.json([line for line in info.split('\n') if '/' in line])
        return data_str
    
    def post_route(self,dst_n,mask,next):
        self.connect()
        cmd_list=[f'ip route-static {dst_n} {mask} {next}']
        self.device.send_config_set(cmd_list)

    def monitor(self):
        cpu_cmd='dis cpu-usage'
        cpu_info=self.device.send_command(cpu_cmd)
        line=cpu_info.split('\n')[2].split('five seconds:')[1]
        cpu_list=line.split('%')
        data_dict={
            'cpu_5s':cpu_list[0][-1:],
            'cpu_1m':cpu_list[2][-1:],
            'cpu_5m':cpu_list[2][-1:]
        }
        return data_dict