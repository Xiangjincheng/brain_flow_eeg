import os
import time

class GPIOControl:
    def __init__(self, gpio_map):
        self.gpio_map = gpio_map
        self.export_gpios()
        self.set_gpios_direction("out")

    def export_gpio(self, gpio_num):
        try:
            with open("/sys/class/gpio/export", "w") as f:
                f.write(str(gpio_num))
        except PermissionError:
            print(f"Permission denied. Please run the script as root to export GPIO {gpio_num}.")
        except FileExistsError:
            print(f"GPIO {gpio_num} already exported.")
        except Exception as e:
            print(f"An error occurred while exporting GPIO {gpio_num}: {e}")

    def set_gpio_direction(self, gpio_num, direction):
        try:
            with open(f"/sys/class/gpio/gpio{gpio_num}/direction", "w") as f:
                f.write(direction)
        except PermissionError:
            print(f"Permission denied. Please run the script as root to set direction for GPIO {gpio_num}.")
        except FileNotFoundError:
            print(f"The GPIO path /sys/class/gpio/gpio{gpio_num}/ does not exist. Please check the GPIO number.")
        except Exception as e:
            print(f"An error occurred while setting GPIO {gpio_num} direction: {e}")

    def set_gpio_value(self, gpio_num, value):
        try:
            with open(f"/sys/class/gpio/gpio{gpio_num}/value", "w") as f:
                f.write(str(value))
        except PermissionError:
            print(f"Permission denied. Please run the script as root to set value for GPIO {gpio_num}.")
        except FileNotFoundError:
            print(f"The GPIO path /sys/class/gpio/gpio{gpio_num}/ does not exist. Please check the GPIO number.")
        except Exception as e:
            print(f"An error occurred while setting GPIO {gpio_num} value: {e}")

    def export_gpios(self):
        for gpio in self.gpio_map.values():
            self.export_gpio(gpio)

    def set_gpios_direction(self, direction):
        for gpio in self.gpio_map.values():
            self.set_gpio_direction(gpio, direction)

    def set_led_value(self, led, value):
        if led in self.gpio_nums:
            self.set_gpio_value(led, value)
        else:
            print(f"LED {led} is not in the GPIO list")

    def set_led_color(self, color):
        if color in self.gpio_map:
            for col, gpio in self.gpio_map.items():
                value = 0 if col == color else 1
                self.set_gpio_value(gpio, value)
        else:
            print(f"Invalid color {color}. Valid colors are: {list(self.gpio_map.keys())}")

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