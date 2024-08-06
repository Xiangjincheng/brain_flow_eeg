import argparse
import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, WindowOperations, DetrendOperations, NoiseTypes, FilterTypes, AggOperations
import numpy as np
from led import LEDControl
from hand_controller import HandController

# LED control
LED_R = 41
LED_G = 44 
LED_B = 45
led_map = {'R': LED_R, 'G': LED_G, 'B': LED_B}
TRIGGLE = 40
led_control = LEDControl(led_map)

# Hand control
hand_control = HandController('COM4', 115200)
hand_control.call_action_group("石头")

def LED_control(alpha_power):
    if alpha_power > TRIGGLE:
        led_control.set_led_color('R')
    else:
        led_control.set_led_color('G')

def HAND_control(alpha_power):
    if alpha_power > TRIGGLE:
        hand_control.call_action_group("石头")
    else:
        hand_control.call_action_group("布")

def main():
    params = BrainFlowInputParams()
    params.serial_port = "/dev/ttyS3"
    board_id = BoardIds.CYTON_BOARD
    board = BoardShim(board_id, params)
    board_descr = BoardShim.get_board_descr(board_id)
    sampling_rate = int(board_descr['sampling_rate'])
    board.prepare_session()
    board.start_stream()
    time.sleep(10)

    while True:
        nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
        data = board.get_current_board_data(256)  # get all data and remove it from internal buffer
        band_power_alpha_list = []
        for channel_index in range(8):
            eeg_channels = board_descr['eeg_channels']
            eeg_channel = eeg_channels[channel_index]
            # optional detrend
            #------------------------Filter--------------------#
            DataFilter.perform_bandpass(data[eeg_channel], BoardShim.get_sampling_rate(board_id), 2.0, 50.0, 4,  #带通
                            FilterTypes.BESSEL_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[eeg_channel], BoardShim.get_sampling_rate(board_id), 48.0, 52.0, 3, #带阻
                            FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.remove_environmental_noise(data[eeg_channel], BoardShim.get_sampling_rate(board_id),      #环境噪声
                                        NoiseTypes.FIFTY.value)
            DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
            #------------------------Filter--------------------#
            
            psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                        WindowOperations.BLACKMAN_HARRIS.value)

            band_power_alpha = DataFilter.get_band_power(psd, 7.0, 13.0)
            band_power_alpha_list.append(band_power_alpha)
        band_power_alpha_sum =  sum(band_power_alpha_list)
        print(band_power_alpha_sum)
        LED_control(band_power_alpha_sum)

if __name__ == "__main__":
    main()