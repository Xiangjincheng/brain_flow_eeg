# Base BrainFlow Analysis EEG

此项目通过OpenBCI的脑电帽检测脑电信号，通过分析脑电信号进行仿真手或者RGB灯珠的控制。

## 目录

- `dev/`: 依赖包源码
	- \- `brainflow/`brainflow依赖包源码
- `brain_main.py`: 脑电帽检测与控制主程序
- `hand_controller.py`:仿生手掌控制类函数库
- `led.py`: RGB灯珠控制类函数库
- `requirement.txt`: python依赖库
- `仿生手掌Yhand-mini动作组.ini`: 仿生手掌动作组配置文件

## 使用方法

直接运行brain_main.py（需要使用sudo权限）

```bash
loongson@loongson:~/eeg$ pwd
/home/loongson/eeg
loongson@loongson:~/eeg$ sudo python3 brain_main.py
#use sudor run it
```

## 灯珠与仿生手控制库使用

### 灯珠

引脚定义：V = 3.3V,	R = GPIO41,	G = GPIO44,	B = GPIO45

```python
if __name__ == "__main__":
    LED_R = 41
    LED_G = 44 
    LED_B = 45
    gpio_map = {'R': LED_R, 'G': LED_G, 'B': LED_B}

    gpio_control = GPIOControl(gpio_map)

    while True:
        gpio_control.set_led_color('R')
        time.sleep(1)
        gpio_control.set_led_color('G')
        time.sleep(1)
        gpio_control.set_led_color('B')
        time.sleep(1)
```

### 仿生手

目前手指只有5各舵机，分别对应驱动板index = 1~5

初始化类时需要根据自己电脑中串口号修改'COM4'，波特率目前固定115200。

```python
controller = HandController('COM4', 115200)
# controller.index_pwm_time(1, 1500, 1000)
# controller.multiple_index_pwm_time([(0, 1500, 1000), (1, 900, 1000)])
controller.call_action_group("一")
# controller.call_action_group_continuous(0, 10, 1)
# controller.set_bias(5, 10)
# controller.stop_all()
# controller.stop_index(1)
# controller.close()
```





