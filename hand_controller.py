import serial
import time

class HandController:
    def __init__(self, com_port, baud_rate):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(com_port, baud_rate)
        
        # Define the group to index mapping
        self.cellname_to_index = {
            "偏差调节组": 0,
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10,
            "OK": 11,
            "ROCK": 12,
            "你真棒": 13,
            "剪子": 14,
            "石头": 15,
            "布": 16
        }
    
    def send_command(self, command):
        """
        发送指令到串口

        :param command: 要发送的指令字符串
        :return: None
        """
        if self.ser.is_open:
            self.ser.write(command.encode())
            time.sleep(0.1)  # Give some time for the command to be processed
        else:
            print("Serial port is not open")
    
    def index_pwm_time(self, index, pwm, time_ms):
        """
        发送单个舵机指令，将舵机设置为指定的PWM值并保持指定的时间。

        :param index: 舵机的索引，范围为 0 到 254
        :param pwm: 舵机的PWM值，范围为 0500 到 2500
        :param time_ms: 舵机保持PWM值的时间，范围为 0000 到 9999 毫秒
        :return: None
        """
        command = f'#{index:03d}P{pwm:04d}T{time_ms:04d}!'
        self.send_command(command)
    
    def multiple_index_pwm_time(self, commands):
        """
        发送多个舵机指令，将多个舵机设置为指定的PWM值并保持指定的时间。

        :param commands: 包含多个指令的列表，每个指令为 (index, pwm, time_ms) 形式的元组
        :return: None
        """
        command = '{' + ''.join([f'#{index:03d}P{pwm:04d}T{time_ms:04d}!' for index, pwm, time_ms in commands]) + '}'
        self.send_command(command)

    def call_action_group(self, group_name):
        """
        根据组名调用动作，前提是动作已经存储。

        :param group_name: 动作组的名称，目前存储的动作组内容查看self.cellname_to_index
        :return: None
        """
        if group_name in self.cellname_to_index:
            group_index = self.cellname_to_index[group_name]
            command = f'$DGS:{group_index}!'
            self.send_command(command)
        else:
            print(f"Group '{group_name}' not found")
    
    def call_action_group_continuous(self, start, end, count):
        """
        循环调用从 start 到 end 的动作组，指定循环次数。

        :param start: 动作组的起始索引
        :param end: 动作组的结束索引
        :param count: 循环次数，0表示循环执行。
        :return: None
        """
        command = f'$DGT:{start:04d}-{end:04d},{count}!'
        self.send_command(command)
    
    def set_bias(self, index, bias):
        """
        设置指定舵机的偏差值。

        :param index: 舵机的索引
        :param bias: 偏差值，最大绝对值为100
        :return: None
        """
        command = f'#{index:03d}PSCK+{bias:03d}!'
        self.send_command(command)
    
    def stop_all(self):
        """
        停止所有舵机在当前位置。

        :return: None
        """
        command = '$DST!'
        self.send_command(command)
    
    def stop_index(self, index):
        """
        停止指定舵机在当前位置。

        :param index: 舵机的索引
        :return: None
        """
        command = f'$DST:{index}!'
        self.send_command(command)
    
    def close(self):
        """
        关闭串口连接。

        :return: None
        """
        if self.ser.is_open:
            self.ser.close()

if __name__ == "__main__":
    # 使用案例:
    controller = HandController('COM4', 115200)
    # controller.index_pwm_time(1, 1500, 1000)
    # controller.multiple_index_pwm_time([(0, 1500, 1000), (1, 900, 1000)])
    controller.call_action_group("二")
    # controller.call_action_group_continuous(0, 10, 1)
    # controller.set_bias(5, 10)
    # controller.stop_all()
    # controller.stop_index(1)
    # controller.close()
